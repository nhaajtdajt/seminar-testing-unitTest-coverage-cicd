#!/usr/bin/env python3
"""Review PR data in parallel with CI, then upsert one comment even when the gate fails."""
import argparse
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import ai_review
import gemini_client as client

ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- seminar-gemini-ai3 -->"
SHA = re.compile(r"[0-9a-f]{40}")


def pull_context(event):
    pr = event.get("pull_request", {})
    repository = event.get("repository", {}).get("full_name", "")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Invalid repository identity")
    if pr.get("head", {}).get("repo", {}).get("full_name") != repository:
        raise ValueError("Fork PRs are excluded from secret-bearing AI jobs")
    base, head = pr.get("base", {}).get("sha", ""), pr.get("head", {}).get("sha", "")
    number = pr.get("number") or event.get("number")
    if not SHA.fullmatch(base) or not SHA.fullmatch(head) or type(number) is not int or number < 1:
        raise ValueError("Invalid PR number or revision")
    return {"repository": repository, "pr": number, "base": base, "head": head}


def git(*arguments):
    return subprocess.check_output(["git", *arguments], cwd=ROOT, text=True)


def read_diff(context):
    revision = context["base"] + "..." + context["head"]
    paths = ["case-study/src", "case-study/pom.xml"]
    diff = git("diff", "--no-ext-diff", "--no-textconv", revision, "--", *paths)
    files = git("diff", "--name-only", "-z", revision, "--", *paths).strip("\0").split("\0")
    if len(diff.encode()) > 80_000:
        raise ValueError("PR diff exceeds 80 KB; no silent truncation or clean-review claim")
    return diff, [name for name in files if name]


def review(event, output):
    context = pull_context(event)
    output.mkdir(parents=True, exist_ok=True)
    client.save(output / "context.json", context)
    state = {"status": "preparing", "api_completed": False, "head": context["head"]}
    try:
        diff, files = read_diff(context)
        context["changed_files"] = files
        client.save(output / "context.json", context)
        if not diff.strip():
            state.update(status="no_app_changes", message="No case-study source/POM diff to review")
            return 0
        if not os.environ.get("GEMINI_API_KEY") or not os.environ.get("AI_MODEL"):
            state.update(status="not_configured", message="Configure repository secret GEMINI_API_KEY and variable AI_MODEL")
            return 0
        template = (ROOT / "ai/prompts/AI-3-review.md").read_text()
        text = template.replace("{{DIFF}}", diff)
        text += ("\nThis review runs in parallel with JUnit/JaCoCo. Their results are not available yet. "
                 "Do not claim test/coverage pass or fail; the final PR comment separately adds measured CI results. "
                 "Limit findings to changed files, with repository-relative paths and real diff line numbers.")
        answer = client.generate(text, output / "model")
        ai_review.validate_review(answer)
        invalid = [finding for finding in answer["findings"] if finding["file"] not in files]
        if invalid:
            raise ValueError("Model returned findings outside the reviewed diff")
        client.save(output / "review.json", answer)
        api = json.loads((output / "model/api.json").read_text())
        state.update(status="reviewed", api_completed=True, model=api["model"],
                     findings=len(answer["findings"]), attempts=api["attempts"])
        return 0
    except (ValueError, RuntimeError, OSError, KeyError, subprocess.SubprocessError) as error:
        state.update(status="error", error_type=type(error).__name__)
        print(f"AI review unavailable ({type(error).__name__}); CI results will still be posted.", file=sys.stderr)
        return 1
    finally:
        client.save(output / "result.json", state)


def safe_text(value, limit=1500):
    # Never let source/model text mention people or inject HTML/Markdown blocks.
    text = html.escape(str(value))[:limit].replace("@", "@\u200b")
    for char in ("\\", "`", "*", "_", "[", "]", "|", "#"):
        text = text.replace(char, "\\" + char)
    return " ".join(text.split())


def bounded_json(path):
    if not path.is_file():
        return None
    if path.stat().st_size > 1_000_000:
        raise ValueError("Oversized AI artifact")
    return json.loads(path.read_text())


