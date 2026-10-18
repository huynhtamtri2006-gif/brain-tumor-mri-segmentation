# LỘ TRÌNH 7 NGÀY HOÀN THÀNH 100% ĐỒ ÁN — DÀNH CHO HÀ MẠNH TRƯỜNG
## Thành viên phụ trách: HÀ MẠNH TRƯỜNG (MSSV: 2045240326)
* **Vai trò:** Nhóm trưởng — Chịu trách nhiệm kiến trúc kỹ thuật, Thuật toán Xử lý ảnh số (DIP Core), Pipeline Tách sọ & Phân đoạn u, Phần Kỹ thuật trong Báo cáo.
* **Thời gian hoàn thành:** 07 Ngày liên tục (Chiến dịch Sprint cán đích đồ án).
* **Cam kết độc lập:** Module của Trường làm việc độc lập với Trí thông qua chuẩn giao tiếp ảnh đầu vào/đầu ra ($256 \times 256$, nhị phân `uint8`).

---

## 🗺️ TỔNG QUAN PHÂN CHIA TRÁCH NHIỆM 7 NGÀY (TRƯỜNG)

```
[NGÀY 1] Chốt Spec Kỹ Thuật & Khung Hàm Module Core
    │
[NGÀY 2] Lập trình Module Tách Sọ Não (Skull Stripping: Otsu + Morphology + LCC)
    │
[NGÀY 3] Lập trình Phương pháp Phân đoạn 1: Marker-controlled Watershed
    │
[NGÀY 4] Lập trình Phương pháp Phân đoạn 2: Seeded Region Growing (Đối chứng)
    │
[NGÀY 5] Chạy Phân đoạn trên 20 Mẫu, Xuất Mặt Nạ Dự Đoán & Phân Tích Lỗi (Failure Cases)
    │
[NGÀY 6] Viết Báo cáo Đồ án: Chương Cơ sở Lý thuyết, Tách sọ & Thuật toán Phân đoạn
    │
[NGÀY 7] Soạn Slide Kỹ thuật, Tối ưu hóa Mã nguồn, Đóng gói Trọn bộ Nộp Bài
```

---

## 📋 CHI TIẾT TỪNG NGÀY & CHECKLIST CỦA TRƯỜNG

### 🔹 NGÀY 1: Thiết Lập Dự Án & Đặc Tả Kỹ Thuật Pipeline
* **Nhiệm vụ:**
  * Soạn thảo tài liệu đặc tả kỹ thuật `docs/SPEC_PIPELINE_MRI.md`: Mô tả chi tiết thuật toán tách sọ và 2 phương pháp phân đoạn u não (Watershed & Region Growing).
  * Khởi tạo khung file rỗng trong `src/preprocessing/` và `src/segmentation/` với đầy đủ type hints và docstring.
  * Thống nhất với Trí về chuẩn dữ liệu đầu vào và đầu ra:
    * Đầu vào: Ảnh MRI xám $256 \times 256$ (`uint8`, $[0, 255]$).
    * Đầu ra tách sọ: Ảnh não đã loại bỏ xương sọ (`uint8`, nền đen ngoài não = 0).
    * Đầu ra phân đoạn: Mặt nạ nhị phân u não (`uint8`, u = 255, mô lành = 0).
* **Checklist hoàn thành Ngày 1:**
  - [ ] Nộp xác nhận đề tài trên Classroom.
  - [ ] Hoàn thành `docs/SPEC_PIPELINE_MRI.md`.
  - [ ] Khởi tạo khung mã nguồn skeleton cho pipeline xử lý ảnh.

---

