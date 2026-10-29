# Seminar contribution — Ngô Gia An (23120205)

Nội dung này dùng để Gia An đối chiếu và nhập vào Google Sheet của giảng viên. Không thay thao tác điền biểu mẫu hoặc xác nhận của người dùng.

## Phần đóng góp

| Phạm vi | Kết quả đã hoàn thành | Minh chứng |
|---|---|---|
| AI-1/AI-2 | Thiết kế luồng đọc class/source động; Gemini 3.6 sinh 7 test LoanService và bổ sung 3 test; review/apply kiểm full suite rồi dọn output tạm | PR #13, commits `b4b4d30`, `3bdbbc8`, `6c928b0`, `f351e88`; `scripts/ai_generate.py`, `scripts/ai_apply.py` |
| AI-3 | Tích hợp review diff test vào GitHub Actions; comment PR có kết quả AI và CI; retry hữu hạn, dừng khi hết quota ngày | PR #13, run `40889189664`; 49 JUnit test pass, line 76/83, branch 24/24 |
| AI-4 | Tự thiết kế trước 23 ca dữ liệu biên và notes; khóa trước khi so; đối chiếu với 13 ca Gemini | `ai/human/`, `evidence/tuan-06/ai-4/`; human 23/23, AI 13/13, 11 ca chung cùng kỳ vọng |
| Paper CoverUp | Kiểm nguồn/hạng; chạy phân tích dữ liệu công bố; tự chạy f003 với Gemini 3.6; áp dụng tool lên source Python nhóm | PR #14, `research/`, `evidence/tuan-06/papers/`; source nhóm 7 pass, coverage kết hợp 23,6% lên 96,4% |
| Paper Pynguin | Thay paper không chạy được bằng paper có artifact; chạy notebook tác giả, generation benchmark và thử source nhóm; ghi cả kết quả hạn chế | PR #14; notebook 134 module/40.200 dòng; benchmark 10 pass + 5 xfail, coverage nội bộ 81,48% |
| Tài liệu và trình bày | Khai báo AI, báo cáo AI/paper, slide 24–29 và kịch bản Video E | `ai-usage-declaration/01_NgoGiaAn.md`, `BaoCao_ChiTiet.md`, `slides/`, `KichBan_QuayVideo_Tuan_06.md` |

## Cách AI hỗ trợ

Codex hỗ trợ đọc source, triển khai script, chạy kiểm chứng và biên tập tài liệu. Gemini 3.6 Flash sinh/review test trong AI-1/2/3 và CoverUp. Pynguin không dùng LLM. Gia An cung cấp bộ human AI-4, tự chạy AI-1/2 LoanService và CoverUp f003, sau đó xác nhận review phần AI/paper ngày 29/10/2026. Chi tiết trung thực nằm trong `ai-usage-declaration/01_NgoGiaAn.md`.

## Việc người dùng còn phải tự thực hiện

- Nhập nội dung vào Google Sheet và xác nhận đúng phạm vi đóng góp.
- Dán URL/timestamp sau khi quay Video E.
- Ký bản AI usage declaration nếu bản nộp yêu cầu chữ ký.
