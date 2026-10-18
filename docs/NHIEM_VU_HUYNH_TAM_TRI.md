# LỘ TRÌNH 7 NGÀY HOÀN THÀNH ĐỒ ÁN — HUỲNH TÂM TRÍ
## Thành viên phụ trách: HUỲNH TÂM TRÍ (MSSV: 2045240315)
* **Vai trò:** Thành viên — Chịu trách nhiệm Dữ liệu thực nghiệm, Engine đo lường & Rút trích đặc trưng hình học, Bộ đo định lượng y khoa, Ứng dụng Streamlit GUI, 5 Chương Tổng quan trong Báo cáo, Slide thuyết trình & Video demo.
* **Thời gian thực hiện:** Chiến dịch 7 ngày liên tục.
* **Phạm vi file phụ trách chính:**
  * `data/README.md` & `data/sample/metadata.csv`
  * `src/measurement/features.py` & `src/measurement/visualization.py`
  * `src/evaluation/metrics.py` & `src/evaluation/benchmark.py`
  * `demo/app.py` & `demo/utils.py` (Giao diện Streamlit)
  * `notebooks/01_data_exploration.ipynb` & `notebooks/04_quantitative_evaluation.ipynb`
  * `tests/test_measurement.py` & `tests/test_metrics.py`
  * `docs/DATA_EXPLORATION_REPORT.md` & `docs/THEORY_EVALUATION_METRICS.md`

---

## 🗺️ TỔNG QUAN PHÂN CHIA TRÁCH NHIỆM 7 NGÀY (TRÍ)

```
[NGÀY 1] Khảo Sát 20 Mẫu TCGA-LGG + Hoàn Thiện Notebook 01_data_exploration.ipynb
    │
[NGÀY 2] Tinh Chỉnh Engine Đo Định Lượng (Dice, IoU, Sens, Spec) + Unit Test Metrics
    │
[NGÀY 3] Hoàn Thiện Module Đo Đặc Trưng Hình Học (Circularity, Bounding Box) + Unit Test
    │
[NGÀY 4] Hoàn Thiện Giao Diện Web Demo Streamlit (demo/app.py) & Kiểm Thử Tương Tác
    │
[NGÀY 5] Chạy Batch Benchmark 20 Mẫu + Hoàn Thiện Notebook 04_quantitative_evaluation
    │
[NGÀY 6] Viết Báo Cáo Đồ Án: 5 Chương Tổng Quan (Chương 1, 3, 6 Số Liệu, 7 GUI, 8)
    │
[NGÀY 7] Thiết Kế Bộ Slide Thuyết Trình, Quay Video Demo 2 Phút & Đóng Gói Hồ Sơ Nộp
```

---

## 📋 CHI TIẾT TỪNG NGÀY & CHECKLIST CỦA TRÍ

### 🔹 NGÀY 1: Khảo Sát Dữ Liệu TCGA-LGG & Hoàn Thiện Notebook 01
* **Nhiệm vụ cụ thể:**
  1. Kiểm tra tính toàn vẹn của 20 cặp ảnh MRI và mặt nạ Ground Truth trong `data/sample/images/` và `data/sample/masks/`.
  2. Mở và chạy toàn bộ notebook `notebooks/01_data_exploration.ipynb`:
     * Đọc `data/sample/metadata.csv`, vẽ biểu đồ phân bố diện tích khối u (Histogram).
     * Trực quan hóa lưới $2 \times 6$ ảnh MRI gốc và mặt nạ Ground Truth.
     * Thống kê các chỉ số mô tả: Min, Max, Mean, Median của diện tích u và tỷ lệ % u/não.
  3. Xuất tài liệu báo cáo khám phá dữ liệu `docs/DATA_EXPLORATION_REPORT.md` có đầy đủ bảng số liệu chi tiết của 20 mẫu.
* **Lệnh kiểm tra:** `python -c "import pandas as pd; df=pd.read_csv('data/sample/metadata.csv'); print(df.describe())"`
* **Checklist hoàn thành Ngày 1:**
  - [ ] Chạy thành công `notebooks/01_data_exploration.ipynb` không phát sinh lỗi.
  - [ ] Hoàn thành tài liệu `docs/DATA_EXPLORATION_REPORT.md`.
  - [ ] Lưu các biểu đồ phân bố kích thước u để đưa vào Chương 3 của Báo cáo.

---

### 🔹 NGÀY 2: Tinh Chỉnh Engine Đo Định Lượng Y Khoa & Unit Test Metrics
* **Nhiệm vụ cụ thể:**
  1. Rà soát và hoàn thiện mã nguồn tính toán 4 chỉ số trong `src/evaluation/metrics.py`:
     * Dice Similarity Coefficient: $DSC = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$.
     * Jaccard Index (IoU): $IoU = \frac{TP}{TP + FP + FN}$.
     * Sensitivity (Độ nhạy): $Sens = \frac{TP}{TP + FN}$.
     * Specificity (Độ đặc hiệu): $Spec = \frac{TN}{TN + FP}$.
     * Xử lý ngoại lệ an toàn khi mặt nạ hoàn toàn rỗng ($0 / 0$).
  2. Chạy kiểm thử tự động bộ đo y khoa: `pytest tests/test_metrics.py -v`.
  3. Viết tài liệu cơ sở lý thuyết bộ đo `docs/THEORY_EVALUATION_METRICS.md` kèm bảng tính số học ví dụ tay trên ma trận nhỏ $4 \times 4$.