### 🔹 NGÀY 2: Cài Đặt Module Tiền Xử Lý & Tách Sọ Não (Skull Stripping)
* **Nhiệm vụ:**
  * Lập trình file `src/preprocessing/filters.py`:
    * Hàm `apply_bilateral_filter(image)`: Khử nhiễu Rician mà vẫn giữ nguyên độ sắc nét của bờ khối u.
    * Hàm `apply_clahe(image)`: Tăng cường tương phản cục bộ mô mềm não.
  * Lập trình file `src/preprocessing/skull_strip.py`:
    * Bước 1: Ngưỡng hóa nhị phân tự động Otsu để tách phần đầu khỏi nền.
    * Bước 2: Phép toán hình thái học `cv2.morphologyEx` với phép Opening và phần tử cấu trúc dạng đĩa (kernel $5 \times 5$ hoặc $7 \times 7$) để cắt đứt cuống nối giữa màng não và xương sọ.
    * Bước 3: Tìm thành phần liên thông lớn nhất (`cv2.connectedComponentsWithStats`) để giữ lại mặt nạ nhu mô não (Brain Mask).
    * Bước 4: Lấp đầy lỗ hổng não thất (Hole Filling) bằng phép bù nhị phân và `cv2.floodFill`.
    * Bước 5: Phép nhân Bitwise-AND với ảnh gốc để lấy toàn bộ phần não sạch xương sọ.
* **Checklist hoàn thành Ngày 2:**
  - [ ] Chạy thử nghiệm thành công tách sọ trên 20 ảnh mẫu trong `data/sample/images/`.
  - [ ] Lưu kết quả ảnh sau tách sọ vào `data/processed/skull_stripped/`.
  - [ ] Đạt tỷ lệ tách sọ sạch > 90% (không còn dính xương sọ sáng màu).

---

### 🔹 NGÀY 3: Cài Đặt Thuật Toán Phân Đoạn Baseline 1 — Watershed Phân Thủy
* **Nhiệm vụ:**
  * Lập trình file `src/segmentation/watershed.py`:
    * Hàm `segment_tumor_watershed(brain_image)`:
      1. Áp dụng biến đổi khoảng cách Euclidean (`cv2.distanceTransform`) trên vùng não sáng màu để tìm tâm u.
      2. Xác định vùng chắc chắn là u (Sure Foreground) bằng cách lấy ngưỡng từ bản đồ khoảng cách: `sure_fg = dist_transform > 0.4 * max(dist_transform)`.
      3. Xác định vùng chắc chắn là nền não lành (Sure Background) bằng phép Dilation trên mặt nạ.
      4. Tìm vùng chưa xác định (Unknown region) = `sure_bg - sure_fg`.
      5. Gán nhãn các điểm hạt giống đánh dấu (Markers) bằng `cv2.connectedComponents`.
      6. Thực thi giải thuật phân thủy `cv2.watershed(image, markers)`.
      7. Trích xuất mặt nạ u nhị phân (vùng có nhãn u gán giá trị 255).
* **Checklist hoàn thành Ngày 3:**
  - [ ] Hàm `segment_tumor_watershed` chạy ổn định, không bị crash.
  - [ ] Xuất mặt nạ phân đoạn u dự đoán cho 20 ảnh mẫu và lưu vào `data/processed/pred_watershed/`.

---

### 🔹 NGÀY 4: Cài Đặt Thuật Toán Phân Đoạn Phương Án 2 — Seeded Region Growing
* **Nhiệm vụ:**
  * Lập trình file `src/segmentation/region_growing.py`:
    * Hàm `segment_tumor_region_growing(brain_image, tolerance=15)`:
      1. Tự động tìm điểm hạt giống ban đầu (Seed point): Chọn pixel có cường độ sáng lớn nhất nằm trong nhu mô não (do u não trên ảnh T1-CE/FLAIR thường có tín hiệu tăng sáng).
      2. Thuật toán lan truyền láng giềng 8 điểm (8-connectivity):
         * Sử dụng hàng đợi BFS (Breadth-First Search).
         * Kiểm tra điều kiện thu nạp láng giềng: $|I(x, y) - \mu_{\text{region}}| \le \text{tolerance}$.
         * Thu nạp pixel vào vùng u nếu thỏa mãn ngưỡng dung sai.
      3. Hậu xử lý hình thái học: Áp dụng phép Closing nhẹ để làm liền bờ u và lấp lỗ trống nội u.
* **Checklist hoàn thành Ngày 4:**
  - [ ] Hàm `segment_tumor_region_growing` chạy độc lập, tự động tìm seed point mà không cần can thiệp bằng tay.
  - [ ] Xuất mặt nạ phân đoạn u dự đoán cho 20 ảnh mẫu và lưu vào `data/processed/pred_region_growing/`.

---

