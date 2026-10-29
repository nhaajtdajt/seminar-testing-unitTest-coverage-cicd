#!/usr/bin/env bash
# Video C demo: start the packaged app, send each request from the script, stop the app.
# Usage: scripts/demo_case_study.sh [port]   (build first: case-study/mvnw -f case-study/pom.xml clean verify)
# Set PAUSE=1 to wait for Enter between steps while recording.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${1:-8081}"
JAR="$ROOT/case-study/target/library-case-study-0.1.0.jar"
LOG="$(mktemp)"
JAVA="${JAVA_HOME:+$JAVA_HOME/bin/}java"

[ -f "$JAR" ] || { echo "Missing $JAR; run: case-study/mvnw -f case-study/pom.xml clean verify"; exit 1; }
"$JAVA" -version 2>&1 | grep -q '"25' || { echo "Need JDK 25 (current: $("$JAVA" -version 2>&1 | head -1))"; exit 1; }

"$JAVA" -jar "$JAR" --server.address=127.0.0.1 --server.port="$PORT" > "$LOG" 2>&1 &
APP=$!
trap 'kill $APP 2>/dev/null; wait $APP 2>/dev/null || true; rm -f "$LOG"' EXIT

for _ in $(seq 60); do
  grep -q 'Started LibraryApplication' "$LOG" && break
  kill -0 $APP 2>/dev/null || { cat "$LOG"; exit 1; }
  sleep 0.5
done
grep -q 'Started LibraryApplication' "$LOG" || { echo "App did not start in 30s"; cat "$LOG"; exit 1; }
echo "App started on port $PORT (H2 in-memory, data.sql loaded)."

step() {
  local title="$1" body="$2" expect="$3"
  echo; echo "=== $title"; echo "POST /api/loans $body   (expect $expect)"
  curl -s -w '\n-> HTTP %{http_code}\n' "http://127.0.0.1:$PORT/api/loans" -H 'Content-Type: application/json' -d "$body"
  if [ "${PAUSE:-0}" = 1 ]; then read -r -p "[Enter]"; fi
}

step "1. Muon hop le: sach 1, thanh vien 1" '{"bookId":1,"memberId":1}' "201"
step "2. Muon lai sach 1" '{"bookId":1,"memberId":1}' "409 BOOK_UNAVAILABLE"
step "3. Sach khong ton tai" '{"bookId":99,"memberId":1}' "404 BOOK_NOT_FOUND"
step "4. Thanh vien khong ton tai" '{"bookId":3,"memberId":99}' "404 MEMBER_NOT_FOUND"
step "5. Request sai: bookId am" '{"bookId":-1,"memberId":1}' "400"
step "6. Thanh vien 2 con no 5.000d" '{"bookId":3,"memberId":2}' "409 UNPAID_FINE"
step "7. Sach 3 van con, thanh vien 1 muon duoc" '{"bookId":3,"memberId":1}' "201"
echo; echo "Done. Stopping app; data resets on next start."