* **Lệnh kiểm tra:** `pytest tests/test_metrics.py -v`
* **Checklist hoàn thành Ngày 2:**
  - [ ] 100% test trong `test_metrics.py` đều đạt (PASSED).
  - [ ] Hoàn thành tài liệu `docs/THEORY_EVALUATION_METRICS.md`.
  - [ ] Chuẩn bị sẵn phần cơ sở lý thuyết độ đo cho Báo cáo.

---

### 🔹 NGÀY 3: Hoàn Thiện Module Đo Đặc Trưng Hình Học & Vẽ Bounding Box
* **Nhiệm vụ cụ thể:**
  1. Tinh chỉnh các hàm đo lường trong `src/measurement/features.py`:
     * Hàm `calculate_circularity()`: Tính độ tròn $C = \frac{4\pi \cdot \text{Area}}{\text{Perimeter}^2}$, giải thích ý nghĩa y khoa về hình thái bờ u lành tính/ác tính.
     * Hàm `extract_tumor_features()`: Trích xuất tọa độ Bounding Box `(x, y, w, h)`, diện tích u, tỷ lệ % u/não đóng gói vào dataclass `DiagnosticResult`.
  2. Tinh chỉnh module trực quan hóa trong `src/measurement/visualization.py`:
     * Hàm `draw_tumor_overlay()`: Vẽ Bounding Box màu đỏ cảnh báo (`color=(0, 0, 255)`) và viền u màu vàng.
     * Hàm `create_comparison_quad()`: Ghép lưới 4 ảnh song song $[Gốc \mid Tách sọ \mid Mặt nạ \mid Bounding Box]$.
  3. Chạy kiểm thử tự động: `pytest tests/test_measurement.py -v`.
* **Lệnh kiểm tra:** `pytest tests/test_measurement.py -v`
* **Checklist hoàn thành Ngày 3:**
  - [ ] 100% test trong `test_measurement.py` đều đạt (PASSED).
  - [ ] Thử nghiệm vẽ Bounding Box thành công trên 20 ảnh mẫu, không bị lệch tọa độ.

---

### 🔹 NGÀY 4: Hoàn Thiện Ứng Dụng Web Demo Streamlit (`demo/app.py`)
* **Nhiệm vụ cụ thể:**
  1. Hoàn thiện toàn bộ tính năng của giao diện Web Demo trong `demo/app.py`:
     * Thanh Sidebar: Logo trường, thông tin 2 sinh viên, chế độ chọn nhanh 20 ảnh mẫu hoặc tải ảnh tùy ý, chọn thuật toán (Watershed vs Region Growing), thanh trượt điều chỉnh siêu tham số.
     * Main Area: Hiển thị 5 thẻ KPI chẩn đoán nổi bật (Trạng thái u, Diện tích px, Tỷ lệ %, Độ tròn, Điểm Dice).
     * Lưới hiển thị trực quan 4 bước xử lý trung gian song song.
     * Khung so sánh trực tiếp mặt nạ dự đoán với Ground Truth của chuyên gia.
  2. Chạy thử nghiệm ứng dụng: `streamlit run demo/app.py`.
  3. Kiểm tra tính ổn định: Thử lần lượt với tất cả 20 ảnh mẫu và tải thử một số ảnh bên ngoài, đảm bảo không bị crash giao diện.
* **Lệnh kiểm tra:** `streamlit run demo/app.py`
* **Checklist hoàn thành Ngày 4:**
  - [ ] Giao diện Web chạy mượt mà, phản hồi tức thì dưới 1 giây.
  - [ ] Chụp lại 4 ảnh màn hình giao diện demo sắc nét để chuẩn bị đưa vào Chương 7 của Báo cáo.

---

### 🔹 NGÀY 5: Thực Thi Benchmark 20 Mẫu & Hoàn Thiện Notebook 04
* **Nhiệm vụ cụ thể:**
  1. Mở và chạy toàn bộ notebook `notebooks/04_quantitative_evaluation.ipynb`:
     * Chạy module `src/evaluation/benchmark.py` trên 20 mẫu ảnh cho cả 2 phương pháp Watershed và Region Growing.
     * Tính toán bảng tổng hợp giá trị trung bình (Mean $\pm$ Std) của cả 4 chỉ số: Dice, IoU, Sensitivity, Specificity, và thời gian chạy trung bình (Latency ms/ảnh).
     * Vẽ biểu đồ cột (Bar chart) so sánh trực quan điểm Dice của từng ca bệnh giữa 2 phương pháp.
  2. Xuất bảng số liệu so sánh chi tiết ra file `docs/BENCHMARK_RESULTS.csv` hoặc bảng Markdown.