def ci_reports(artifacts):
    totals = {key: 0 for key in ("tests", "failures", "errors", "skipped")}
    reports = list((artifacts / "tests-jdk-25").glob("TEST-*.xml"))
    if len(reports) > 300:
        raise ValueError("Too many test reports")
    for path in reports:
        if path.stat().st_size > 2_000_000:
            raise ValueError("Oversized test report")
        suite = ET.parse(path).getroot()
        for key in totals:
            totals[key] += int(suite.get(key, "0"))
    coverage, classes = {}, []
    xml = artifacts / "coverage/jacoco.xml"
    if xml.is_file():
        if xml.stat().st_size > 5_000_000:
            raise ValueError("Oversized JaCoCo report")
        root = ET.parse(xml).getroot()
        coverage = {c.get("type"): (int(c.get("covered")), int(c.get("missed"))) for c in root.findall("counter")}
        for node in root.findall(".//class"):
            counters = {c.get("type"): (int(c.get("covered")), int(c.get("missed"))) for c in node.findall("counter")}
            classes.append({"name": node.get("name", ""), "coverage": counters})
    return {"tests_available": bool(reports), "totals": totals, "coverage": coverage, "classes": classes}


def ratio(counters, key):
    values = counters.get(key)
    if not values or sum(values) == 0:
        return "N/A"
    return f"{values[0]}/{sum(values)} ({100 * values[0] / sum(values):.1f}%)"


def comment_body(context, artifacts, statuses, run_url):
    review_dir = artifacts / "ai-review"
    saved = bounded_json(review_dir / "context.json")
    result = bounded_json(review_dir / "result.json") or {"status": "missing_artifact"}
    answer = bounded_json(review_dir / "review.json")
    if saved and any(saved.get(key) != context[key] for key in ("repository", "pr", "base", "head")):
        raise ValueError("AI artifact belongs to a different PR revision")
    lines = [MARKER, "## Gemini AI-3 review", "",
             f"PR #{context['pr']} · commit `{context['head'][:12]}` · [GitHub Actions]({run_url})", "",
             "### Kết quả CI", "", "| Check | Trạng thái |", "|---|---|"]
    for name in ("test", "coverage-gate", "package"):
        lines.append(f"| {name} | {safe_text(statuses.get(name, 'unknown'))} |")
    try:
        measured = ci_reports(artifacts)
        if measured["tests_available"]:
            counts = measured["totals"]
            lines += ["", f"JUnit: {counts['tests']} tests; failures={counts['failures']}; "
                      f"errors={counts['errors']}; skipped={counts['skipped']}."]
        else:
            lines += ["", "Chưa có Surefire report hợp lệ cho lượt này; không tự suy ra test pass."]
        if measured["coverage"]:
            lines += ["", f"JaCoCo toàn project: LINE {ratio(measured['coverage'], 'LINE')}; "
                      f"BRANCH {ratio(measured['coverage'], 'BRANCH')}."]
            changed = set((saved or {}).get("changed_files", []))
            selected = [c for c in measured["classes"] if "case-study/src/main/java/" + c["name"].split('$')[0] + ".java" in changed]
            if selected:
                lines += ["", "| Class đổi trong PR | LINE | BRANCH |", "|---|---|---|"]
                for item in selected[:20]:
                    lines.append(f"| {safe_text(item['name'])} | {ratio(item['coverage'], 'LINE')} | {ratio(item['coverage'], 'BRANCH')} |")
        else:
            lines += ["", "Chưa có JaCoCo report; không tự suy ra coverage đạt ngưỡng."]
    except (ValueError, ET.ParseError, OSError) as error:
        lines += ["", f"Không đọc được report ({type(error).__name__}); dùng trạng thái job/log CI làm căn cứ."]
    if statuses.get("coverage-gate") == "failure":
        lines += ["", "**Coverage job đỏ.** Xem log để phân biệt vi phạm ngưỡng với lỗi build/test/môi trường; AI không đổi kết quả gate."]
    elif statuses.get("coverage-gate") == "skipped":
        lines += ["", "Coverage gate bị bỏ qua; thường do test trước đó lỗi hoặc lượt chạy bị hủy, không có kết luận đạt coverage."]
    lines += ["", "### Nhận xét Gemini về diff", ""]
    if result.get("status") == "reviewed" and result.get("api_completed") and answer:
        ai_review.validate_review(answer)
        lines.append(f"Model: `{safe_text(result.get('model', 'unknown'))}`. Review diff chạy song song với CI.")
        if not answer["findings"]:
            lines.append("Gemini không nêu finding trên diff được gửi; đây không phải chứng nhận code/test hoàn toàn đúng.")
        for item in answer["findings"][:30]:
            if item["file"] not in (saved or {}).get("changed_files", []):
                raise ValueError("Finding path outside reviewed diff")
            link = (f"https://github.com/{context['repository']}/blob/{context['head']}/"
                    + urllib.parse.quote(item["file"], safe="/") + f"#L{item['line']}")
            lines.append(f"- **{safe_text(item['rule'], 80)}** [{safe_text(item['file'])}:{item['line']}]({link}): {safe_text(item['message'])}")
    elif result.get("status") == "no_app_changes":
        lines.append("PR không thay đổi source/POM của case study; không gọi Gemini cho phần ứng dụng.")
    elif result.get("status") == "not_configured":
        lines.append("**Chưa gọi Gemini:** cần repository secret `GEMINI_API_KEY` và cấu hình model.")
    else:
        lines.append("**Chưa có review Gemini hoàn chỉnh** (API/job/artifact lỗi). Không nhận là AI đã duyệt PR; xem Actions log.")
    lines += ["", "Test/coverage là kết quả đo của CI; Gemini chỉ review diff và chưa nhận các report chạy sau đó. "
              "Nhận xét AI không thay required checks, không tự sinh/sửa/merge test."]
    return "\n".join(lines)[:60000]