### 🔹 NGÀY 5: Đánh Giá So Sánh Thực Nghiệm 2 Thuật Toán & Phân Tích Lỗi
* **Nhiệm vụ:**
  * Kết nối với module tính chỉ số của Trí (`src/evaluation/metrics.py`) để chạy đánh giá trên toàn bộ 20 mẫu ảnh cho cả 2 phương pháp:
    * Bảng 1: Điểm Dice, IoU, Sensitivity, Specificity của Watershed.
    * Bảng 2: Điểm Dice, IoU, Sensitivity, Specificity của Region Growing.
  * Phân tích chuyên sâu các ca thành công và ca thất bại (Failure Cases):
    * Phân tích tại sao ca u nhỏ (< 1%) Watershed bị bắt hụt hoặc over-segmentation.
    * Phân tích tại sao Region Growing nhạy cảm với việc chọn điểm seed ban đầu khi có mô xám sáng màu lân cận.
    * Đưa ra kết luận phương pháp nào vượt trội hơn và lý giải nguyên nhân dựa trên lý thuyết xử lý ảnh số.
* **Checklist hoàn thành Ngày 5:**
  - [ ] Xuất bảng so sánh tổng hợp số liệu 2 phương án ra file CSV hoặc Markdown.
  - [ ] Chọn ra 3 ca tiêu biểu (1 ca xuất sắc, 1 ca trung bình, 1 ca thất bại) để đưa vào báo cáo.

---

### 🔹 NGÀY 6: Biên Soạn Báo Cáo Đồ Án (Phần Cơ Sở Lý Thuyết & Kỹ Thuật DIP)
* **Nhiệm vụ:**
  * Phụ trách viết 4 chương trọng tâm về kỹ thuật trong Báo cáo đồ án chuẩn Khoa CNTT:
    1. **Chương 2: Cơ sở lý thuyết Xử lý ảnh số:** Giải thích chi tiết toán học của phép toán hình thái học (Erosion, Dilation, Opening, Closing), biến đổi khoảng cách Distance Transform, giải thuật Watershed và nguyên lý Region Growing. Có hình vẽ minh họa trích từ Gonzalez & Woods.
    2. **Chương 4: Quy trình Tiền xử lý & Tách sọ não (Skull Stripping):** Trình bày chi tiết từng bước tách sọ, hình ảnh minh họa trước/sau tách sọ của các ca bệnh.
    3. **Chương 5: Phương pháp phân đoạn và phát hiện khối u não:** Mô tả sơ đồ khối của 2 phương án Watershed và Region Growing, công thức xác định hạt giống, bảng tham số thực nghiệm.
    4. **Chương 6 (Phần kỹ thuật): Phân tích định tính & Các trường hợp thất bại:** Bình luận nguyên nhân sai lệch và đề xuất cải tiến.
* **Checklist hoàn thành Ngày 6:**
  - [ ] Hoàn tất nội dung 4 chương kỹ thuật trong file Báo cáo đồ án.
  - [ ] Đảm bảo đúng định dạng quy chuẩn văn bản của Khoa CNTT (font chữ, đánh số hình, trích dẫn tài liệu tham khảo chuẩn IEEE).

---

### 🔹 NGÀY 7: Soạn Slide Thuyết Trình Kỹ Thuật, Tối Ưu Code & Đóng Gói
* **Nhiệm vụ:**
  * Soạn phần Slide thuyết trình của mình (khoảng 8–10 slides): Bối cảnh kỹ thuật, Pipeline tách sọ, Thuật toán Watershed vs Region Growing, Kết quả trực quan trước/sau xử lý.
  * Rà soát lại toàn bộ code trong `src/preprocessing` và `src/segmentation`: Thêm docstrings tiếng Việt chuẩn, xóa các biến thừa, đảm bảo chạy mượt không lỗi.
  * Họp tổng duyệt lần cuối cùng Trí, kiểm tra chạy thử toàn bộ demo Streamlit và đóng gói hồ sơ nộp đồ án.
* **Checklist hoàn thành Ngày 7:**
  - [ ] Toàn bộ code xử lý ảnh số chạy trơn tru, có chú thích đầy đủ.
  - [ ] Slide phần kỹ thuật hoàn tất, sẵn sàng thuyết trình bảo vệ trước hội đồng.
