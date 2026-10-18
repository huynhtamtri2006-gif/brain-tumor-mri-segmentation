# LỘ TRÌNH 7 NGÀY HOÀN THÀNH 100% ĐỒ ÁN — DÀNH CHO HUỲNH TÂM TRÍ
## Thành viên phụ trách: HUỲNH TÂM TRÍ (MSSV: 2045240315)
* **Vai trò:** Thành viên — Chịu trách nhiệm Dữ liệu thực nghiệm, Engine đo lường & Đánh giá định lượng (Dice/IoU), Ứng dụng Demo Streamlit GUI, Phần Đánh giá & Báo cáo Tổng quan, Slide thuyết trình.
* **Thời gian hoàn thành:** 07 Ngày liên tục (Chiến dịch Sprint cán đích đồ án).
* **Cam kết độc lập:** Trí làm việc độc lập 100% trên phần dữ liệu, độ đo toán học, giao diện web demo và phần thuyết trình, chỉ cần nhận ảnh dự đoán nhị phân từ module của Trường.

---

## 🗺️ TỔNG QUAN PHÂN CHIA TRÁCH NHIỆM 7 NGÀY (TRÍ)

```
[NGÀY 1] Khảo Sát & Lập Báo Cáo Đặc Tính 20 Mẫu Dữ Liệu TCGA-LGG
    │
[NGÀY 2] Lập trình Engine Tính Bộ Đo Định Lượng (Dice, IoU, Sensitivity, Specificity)
    │
[NGÀY 3] Lập trình Module Rút Trích Đặc Trưng U Não (Diện tích, Tỷ lệ %, Bounding Box, Độ tròn)
    │
[NGÀY 4] Dựng Khung Giao Diện Web Demo Tương Tác Streamlit (Base UI & Tải ảnh)
    │
[NGÀY 5] Hoàn Thiện Full Tính Năng Streamlit GUI: Hiển Thị 4 Bước Trung Gian + Card Chỉ Số
    │
[NGÀY 6] Viết Báo cáo Đồ án: Chương Giới thiệu, Mô tả dữ liệu, Kết quả định lượng & GUI
    │
[NGÀY 7] Thiết Kế Toàn Bộ Slide Thuyết Trình, Quay Video Demo & Đóng Gói Bộ Hồ Sơ Nộp
```

---

## 📋 CHI TIẾT TỪNG NGÀY & CHECKLIST CỦA TRÍ

### 🔹 NGÀY 1: Khảo Sát & Báo Cáo Khám Phá Dữ Liệu Thực Nghiệm (TCGA-LGG)
* **Nhiệm vụ:**
  * Khảo sát toàn bộ 20 cặp ảnh và mặt nạ Ground Truth trong [data/sample/](file:///C:/Users/xpaga/Documents/xlas/data/sample/).
  * Lập file tài liệu `docs/DATA_EXPLORATION_REPORT.md`:
    * Nguồn gốc dữ liệu: Bộ dữ liệu The Cancer Genome Atlas Low-Grade Glioma (TCGA-LGG), nghiên cứu Buda et al. (2019).
    * Phân tích thuộc tính: Ảnh cắt lát cộng hưởng từ sọ não chuỗi xung FLAIR/T1-CE, kích thước $256 \times 256$, định dạng grayscale uint8 $[0, 255]$.
    * Phân nhóm dữ liệu theo độ khó phân đoạn:
      * U nhỏ ($< 1.5\%$ diện tích): Ca 05, 11, 12, 13, 16, 19, 20 (Thách thức lớn về độ nhạy).
      * U trung bình ($1.5\% - 5\%$): Ca 01, 02, 03, 04, 06, 14, 15, 17, 18.
      * U lớn ($> 5\%$): Ca 07, 08, 09, 10 (U lan tỏa, hiệu ứng khối đè đẩy).
    * Đánh giá độ tương phản: U tăng tín hiệu sáng rõ hay u bờ mờ.
* **Checklist hoàn thành Ngày 1:**
  - [ ] Hoàn thành tài liệu `docs/DATA_EXPLORATION_REPORT.md`.
  - [ ] Kiểm tra tính toàn vẹn của 20 ảnh và 20 mặt nạ (không có file nào bị lỗi mở).

---

### 🔹 NGÀY 2: Cài Đặt Engine Đánh Giá Định Lượng (Quantitative Evaluation Engine)
* **Nhiệm vụ:**
  * Lập trình file `src/evaluation/metrics.py`:
    * Hàm `calculate_dice_score(pred_mask, gt_mask)`:
      $$\text{Dice} = \frac{2 \cdot \text{TP}}{2 \cdot \text{TP} + \text{FP} + \text{FN}}$$
    * Hàm `calculate_iou(pred_mask, gt_mask)`:
      $$\text{IoU} = \frac{\text{TP}}{\text{TP} + \text{FP} + \text{FN}}$$
    * Hàm `calculate_sensitivity(pred_mask, gt_mask)`:
      $$\text{Sensitivity} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
    * Hàm `calculate_specificity(pred_mask, gt_mask)`:
      $$\text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}$$
    * Hàm `evaluate_batch(pred_masks_dir, gt_masks_dir)`: Tự động quét toàn bộ thư mục, so sánh từng cặp ảnh và xuất bảng thống kê trung bình (Mean $\pm$ Std) cùng độ trễ xử lý (Latency ms).
  * Viết tài liệu giải thích công thức `docs/THEORY_EVALUATION_METRICS.md` kèm bảng tính ví dụ tay $4 \times 4$.
