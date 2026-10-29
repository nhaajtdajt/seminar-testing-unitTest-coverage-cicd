# Minh chứng AI-5 — LoanService (28/10/2026)

**Phụ trách:** Ngô Gia An (23120205). **Thực hiện lượt chạy:** Codex, local JDK 25.0.5. Đây là snapshot tương tác trước luồng Gemini thật, không phải output Gemini hoặc artifact paper. Gia An đã review phạm vi AI/paper ngày 29/10; kết quả Gemini 3.6 mới nằm trên PR #13 và được khai báo riêng.

| Lượt | Test / kết quả | LoanService line / branch | Minh chứng |
|---|---|---|---|
| Nháp | 2 pass | 14/17; 3/6 | [draft/run.json](draft/run.json), [gaps](draft/gaps.json), XML ở `draft/site/jacoco/` |
| Bổ sung | 10 pass (gồm 2 kế thừa từ nháp) | 17/17; 6/6 | [improved/run.json](improved/run.json), XML ở `improved/site/jacoco/` |
| Oracle sai | 3 lượt, đúng 1 assertion failure; Maven exit 1 | Không xuất JaCoCo vì verify dừng ở test | [mistake/run.json](mistake/run.json), [log](mistake/output.log) |
| PIT | 9 KILLED/9 mutant | Chỉ tập mutator đã cấu hình | [pit-strong/run.json](pit-strong/run.json), [mutations.xml](pit-strong/pit-reports/mutations.xml) |
| PIT lỗi quyền | Chưa chạy mutation | Không có score | [pit-failed-permissions/run.json](pit-failed-permissions/run.json) |
| PIT lỗi mạng | Maven Central HTTP 502, chưa chạy mutation | Không có score | [pit-failed-network/run.json](pit-failed-network/run.json) |

## Cách tái hiện

Từ gốc repo, chọn output mới và chạy tuần tự:

```bash
python3 scripts/run_ai_demo.py draft --output /tmp/ai-loan-draft
python3 scripts/run_ai_demo.py improved --output /tmp/ai-loan-improved
python3 scripts/run_ai_demo.py mistake --output /tmp/ai-loan-mistake
python3 scripts/run_ai_demo.py mutation --output /tmp/ai-loan-pit
```

## Giới hạn

- Fixture sai cố ý kỳ vọng được mượn khi đang giữ 3 sách; không phải lỗi model quan sát được. Không sửa nghiệp vụ để làm fixture này pass.
- 100% branch/9 mutant bị diệt không chứng minh mọi yêu cầu hay vấn đề đồng thời đã được kiểm.
- Lượt thất bại giữ nguyên và không tính vào kết quả PIT. Một metadata cũ từng gắn Surefire từ lượt khác đã được sửa có ghi chú; collector hiện chỉ nhận report mới của lượt chạy.
- File evidence được chuyển thư mục ngày 29/10, không chạy lại hoặc đổi số liệu. [Nhận xét AI-5](../../../ai/results/AI-5-loan-review.md) và [hướng dẫn chung](../../../docs/thuc-hanh/HuongDan_Demo.md).
