# BẢN PHÂN CÔNG NHIỆM VỤ ĐỘC LẬP — TUẦN 1
## Thành viên phụ trách: HUỲNH TÂM TRÍ (MSSV: 2045240315)
* **Vai trò trong đồ án:** Thành viên — Chuyên trách Dữ liệu thực nghiệm, Bộ đo định lượng & Giao diện người dùng
* **Học phần:** Xử lý ảnh số (2026–2027) — Khoa CNTT — Trường ĐH Công Thương TP.HCM (HUIT)
* **Đề tài:** Phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ MRI

---

## 🎯 1. Mục Tiêu Trọng Tâm Trong Tuần 1 Của Trí
Tập trung 100% vào **khảo sát tập dữ liệu thực nghiệm MRI, đặc tả cơ sở toán học của bộ đo đánh giá (Dice, IoU, Sensitivity, Specificity) và phác thảo Wireframe giao diện demo**. Hoàn toàn **không phụ thuộc** vào phần việc của Hà Mạnh Trường và **chưa cần viết code logic** trong tuần này.

---

## 📋 2. Chi Tiết Các Hạng Mục Công Việc Độc Lập

### Hạng mục 1: Khảo sát & Lập Báo cáo Khám phá Dữ liệu (`docs/DATA_EXPLORATION_REPORT.md`)
* **Nội dung:**
  * Khảo sát toàn bộ 20 cặp ảnh MRI và mặt nạ Ground Truth đã có sẵn trong `data/sample/images/` và `data/sample/masks/`.
  * Phân tích, thống kê các đặc tính quan trọng:
    * Kích thước ảnh, định dạng, độ sâu màu (Grayscale uint8 0–255).
    * Phân nhóm dữ liệu theo diện tích khối u:
      * Nhóm u nhỏ ($< 1.5\%$ diện tích ảnh): Ghi rõ mã ca (ví dụ: ca 05, 11, 12, 13, 16, 19, 20).
      * Nhóm u trung bình ($1.5\% - 5\%$): Các ca 01, 02, 03, 04, 06, 14, 15, 17, 18.
      * Nhóm u lớn ($> 5\%$): Các ca 07, 08, 09, 10.
    * Đánh giá trực quan về độ tương phản giữa khối u và nhu mô não xung quanh; ghi nhận các ca u có bờ mờ hoặc nằm sát rìa sọ.
* **Sản phẩm bàn giao:** File tài liệu `docs/DATA_EXPLORATION_REPORT.md` kèm bảng số liệu chi tiết.

### Hạng mục 2: Nghiên cứu & Soạn thảo Cơ sở Lý thuyết Bộ đo Định lượng (`docs/THEORY_EVALUATION_METRICS.md`)
* **Nội dung:**
  * Viết tài liệu giải thích chi tiết bản chất toán học và ý nghĩa y khoa của 4 chỉ số đánh giá phân đoạn ảnh:
    1. **Dice Similarity Coefficient (DSC / F1-Score):**
       $$\text{Dice} = \frac{2 |P \cap G|}{|P| + |G|} = \frac{2 \cdot \text{TP}}{2 \cdot \text{TP} + \text{FP} + \text{FN}}$$
    2. **Jaccard Index (IoU - Intersection over Union):**
       $$\text{IoU} = \frac{|P \cap G|}{|P \cup G|} = \frac{\text{Dice}}{2 - \text{Dice}}$$
    3. **Độ nhạy (Sensitivity / Recall / True Positive Rate):** Đo tỷ lệ vùng u thực tế được thuật toán phát hiện đúng.
    4. **Độ đặc hiệu (Specificity / True Negative Rate):** Đo khả năng thuật toán không nhận nhầm mô lành thành u.
  * Tự tạo một ví dụ minh họa bằng số học cụ thể trên ma trận nhị phân nhỏ $4 \times 4$ để minh chứng cách tính từng chỉ số (chuẩn bị làm nội dung cho báo cáo cuối kỳ).
* **Sản phẩm bàn giao:** File tài liệu `docs/THEORY_EVALUATION_METRICS.md`.

### Hạng mục 3: Thiết kế Bản vẽ Wireframe / Bố cục Giao diện Demo Streamlit (`docs/GUI_WIREFRAME_MOCKUP.md`)
* **Nội dung:**
  * Lên ý tưởng và phác thảo giao diện trực quan cho ứng dụng Web Demo (sẽ cài đặt ở Tuần 11 bằng Streamlit).
  * Thiết kế luồng tương tác của người dùng (Bác sĩ / Giảng viên):
    * Khung 1: Tải ảnh MRI từ máy tính hoặc chọn nhanh từ 20 ảnh mẫu.
    * Khung 2: Chọn phương pháp phân đoạn (Baseline Watershed hoặc Seeded Region Growing).
    * Khung 3: Hiển thị 4 ảnh song song so sánh trực tiếp: (Ảnh gốc $\rightarrow$ Ảnh sau tách sọ $\rightarrow$ Mặt nạ dự đoán $\rightarrow$ Ảnh khoanh vùng Bounding Box).
    * Khung 4: Bảng hiển thị thông số chẩn đoán (Diện tích u tính bằng pixel, Tỷ lệ % u/não, Độ tròn Circularity, Điểm Dice so với Ground Truth).
* **Sản phẩm bàn giao:** File tài liệu `docs/GUI_WIREFRAME_MOCKUP.md` (vẽ bố cục bằng sơ đồ ASCII hoặc bảng Markdown trực quan).

---

## 📅 3. Lịch Trình Thực Hiện 7 Ngày (Dành Riêng Cho Trí)

| Ngày | Công việc cụ thể | Trạng thái |
| :--- | :--- | :---: |
| **Thứ 2** | Clone repo từ GitHub về máy cá nhân, kiểm tra xem được thư mục `data/sample/`. | [ ] |
| **Thứ 3** | Mở từng ảnh trong `data/sample/`, quan sát vị trí và hình thái các khối u não. | [ ] |
| **Thứ 4** | Soạn thảo xong bản nháp báo cáo khám phá dữ liệu `docs/DATA_EXPLORATION_REPORT.md`. | [ ] |
| **Thứ 5** | Nghiên cứu công thức Dice, IoU, Sensitivity, Specificity và viết ví dụ ma trận $4 \times 4$. | [ ] |
| **Thứ 6** | Hoàn thành tài liệu `docs/THEORY_EVALUATION_METRICS.md`. | [ ] |
| **Thứ 7** | Phác thảo Wireframe bố cục ứng dụng demo vào `docs/GUI_WIREFRAME_MOCKUP.md`. | [ ] |
| **Chủ nhật** | Họp giao ban 15 phút với Trường, tổng kết tuần 1 và sẵn sàng bước sang tuần 2. | [ ] |

---

## ✅ 4. Tiêu Chí Nghiệm Thu (Definition of Done) Của Trí
Trí được coi là hoàn thành xuất sắc Tuần 1 khi đạt đủ 3 tiêu chí sau:
1. File `docs/DATA_EXPLORATION_REPORT.md` được nộp, có đầy đủ bảng phân loại 20 ảnh mẫu.
2. File `docs/THEORY_EVALUATION_METRICS.md` giải thích chính xác 4 công thức toán học và có ví dụ tính tay trực quan.
3. File `docs/GUI_WIREFRAME_MOCKUP.md` mô tả rõ ràng luồng tương tác của giao diện demo.
