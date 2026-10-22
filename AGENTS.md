# Đồ án Xử lý ảnh số: Phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ MRI
**Học phần:** Xử lý ảnh số — Bộ môn Khoa học Dữ liệu — Khoa CNTT — Trường ĐH Công Thương TP.HCM (HUIT)  
**Năm học:** 2026–2027  
**Repository:** [brain-tumor-mri-segmentation](https://github.com/mtzwyu/brain-tumor-mri-segmentation)

## Thông tin nhóm thực hiện
| STT | Họ và Tên | Mã số sinh viên | Vai trò |
| :---: | :--- | :---: | :--- |
| 1 | **Hà Mạnh Trường** | **2045240326** | Nhóm trưởng, Pipeline tiền xử lý & Tách sọ (Skull Stripping), Thuật toán phân đoạn u lõi (Watershed/Region Growing), Báo cáo khoa học |
| 2 | **Huỳnh Tâm Trí** | **2045240315** | Thành viên, Dữ liệu MRI & Ground truth, Rút trích đặc trưng hình học khối u, Đánh giá định lượng (Dice/IoU), Demo GUI |

---

# Global Multi-Agent Guidelines & Smart Model Router Protocol

Behavioral guidelines adapted from Andrej Karpathy's engineering principles (`CLAUDE.md`), Antigravity with ChatGPT planning standards, and Smart Model Router architecture. Applies globally across all Antigravity projects and agent sessions.

---

## 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- State your assumptions explicitly before implementing. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear or ambiguous, STOP. Name what is confusing. Ask.

---

## 2. Planning with Antigravity & ChatGPT (Mandatory for Multi-Step Tasks)
**Define clear success criteria. Decompose before coding using Antigravity with ChatGPT standards.**
- **Cơ chế kết hợp:**
  - **Antigravity:** Đóng vai trò Agentic Harness — quản lý workspace, sinh Artifacts kế hoạch (`implementation_plan.md` / `task.md`), điều phối ngữ cảnh và quản lý vòng lặp thực thi độc lập.
  - **ChatGPT / Advanced Reasoning:** Đóng vai trò bộ não lập luận kiến trúc — phân tích yêu cầu sâu, bóc tách module, phản biện thiết kế và đề xuất lộ trình.
- **Khởi động Bridge Server riêng biệt cho từng Workspace khi phối hợp với ChatGPT:**
  - **Nguyên tắc "Từng con riêng từng workspace":** Tuyệt đối **không** dùng chung một tiến trình server cho tất cả các workspace và không gộp chung nhiều workspace vào cùng một server. Mỗi workspace phải có một tiến trình server bridge độc lập tương ứng với đúng đường dẫn của workspace đó (`--workspace <đường_dẫn_workspace_hiện_tại>`), giúp cô lập hoàn toàn ngữ cảnh, tránh rò rỉ dữ liệu (context bleed) giữa các dự án.
  - **Cách khởi động đúng kèm Cloudflare Tunnel & Pairing Code**:
    Khi kích hoạt quy trình lập kế hoạch phối hợp với ChatGPT Web (A2C bridge), sử dụng lệnh `setup` (hoặc `start --tunnel`) để khởi tạo Cloudflare Tunnel công khai (`https://*.trycloudflare.com/mcp`) và sinh Pairing Code OAuth:
    ```bash
    node C:\Users\xpaga\codex-with-chatgpt\bin\c2c.js setup --workspace <đường_dẫn_workspace_hiện_tại>
    # hoặc dùng lệnh CLI toàn cục:
    a2c setup -w <đường_dẫn_workspace_hiện_tại>
    ```
    *Lưu ý:* Tuyệt đối không dùng lệnh `serve` trần vì `serve` chỉ mở port nội bộ `127.0.0.1` mà không tạo Cloudflare Tunnel công khai, khiến ChatGPT Web không thể kết nối.
  - **Chế độ Tự Chủ (Standalone Mode / Fallback):**
    Nếu tác vụ người dùng không yêu cầu cầu nối ChatGPT Web bên ngoài, hoặc khi Cloudflare Tunnel/mạng gặp sự cố, Antigravity **được phép lập kế hoạch và thực thi độc lập 100% (Standalone Harness)** bằng chính các model tư duy tích hợp (Gemini Flash/Pro Thinking, Smart Model Router) mà không để quy trình bị nghẽn hay gián đoạn.
  - Sau khi Bridge Server của workspace hiện tại sẵn sàng, tận dụng ChatGPT đóng vai trò bộ não lập luận kiến trúc hỗ trợ Antigravity lên kế hoạch chuẩn xác.
- **Biến quyết định thành spec (`to-spec`):** Trước khi code tính năng lớn, chốt rõ ranh giới, seams, và quyết định kiến trúc thành tài liệu đặc tả.
- **Bóc tách thành Tracer-Bullet Tickets (`to-tickets`):** Cắt nhỏ task phức tạp thành các ticket tự chứa, có thứ tự phụ thuộc (Blocked by) và tiêu chí nghiệm thu có thể demo/verify được.
- **Cấu trúc thực thi từng bước (Bắt buộc tiêu chí xác minh):**
```
1. [Bước triển khai] -> verify: [Lệnh test / Tiêu chí nghiệm thu]
2. [Bước triển khai] -> verify: [Lệnh test / Tiêu chí nghiệm thu]
3. [Bước triển khai] -> verify: [Lệnh test / Tiêu chí nghiệm thu]
```
- Tiêu chí thành công mạnh mẽ giúp Agent tự chạy vòng lặp kiểm tra độc lập. Tránh các tiêu chí mơ hồ như "làm cho nó chạy".

---

## 3. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No defensive error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
- Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

---

## 4. Surgical Changes
**Touch only what you must. Clean up only your own mess.**
- When editing existing code:
  - Match existing style and conventions, even if you'd do it differently.
  - Don't "improve" adjacent code, comments, or formatting.
  - Don't refactor things that aren't broken.
  - If you notice unrelated dead code, mention it — don't delete it without permission.
- When your changes create orphans:
  - Remove imports/variables/functions that YOUR changes made unused.
  - Don't remove pre-existing dead code unless asked.
- The Golden Test: Every changed line in a diff should trace directly to the user's request.

---

## 5. Model Selection via Smart Model Router
**Route each task to the cheapest and fastest model that clears the quality bar.**
- **Default Working Tier:** Claude Sonnet 5 or Gemini Flash (`Model: flash`). Do NOT default to expensive models (Opus / Gemini Pro) for routine coding or lookups.
- **Tier 1 - Retrieval & Lookups (`flash_lite` / Haiku 4.5):** File lookups, regex, CSV/JSON extraction, bulk classification, status checks, market data parsing.
- **Tier 2 - Coding & Testing (`flash` / Sonnet 5 / Grok 4.5):** The default working tier for well-specified coding, unit tests (pytest, vitest), indicator math, and refactoring. Grok 4.5 is the fastest median coder (~2.5 min/task).
- **Tier 3 - Deep Reasoning & Auditing (`pro` / Opus 4.8 / Fable 5):** Multi-file architecture, mathematical modeling, cointegration/Monte Carlo, and adversarial risk audits.
- **Operating Modes:**
  - `balanced` (default): cheapest model within delta=0.10 of best pass@k with CI-low >= 0.5.
  - `fast`: lowest median latency (Grok 4.5).
  - `frugal`: lowest cost clearing quality bar (Flash-Lite / Haiku).
  - `deep`: capability ceiling (highest pass@k, tightest CI).
- **Measured Ties:** NEVER break measured ties arbitrarily. Surface options to the user.
- **Attribution & Logging:** Always attribute the model used: `> **[{Model Name}]** — {reason}` and log decisions to `logs/routing-log.jsonl`. Use `router stats` or `router review`.

---

## 6. Execution Safety Floor & Risk Guardrails
**Non-negotiable controls for trading, financial, and production code:**
1. **Zero Unsupervised Live Orders:** No model has autonomous authority to execute real-capital transactions or submit live orders. Live execution requires explicit human authorization (`HOLD_FOR_APPROVAL`).
2. **Deterministic Lookahead Bias Prevention:** Lookahead bias (e.g. `df['close'].shift(-1)`, forward indexing `iloc[i+1]`) is strictly forbidden in backtesting and time-series pipelines. Signals at $t$ execute at $t+1$.
3. **Mandatory Friction & Stop-Loss:** Backtests must model realistic fees (0.05% - 0.10%) and slippage. Position entries must define a deterministic stop-loss price.
4. **Secret Isolation:** Never hardcode, display, or commit API keys, private keys, or credentials.
5. **Deterministic Pre-Execution Audit:** Audit code before execution: `router check-safety <file>`.

---

## Agent skills

### Issue tracker

Issues and specs live in GitHub Issues via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Uses the default labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout using root `GLOSSARY.md` and `docs/adr/`. See `docs/agents/domain.md`.

---

## 7. Quy chuẩn Định dạng Văn bản Báo cáo Đồ án (Word / DOCX Format)
**Áp dụng bắt buộc cho toàn bộ báo cáo đồ án, thuyết minh chuyên đề khi xuất định dạng Microsoft Word (`.docx`), trích xuất chuẩn hóa từ tệp mẫu `docs/Nhom12_BaoCao.docx`:**

* **Kỹ năng Word bắt buộc:** Sử dụng thư viện `python-docx` kết hợp module điều phối `src/report/docx_builder.py` để sinh và thao tác văn bản Word.
* **Quy chuẩn Căn lề trang in (Page Margins chuẩn NXB & HUIT):**
  * Khổ giấy: **Letter** (`21.59 cm x 27.94 cm`) hoặc **A4** (`21.00 cm x 29.70 cm`).
  * Lề trên (Top): **3.0 cm**
  * Lề dưới (Bottom): **3.0 cm**
  * Lề trái (Left): **3.0 cm** (khoảng cách đóng gáy hồ sơ)
  * Lề phải (Right): **2.0 cm**
  * Khoảng cách Header / Footer: **1.27 cm** (0.5 inch).
* **Quy chuẩn Kiểu chữ & Đoạn văn bản (Body Text / Normal Style):**
  * Font chữ: **Times New Roman** thống nhất 100% toàn bộ văn bản.
  * Cỡ chữ nội dung: **13.0 pt** (`w:sz = 26` nửa pt).
  * Căn lề đoạn: **Căn đều hai bên (Justified / Both)** (`w:jc = both`).
  * Giãn cách dòng: **1.5 lines** (`w:line = 360` twips, `lineRule = auto`).
  * Khoảng cách đoạn: Trước đoạn **0 pt**, Sau đoạn **4.0 pt** (`w:after = 80` twips).
  * Thụt đầu dòng (First Line Indent): **1.27 cm** (`w:ind = 720` twips) cho các đoạn văn xuôi nội dung; tiêu đề và bảng biểu đặt **0 cm**.
* **Quy tắc phân cấp Tiêu đề (Heading Hierarchy):**
  * **Heading 1 (Chương & Mục lớn mở đầu):** Dùng cho `LỜI MỞ ĐẦU`, `TÓM TẮT`, `BẢNG PHÂN CÔNG NHIỆM VỤ`, `MỤC LỤC`, `CHƯƠNG 1...`, `TÀI LIỆU THAM KHẢO`, `PHỤ LỤC`. Định dạng: **15.0 pt**, **IN HOA, IN ĐẬM**, **Căn giữa** (`CENTER`), Trước: **12.0 pt**, Sau: **6.0 pt**.
  * **Heading 2 (Tiểu mục cấp 1: X.Y):** Dùng cho `1.1`, `1.2`, `2.1`... Định dạng: **13.5 pt**, **Chữ thường, IN ĐẬM**, **Căn trái** (`LEFT`), Trước: **8.0 pt**, Sau: **0 pt**.
  * **Heading 3 (Tiểu mục cấp 2: X.Y.Z):** Dùng cho `1.1.1`, `1.2.1`... Định dạng: **13.0 pt**, **Chữ thường, IN NGHIÊNG**, **Căn trái** (`LEFT`), Trước: **6.0 pt**, Sau: **2.0 pt**.
* **Quy chuẩn Bảng biểu (Tables) & Caption:**
  * Cỡ chữ trong ô bảng: **10.5 pt - 11.0 pt**, giãn dòng đơn (1.0) hoặc 1.15 lines.
  * Hàng tiêu đề (Header row): **In đậm (Bold)**, căn giữa ô.
  * Ô dữ liệu chữ căn trái, ô dữ liệu số căn giữa hoặc căn phải.
  * **Vị trí Caption Bảng:** Nằm **TRÊN** bảng. Định dạng: `Bảng X.Y: Tên bảng`, cỡ chữ **11.5 pt**, **In nghiêng (Italic)**, căn giữa (`CENTER`), Sau 4.0 pt.
* **Quy chuẩn Hình ảnh (Figures) & Caption:**
  * Hình ảnh được căn giữa trang (`CENTER`).
  * **Vị trí Caption Hình:** Nằm **DƯỚI** hình. Định dạng: `Hình X.Y: Tên hình ảnh minh họa`, cỡ chữ **11.5 pt**, **In nghiêng (Italic)**, căn giữa (`CENTER`), Trước 4.0 pt, Sau 6.0 pt.
* **Quy chuẩn Trang bìa (Cover Page Layout):**
  * Căn giữa toàn bộ trang bìa, không đánh số trang:
    1. `TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP. HỒ CHÍ MINH` (15.0 pt, In hoa, In đậm, Sau 6pt).
    2. `KHOA CÔNG NGHỆ THÔNG TIN` (14.0 pt, In hoa, In đậm, Sau 6pt).
    3. `BỘ MÔN KHOA HỌC DỮ LIỆU` (14.0 pt, In hoa, In đậm, Sau 6pt).
    4. `BÁO CÁO ĐỒ ÁN HỌC PHẦN` (13.0 pt, In hoa, Đứng).
    5. `XỬ LÝ ẢNH SỐ` (14.0 pt, In hoa, In đậm, Sau 6pt).
    6. `ĐỀ TÀI` (16.0 pt, In hoa, In đậm).
    7. `PHÂN ĐOẠN VÀ PHÁT HIỆN KHỐI U NÃO TRÊN ẢNH CỘNG HƯỞNG TỪ MRI` (16.0 pt, In hoa, In đậm).
    8. `(BỘ DỮ LIỆU CHUẨN TCGA-LGG)` (13.0 pt, In nghiêng).
    9. `Giảng viên hướng dẫn: ...` (13.0 pt).
    10. `Sinh viên thực hiện:` (13.0 pt, In đậm), liệt kê đầy đủ thành viên, MSSV và tỷ lệ đóng góp (50% - 50%).
    11. `TP. Hồ Chí Minh, Năm 2026` (13.0 pt, In đậm).
* **Khung Cấu Trúc 8 Chương chuẩn mực Bộ môn KHDL - HUIT:**
  * Bìa ngoài & Bìa trong $\rightarrow$ Lời mở đầu $\rightarrow$ Tóm tắt $\rightarrow$ Bảng phân công nhiệm vụ $\rightarrow$ Mục lục, Danh mục bảng, Danh mục hình $\rightarrow$ **Chương 1: Giới thiệu đề tài** $\rightarrow$ **Chương 2: Cơ sở lý thuyết Xử lý ảnh số** $\rightarrow$ **Chương 3: Mô tả tập dữ liệu MRI TCGA-LGG** $\rightarrow$ **Chương 4: Tiền xử lý ảnh và Tách sọ não** $\rightarrow$ **Chương 5: Phương pháp phân đoạn u não và Pipeline** $\rightarrow$ **Chương 6: Kết quả thực nghiệm và Đánh giá định lượng** $\rightarrow$ **Chương 7: Xây dựng ứng dụng minh họa Demo Web UI** $\rightarrow$ **Chương 8: Kết luận và Hướng phát triển** $\rightarrow$ **Tài liệu tham khảo (chuẩn IEEE `[1]`, `[2]`)** $\rightarrow$ **Phụ lục**.