* **Checklist hoàn thành Ngày 2:**
  - [ ] File `src/evaluation/metrics.py` chạy độc lập, có thể test thử với 2 mặt nạ bất kỳ trong `data/sample/masks/`.
  - [ ] Bổ sung cơ chế xử lý ngoại lệ chia cho 0 khi cả hai mặt nạ đều rỗng (Dice = 1.0).

---

### 🔹 NGÀY 3: Cài Đặt Module Đo Lường & Rút Trích Đặc Trưng Khối U (Feature Extraction)
* **Nhiệm vụ:**
  * Lập trình file `src/measurement/features.py`:
    * Hàm `measure_tumor_properties(tumor_mask, brain_mask=None)`:
      1. Tìm đường bao khối u (`cv2.findContours` với cờ `RETR_EXTERNAL`).
      2. Tính diện tích u: $S_{\text{tumor}} = \sum \text{pixel}$ (hoặc `cv2.contourArea`).
      3. Tính chu vi u: $P_{\text{tumor}} = \text{cv2.arcLength(contour, True)}$.
      4. Tính độ tròn (Circularity / Compactness):
         $$C = \frac{4 \pi \cdot \text{Area}}{\text{Perimeter}^2}$$
         *(Nếu $C \approx 1$: khối u tròn đều, thường là u màng não lành tính Meningioma; nếu $C \ll 1$: bờ u gồ ghề, xâm lấn, thường là u thần kinh đệm ác tính Glioma)*.
      5. Tính tỷ lệ chiếm chỗ: $\text{Ratio} = \frac{S_{\text{tumor}}}{S_{\text{brain}}} \times 100\%$.
    * Hàm `draw_tumor_bounding_box(original_image, tumor_mask)`:
      * Trích xuất tọa độ $(x, y, w, h) = \text{cv2.boundingRect(contour)}$.
      * Vẽ hình chữ nhật màu đỏ cảnh báo (`color=(0, 0, 255)`, nét vẽ $2\text{px}$) quanh vùng u.
      * Thêm nhãn text: `"Tumor: Area = ... px, Circ = ..."`.
* **Checklist hoàn thành Ngày 3:**
  - [ ] Chạy thử nghiệm trích xuất đặc trưng và vẽ Bounding Box trên toàn bộ 20 mặt nạ Ground Truth.
  - [ ] Xuất ảnh minh họa u khoanh vùng lưu tại `data/processed/annotated_samples/`.

---

### 🔹 NGÀY 4: Xây Dựng Khung Giao Diện Web Demo (Streamlit Base UI)
* **Nhiệm vụ:**
  * Lập trình file `demo/app.py` bằng thư viện Streamlit (`streamlit run demo/app.py`):
    * Sidebar:
      * Logo và thông tin đề tài: Bộ môn Khoa học Dữ liệu — HUIT.
      * Tên 2 sinh viên thực hiện: Hà Mạnh Trường & Huỳnh Tâm Trí.
      * Chế độ nạp ảnh: Cho phép người dùng "Tải ảnh từ máy tính (.png, .jpg)" HOẶC "Chọn nhanh trong 20 ca bệnh mẫu TCGA-LGG".
      * Hộp chọn thuật toán (Dropdown): "Phương án A: Marker-controlled Watershed" hoặc "Phương án B: Seeded Region Growing".
    * Main Area:
      * Tiêu đề chuyên nghiệp: "Hệ Thống Phân Đoạn & Phát Hiện Khối U Não MRI".
      * Bố cục 2 cột ban đầu: Cột 1 hiển thị Ảnh MRI Gốc, Cột 2 hiển thị Thông tin ca chụp.
* **Checklist hoàn thành Ngày 4:**
  - [ ] Khởi chạy giao diện thử nghiệm: `streamlit run demo/app.py` mở được trên trình duyệt (`http://localhost:8501`).
  - [ ] Chức năng tải ảnh và chọn ca mẫu hoạt động mượt mà.

---