def github(method, path, data=None):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN is required for PR comments")
    request = urllib.request.Request("https://api.github.com" + path,
        data=json.dumps(data).encode() if data is not None else None, method=method,
        headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json", "X-GitHub-Api-Version": "2022-11-28"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def publish(context, body):
    prefix = "/repos/" + context["repository"]
    current = github("GET", prefix + f"/pulls/{context['pr']}")
    if current.get("head", {}).get("sha") != context["head"] or current.get("state") != "open":
        print("PR closed or head changed; stale comment ignored.")
        return "stale"
    existing = None
    for page in range(1, 101):
        comments = github("GET", prefix + f"/issues/{context['pr']}/comments?per_page=100&page={page}")
        existing = next((c for c in comments if c.get("user", {}).get("login") == "github-actions[bot]"
                         and c.get("body", "").startswith(MARKER)), existing)
        if len(comments) < 100:
            break
    # Check again immediately before a write so an older run does not replace newer findings.
    current = github("GET", prefix + f"/pulls/{context['pr']}")
    if current.get("head", {}).get("sha") != context["head"] or current.get("state") != "open":
        return "stale"
    if existing:
        result = github("PATCH", prefix + f"/issues/comments/{existing['id']}", {"body": body})
    else:
        result = github("POST", prefix + f"/issues/{context['pr']}/comments", {"body": body})
    print("PR comment: " + result.get("html_url", "updated"))
    return "posted"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("review", "comment"))
    parser.add_argument("--event", type=Path, default=Path(os.environ.get("GITHUB_EVENT_PATH", "event.json")))
    parser.add_argument("--output", type=Path, default=Path(".ai-work/ci-review"))
    parser.add_argument("--artifacts", type=Path, default=Path(".ai-work/ci-artifacts"))
    args = parser.parse_args()
    try:
        event = json.loads(args.event.read_text())
        if args.mode == "review":
            return review(event, args.output)
        context = pull_context(event)
        run_id = os.environ.get("GITHUB_RUN_ID", "")
        if not run_id.isdecimal():
            raise ValueError("Invalid workflow run identity")
        statuses = {"test": os.getenv("TEST_RESULT", "unknown"), "coverage-gate": os.getenv("COVERAGE_RESULT", "unknown"),
                    "package": os.getenv("PACKAGE_RESULT", "unknown")}
        body = comment_body(context, args.artifacts, statuses,
                            f"https://github.com/{context['repository']}/actions/runs/{run_id}")
        return 0 if publish(context, body) in ("posted", "stale") else 1
    except (ValueError, OSError, KeyError, urllib.error.URLError) as error:
        print(f"AI-3 {args.mode} failed ({type(error).__name__}); credentials and response body omitted.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