* **Lệnh kiểm tra:** `python -c "from src.evaluation.benchmark import run_benchmark; print('Benchmark module OK')"`
* **Checklist hoàn thành Ngày 5:**
  - [ ] Chạy thành công toàn bộ `notebooks/04_quantitative_evaluation.ipynb`.
  - [ ] Xuất bảng kết quả thực nghiệm hoàn chỉnh, có đầy đủ độ lệch chuẩn.
  - [ ] Lưu biểu đồ so sánh độ phân giải cao phục vụ chèn vào Chương 6 của Báo cáo.

---

### 🔹 NGÀY 6: Biên Soạn Báo Cáo Đồ Án (5 Chương Tổng Quan & Định Lượng)
* **Nhiệm vụ cụ thể:**
  * Chịu trách nhiệm viết 5 chương quan trọng trong Báo cáo đồ án chuẩn Khoa CNTT (Word/PDF):
    1. **Trang bìa & Mục lục:** Chuẩn hóa thông tin đề tài, giảng viên hướng dẫn, thông tin 2 thành viên, mục lục tự động, danh mục hình ảnh và bảng biểu.
    2. **Mục 1: Giới thiệu đề tài:** Tính cấp thiết của chẩn đoán khối u não trên ảnh cộng hưởng từ MRI, mục tiêu hệ thống (đầu vào ảnh xám, đầu ra mặt nạ và thông số chẩn đoán), phạm vi bài toán.
    3. **Mục 3: Mô tả tập dữ liệu:** Thuyết minh chi tiết bộ dữ liệu benchmark quốc tế TCGA-LGG (Buda et al. 2019), bảng metadata 20 mẫu ảnh, biểu đồ phân bố kích thước u trích từ Notebook 01.
    4. **Mục 6 (Phần định lượng): Bảng số liệu & Biểu đồ đánh giá:** Trình bày bảng so sánh Mean $\pm$ Std của Dice/IoU/Latency trích từ Notebook 04, biểu đồ so sánh cột giữa Watershed và Region Growing.
    5. **Mục 7: Chương trình minh họa (Demo GUI):** Giới thiệu kiến trúc ứng dụng Streamlit, hướng dẫn chạy `streamlit run demo/app.py`, chèn các ảnh chụp màn hình thao tác thực tế.
    6. **Mục 8: Kết luận & Hướng phát triển:** Tóm tắt kết quả đạt được, đóng góp của nhóm, hạn chế còn tồn tại và hướng nâng cấp tiếp theo.
* **Checklist hoàn thành Ngày 6:**
  * [ ] Hoàn tất nội dung 5 chương tổng quan.
  * [ ] Ghép nối với 4 chương kỹ thuật của Trường thành một bản Báo cáo duy nhất, kiểm tra lỗi chính tả và định dạng.

---

### 🔹 NGÀY 7: Thiết Kế Slide Thuyết Trình, Quay Video Demo & Đóng Gói
* **Nhiệm vụ cụ thể:**
  1. Thiết kế toàn bộ bộ Slide thuyết trình (PowerPoint / Canva, khoảng 15–18 slides) theo chuẩn nhận diện Khoa CNTT:
     * Slide 1: Bìa đề tài và thành viên nhóm.
     * Slide 2–3: Đặt vấn đề và mục tiêu đồ án.
     * Slide 4: Bộ dữ liệu thực nghiệm TCGA-LGG.
     * Slide 5: Sơ đồ kiến trúc pipeline 4 tầng.
     * Slide 6–9: Kỹ thuật tách sọ và 2 thuật toán phân đoạn (Trường hỗ trợ nội dung).
     * Slide 10–12: Bảng kết quả định lượng (Dice, IoU, Latency) và biểu đồ so sánh.
     * Slide 13–15: Giới thiệu ứng dụng Streamlit GUI (hình ảnh trực quan).
     * Slide 16: Kết luận và bài học kinh nghiệm.
  2. Quay video clip ngắn (khoảng 2–3 phút) ghi lại màn hình thao tác trực tiếp trên giao diện Streamlit: Nạp ảnh mẫu, chọn Watershed, quan sát ảnh tách sọ và Bounding Box, thay đổi sang Region Growing.
  3. Kiểm tra toàn bộ hồ sơ nộp đồ án: File Báo cáo (Word + PDF), Slide (PPTX + PDF), Video demo, Mã nguồn `src/` và `notebooks/`, đóng gói thành file ZIP hoàn chỉnh.
* **Checklist hoàn thành Ngày 7:**
  - [ ] Slide thuyết trình hoàn tất, thiết kế chuyên nghiệp và ấn tượng.
  - [ ] Video demo chạy mượt mà, âm thanh/thuyết minh rõ ràng.
  - [ ] Bộ hồ sơ đồ án đóng gói sẵn sàng nộp đúng hạn.