### 🔹 NGÀY 5: Tích Hợp Toàn Diện Pipeline & Hoàn Thiện GUI Demo
* **Nhiệm vụ:**
  * Tích hợp toàn bộ các module của Trường và Trí vào `demo/app.py`:
    * Khi người dùng nhấn nút **"Tiến Hành Chẩn Đoán & Phân Đoạn"**:
      * Gọi `apply_bilateral_filter` + `apply_skull_stripping` (từ module của Trường).
      * Gọi thuật toán phân đoạn đã chọn (Watershed hoặc Region Growing).
      * Gọi `measure_tumor_properties` + `draw_tumor_bounding_box` (từ module của Trí).
      * Nếu có Ground Truth, gọi `calculate_dice_score` + `calculate_iou`.
    * Trực quan hóa kết quả theo lưới 4 ảnh song song:
      * `[Ảnh MRI Gốc]` $\rightarrow$ `[Ảnh Sau Tách Sọ Não]` $\rightarrow$ `[Mặt Nạ Phân Đoạn U]` $\rightarrow$ `[Ảnh Khoanh Vùng Bounding Box Đỏ]`.
    * Hiển thị bảng số liệu chẩn đoán (Diagnostic Dashboard):
      * Thẻ KPI nổi bật: Diện tích u, Tỷ lệ % u/não, Độ tròn u, Điểm Dice Score, Thời gian xử lý (ms).
    * Bổ sung nút **"Tải Báo Cáo Chẩn Đoán (.png / .txt)"**.
* **Checklist hoàn thành Ngày 5:**
  - [ ] Ứng dụng chạy hoàn chỉnh, không phát sinh lỗi ngoại lệ khi nạp bất kỳ ảnh nào trong 20 mẫu.
  - [ ] Giao diện trực quan, chuyên nghiệp, gây ấn tượng mạnh với người chấm.

---

### 🔹 NGÀY 6: Biên Soạn Báo Cáo Đồ Án (Phần Giới Thiệu, Dữ Liệu & Đánh Giá)
* **Nhiệm vụ:**
  * Phụ trách viết 5 chương quan trọng trong Báo cáo đồ án chuẩn Khoa CNTT:
    1. **Chương 1: Giới thiệu đề tài:** Tính cấp thiết của chẩn đoán u não, vai trò của ảnh cộng hưởng từ MRI, mục tiêu và phạm vi đề tài.
    2. **Chương 3: Mô tả và Phân tích Dữ liệu:** Thuyết minh bộ dữ liệu TCGA-LGG, bảng thống kê 20 mẫu ảnh, các biểu đồ phân bố kích thước u.
    3. **Chương 6 (Phần định lượng): Kết quả Thực nghiệm & Đánh giá:** Lập bảng so sánh chi tiết điểm Dice, IoU, Sensitivity, Specificity và thời gian chạy của cả 2 phương pháp. Vẽ biểu đồ so sánh.
    4. **Chương 7: Chương trình Ứng dụng Demo (GUI):** Giới thiệu chức năng, chụp các màn hình giao diện Streamlit khi phân đoạn thực tế các ca bệnh, hướng dẫn thao tác.
    5. **Chương 8: Kết luận & Hướng phát triển:** Tóm tắt các kết quả đạt được, đóng góp của nhóm, các hạn chế còn tồn tại và hướng nâng cấp tiếp theo.
* **Checklist hoàn thành Ngày 6:**
  - [ ] Hoàn tất nội dung 5 chương trong file Báo cáo đồ án.
  - [ ] Ghép nối với các chương kỹ thuật của Trường thành một file Báo cáo duy nhất hoàn chỉnh.

---

### 🔹 NGÀY 7: Thiết Kế Slide Thuyết Trình, Quay Video Demo & Đóng Gói
* **Nhiệm vụ:**
  * Thiết kế toàn bộ Slide thuyết trình (PowerPoint hoặc Canva, khoảng 15–18 slides) chuẩn nhận diện Khoa CNTT: Bìa đề tài, Đặt vấn đề, Pipeline hệ thống, Minh họa tách sọ, Minh họa phân đoạn u, Bảng so sánh định lượng, Giới thiệu GUI Demo, Kết luận.
  * Quay video ngắn (khoảng 2–3 phút) ghi lại màn hình chạy demo Streamlit trên 2–3 ca bệnh khác nhau để làm minh chứng nộp kèm.
  * Kiểm tra trọn bộ sản phẩm nộp theo yêu cầu của Bộ môn:
    * Thư mục `src/` sạch sẽ, chạy được.
    * Thư mục `data/sample/` đầy đủ.
    * Thư mục `demo/` khởi chạy ổn định.
    * File Báo cáo `.pdf` và `.docx`.
    * File Slide `.pdf` và `.pptx`.
    * Link video demo.
  * Nén toàn bộ thành file nộp đồ án chuẩn.
* **Checklist hoàn thành Ngày 7:**
  - [ ] Slide thuyết trình hoàn tất, đẹp mắt, mạch lạc.
  - [ ] Trọn bộ hồ sơ đồ án sẵn sàng nộp đúng hạn.
