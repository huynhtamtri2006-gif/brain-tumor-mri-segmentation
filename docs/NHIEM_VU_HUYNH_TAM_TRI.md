# KẾ HOẠCH & PHÂN CÔNG NHIỆM VỤ CẤP TỐC 7 NGÀY — HUỲNH TÂM TRÍ
### Học phần: Xử lý ảnh số (0101006276) — Học kỳ 2026–2027
**Đơn vị:** Bộ môn Khoa học Dữ liệu — Khoa Công nghệ Thông tin — Trường ĐH Công Thương TP.HCM (HUIT)  
**Đề tài:** Phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ MRI (TCGA-LGG Benchmark)

---

## 👤 THÔNG TIN SINH VIÊN
* **Họ và tên:** **HUỲNH TÂM TRÍ**
* **Mã số sinh viên:** **2045240315**
* **Lớp sinh hoạt:** 15DHKHDL03
* **Vai trò:** **Thành viên**
* **Trách nhiệm trọng tâm:**
  * Thu thập, cấu trúc hóa dữ liệu ảnh MRI toàn bộ 3,929 lát cắt chuẩn quốc tế TCGA-LGG (`data/full/`).
  * Nghiên cứu cơ sở toán học và cài đặt hệ thống chỉ số đánh giá y sinh chuẩn mực (Dice Score, IoU Jaccard, Sensitivity, Specificity).
  * Cài đặt module Rút trích đặc trưng hình học khối u (Diện tích u, Tỷ lệ u/não, Độ tròn bờ u Circularity, Bounding Box cảnh báo đỏ).
  * Xây dựng và hoàn thiện ứng dụng web tương tác minh họa (Streamlit GUI) hỗ trợ chế độ Dual-mode dữ liệu.
  * Chạy thực nghiệm định lượng quy mô lớn (3,929 lát cắt) qua framework xử lý đa tiến trình và hoàn thiện Notebook 01, 04.
  * Soạn thảo các chương tổng quan & định lượng trong Báo cáo (Chương 1, 3, 5, 8 số liệu, 9 GUI, 10 kết luận).
  * Thiết kế Slide thuyết trình bảo vệ cuối kỳ 20 trang và quay Video clip demo hệ thống 3 phút.

---

## 🎯 ĐỐI CHIẾU VỚI RUBRIC ĐÁNH GIÁ ĐỒ ÁN MÔN HỌC (KHOA CNTT - HUIT)

Đồ án được chấm theo thang điểm 10 theo đúng Mục III trong `9. Ke_hoach_thuc_ĐA__XLAS_2026-2027.pdf`:

| Tiêu chí đánh giá | Trọng số | Đóng góp và minh chứng chính của Huỳnh Tâm Trí |
| :--- | :---: | :--- |
| **1. Phân tích & lựa chọn đúng phương pháp (PLO2, CLO1)** | **15% (1.5đ)** | - Khảo sát các bộ độ tương đồng y khoa chuẩn quốc tế (Dice Similarity Coefficient, Jaccard Index).<br>- Lựa chọn các đặc trưng hình học (Area, Perimeter, Circularity) phản ánh độ gồ ghề bờ u theo góc nhìn chẩn đoán lâm sàng. |
| **2. Áp dụng được các phương pháp xử lý (PLO2, CLO2)** *(Trọng tâm)* | **50% (5.0đ)** | - Chuẩn hóa kho dữ liệu toàn bộ 3,929 lát cắt chuẩn quốc tế TCGA-LGG (`data/full/`).<br>- Cài đặt module `src/evaluation/metrics.py` và `src/measurement/features.py`.<br>- Xây dựng ứng dụng Web tương tác Streamlit GUI (`demo/app.py`).<br>- Chạy thực nghiệm định lượng toàn diện trên 3,929 lát cắt và xuất báo cáo CSV chi tiết.<br>- Đạt 100% test cases trong `tests/test_metrics.py` và `tests/test_measurement.py`. |
| **3. Đọc tài liệu, nghiên cứu giải quyết bài toán (PLO4, CLO3)** | **10% (1.0đ)** | - Nghiên cứu bài báo gốc của Buda et al. (2019) công bố trên tạp chí *Computers in Biology and Medicine* về bộ dữ liệu TCGA-LGG.<br>- Soạn thảo tài liệu phân tích dữ liệu chuyên sâu [DATA_EXPLORATION_REPORT.md](file:///C:/Users/xpaga/Documents/xlas/docs/DATA_EXPLORATION_REPORT.md). |
| **4. Trình bày báo cáo (PLO7, CLO5)** | **15% (1.5đ)** | - Biên soạn các chương tổng quan, dữ liệu, bảng số liệu định lượng, giới thiệu GUI và kết luận.<br>- Chuẩn hóa bảng biểu, biểu đồ phân bố và hình ảnh chụp giao diện Streamlit rõ nét. |
| **5. Phân công & phối hợp làm việc nhóm (PLO6, CLO4)** | **10% (1.0đ)** | - Phối hợp chặt chẽ với Nhóm trưởng Trường trong suốt Sprint 7 ngày theo đúng kế hoạch.<br>- Phụ trách toàn bộ khâu thiết kế Slide thuyết trình chuyên nghiệp và video clip minh họa hệ thống. |

---

## 🗺️ LỘ TRÌNH SPRINT CẤP TỐC 7 NGÀY CỦA HUỲNH TÂM TRÍ

```
[Ngày 1] Tiếp nhận Kế hoạch Sprint, Thu thập & Chuẩn hóa Dữ liệu TCGA-LGG (3,929 lát) + Notebook 01 EDA
   │
[Ngày 2] Cài đặt Module Chỉ số Đánh giá Y sinh (Dice, IoU, Sens, Spec) + Unit Tests (test_metrics.py)
   │
[Ngày 3] Cài đặt Module Rút trích Đặc trưng Hình học (Area, Circularity) & Trực quan hóa Bounding Box
   │
[Ngày 4] Hoàn thiện Notebook 03 (So sánh Phân đoạn) & Xây dựng Framework Benchmark Tự động
   │
[Ngày 5] Hoàn thiện Web Demo Streamlit GUI, Thực thi Benchmark 3,929 Lát Cắt & Notebook 04 Đánh giá
   │
[Ngày 6] Biên soạn Báo cáo Đồ án Toàn văn (6 Chương Tổng quan & Định lượng), Xuất Báo Cáo Word Chuẩn HUIT
   │
[Ngày 7] Thiết kế Bộ Slide Thuyết trình 20 Trang, Quay Video Demo 3 Phút & Đóng gói Hồ sơ Đồ án
   │
[Nghiệm thu] PHỐI HỢP CÙNG NHÓM TRƯỞNG BẢO VỆ ĐỒ ÁN TRƯỚC HỘI ĐỒNG CHẤM THI
```

---

## 📋 NỘI DUNG THỰC HIỆN CHI TIẾT TỪNG NGÀY

### 🔹 NGÀY 1: Tiếp Nhận Sprint, Thu Thập & Chuẩn Hóa Dữ Liệu TCGA-LGG (3,929 Lát Cắt)
* **Mục tiêu:** Thiết lập kho dữ liệu thực nghiệm TCGA-LGG chuẩn mực, kiểm tra tính hợp lệ của mặt nạ nhãn chuyên gia, và hoàn thành báo cáo khám phá dữ liệu ban đầu.
* **Nhiệm vụ cụ thể:**
  1. Họp cùng Nhóm trưởng Trường: Tiếp nhận bản kế hoạch Sprint cấp tốc 7 ngày, thống nhất giao diện dữ liệu đầu vào.
  2. Thu thập và chuẩn hóa bộ dữ liệu nghiên cứu chuẩn The Cancer Genome Atlas Low-Grade Glioma (TCGA-LGG) gồm 3,929 lát cắt MRI từ 110 bệnh nhân:
     * Kho dữ liệu `data/full/`: 3,929 lát cắt MRI chuẩn hóa từ 110 bệnh nhân.
     * Tầng 2 (`data/full/`): Toàn bộ 3,929 lát cắt chuẩn (tải tự động qua `python scripts/download_full_dataset.py`).
  3. Kiểm tra tính hợp lệ của dữ liệu: Đảm bảo ảnh gốc là định dạng chuẩn $256 \times 256$, mặt nạ Ground Truth chỉ chứa giá trị nhị phân $\{0, 255\}$.
  4. Xây dựng và chạy hoàn thiện `notebooks/01_data_exploration.ipynb`:
     * Thống kê kích thước khối u: Diện tích nhỏ nhất (7 px), lớn nhất (7,929 px), trung vị (1,529 px), trung bình (1,931 px).
     * Phân nhóm 3 dải diện tích: U nhỏ (< 1.5%), U trung bình (1.5%–5%), U lớn (> 5% diện tích não).
     * Xuất tài liệu thống kê chuyên sâu `docs/DATA_EXPLORATION_REPORT.md`.
* **Lệnh kiểm tra:** `python -c "import os; print('Sample images:', len(os.listdir('data/full/images')))"`
* **Tiêu chí nghiệm thu & Checklist:**
  - [x] Kho dữ liệu thực nghiệm TCGA-LGG được chuẩn hóa.
  - [x] Chạy hoàn thiện `notebooks/01_data_exploration.ipynb`.
  - [x] Hoàn tất tài liệu phân tích dữ liệu `docs/DATA_EXPLORATION_REPORT.md`.

---

### 🔹 NGÀY 2: Cài Đặt Module Chỉ Số Đánh Giá Y Sinh & Unit Tests
* **Mục tiêu:** Hiện thực hóa các công thức toán học đo lường độ trùng khớp y tế giữa mặt nạ phân đoạn và Ground Truth.
* **Nhiệm vụ cụ thể:**
  1. Cài đặt module `src/evaluation/metrics.py`:
     * Chỉ số tương đồng Dice (Dice Similarity Coefficient / F1-score):
       $$DSC = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$$
     * Chỉ số Jaccard (Intersection over Union - IoU):
       $$IoU = \frac{TP}{TP + FP + FN}$$
     * Độ nhạy (Sensitivity / Recall - Tỷ lệ phát hiện đúng mô bệnh lý):
       $$Sens = \frac{TP}{TP + FN}$$
     * Độ đặc hiệu (Specificity - Tỷ lệ nhận diện đúng mô lành):
       $$Spec = \frac{TN}{TN + FP}$$
  2. Xử lý an toàn các ca biên (Edge cases): Khi cả Ground Truth và dự đoán đều là lát não lành không chứa u ($0/0$), hàm trả về giá trị an toàn ($Dice = 1.0, Sens = 1.0$) mà không gây lỗi chia cho 0.
  3. Viết unit tests kiểm thử tính chính xác số học: `tests/test_metrics.py` (kiểm tra ma trận giả định $4 \times 4$, trường hợp trùng khớp 100%, sai lệch hoàn toàn, và ca âm tính).
  4. Chạy kiểm thử tự động: `pytest tests/test_metrics.py -v`.
* **Lệnh kiểm tra:** `pytest tests/test_metrics.py -v`
* **Tiêu chí nghiệm thu & Checklist:**
  - [x] 100% test cases trong `test_metrics.py` đạt kết quả PASSED.
  - [x] Bắt lỗi số học an toàn, không có hiện tượng ngoại lệ `ZeroDivisionError`.
  - [x] Các hàm trả về kiểu dữ liệu float chuẩn xác trong khoảng $[0.0, 1.0]$.


---

### 🔹 NGÀY 3: Cài Đặt Module Đo Đặc Trưng Hình Học & Vẽ Bounding Box
* **Mục tiêu:** Trích xuất các tham số định lượng hình học khối u có ý nghĩa hỗ trợ chẩn đoán lâm sàng và trực quan hóa cảnh báo.
* **Nhiệm vụ cụ thể:**
  1. Cài đặt các hàm đo lường trong `src/measurement/features.py`:
     * Hàm `calculate_circularity()`: Tính độ tròn bờ u:
       $$C = \frac{4\pi \cdot \text{Area}}{\text{Perimeter}^2}$$
       Khối u bờ tròn đều ($C \approx 1$) gợi ý u lành tính; bờ gồ ghề đa cung ($C \ll 1$) gợi ý u ác tính xâm lấn.
     * Hàm `extract_tumor_features()`: Đo diện tích u ($S_{\text{tumor}}$ pixel), tỷ lệ % u/não, tính tọa độ Bounding Box $(x, y, w, h)$, đóng gói vào dataclass `DiagnosticResult`.
  2. Cài đặt module trực quan hóa trong `src/measurement/visualization.py`:
     * Hàm `draw_tumor_overlay()`: Vẽ đường bao viền u màu vàng (`color=(0, 255, 255)`) và hộp giới hạn Bounding Box màu đỏ cảnh báo (`color=(0, 0, 255)`).
     * Hàm `create_comparison_quad()`: Ghép lưới 4 ảnh song song $[Ảnh gốc \mid Tách sọ \mid Mặt nạ u \mid Bounding Box]$.
  3. Viết unit tests kiểm thử: `tests/test_measurement.py`.
* **Lệnh kiểm tra:** `pytest tests/test_measurement.py -v`
* **Tiêu chí nghiệm thu & Checklist:**
  - [ ] 100% test cases trong `test_measurement.py` đạt kết quả PASSED.
  - [ ] Bounding Box và Contour vẽ chính xác trên tọa độ u, không bị lệch hoặc tràn khung.
  - [ ] Lưới 4 ảnh Quad display hiển thị đồng bộ kích thước $256 \times 256$.

---

### 🔹 NGÀY 4: Hoàn Thiện Notebook 03 & Xây Dựng Framework Benchmark Tự Động
* **Mục tiêu:** Xây dựng công cụ tự động đánh giá hàng loạt và hoàn thiện notebook so sánh đối chứng 2 giải thuật.
* **Nhiệm vụ cụ thể:**
  1. Hoàn thiện nội dung thực nghiệm trong `notebooks/03_tumor_segmentation_comparison.ipynb`:
     * Lập bảng so sánh trực quan Watershed vs Region Growing trên 3 nhóm kích thước: Ca u nhỏ, ca u trung bình, ca u lớn.
     * Trực quan hóa mặt nạ nhị phân dự đoán đặt cạnh mặt nạ Ground Truth của bác sĩ.
  2. Xây dựng module đánh giá hàng loạt `src/evaluation/benchmark.py`:
     * Lớp `BenchmarkRunner`: Tự động duyệt qua danh sách các file ảnh, nạp ground truth, gọi pipeline phân đoạn, đo thời gian thực thi (Latency ms) và thu thập 4 chỉ số y sinh.
  3. Xây dựng script thực nghiệm xử lý đa tiến trình `scripts/run_all_experiments.py`:
     * Tận dụng `concurrent.futures.ProcessPoolExecutor` trên CPU đa nhân để chạy song song hàng ngàn lát cắt đạt tốc độ ~250 ảnh/giây.
* **Lệnh kiểm tra:** `python -c "from src.evaluation.benchmark import run_benchmark; print('Benchmark module OK')"`
* **Tiêu chí nghiệm thu & Checklist:**
  - [ ] Chạy mượt mà toàn bộ `notebooks/03_tumor_segmentation_comparison.ipynb`.
  - [ ] Framework benchmark sẵn sàng thực thi quy mô lớn mà không nghẽn bộ nhớ.

---

### 🔹 NGÀY 5: Hoàn Thiện Web Demo Streamlit, Benchmark 3,929 Lát & Notebook 04
* **Mục tiêu:** Hoàn thiện giao diện ứng dụng web tương tác trực quan cho bác sĩ và chốt toàn bộ số liệu benchmark trên 3,929 lát cắt.
* **Nhiệm vụ cụ thể:**
  1. Hoàn thiện ứng dụng web tương tác Streamlit trong `demo/app.py`:
     * Sidebar điều khiển: Chuyển đổi linh hoạt giữa "Dữ liệu toàn bộ (3,929 lát)" và "20 mẫu nhanh", bộ lọc 110 mã bệnh nhân, chọn thuật toán phân đoạn (Watershed / Region Growing), thanh trượt điều chỉnh siêu tham số theo thời gian thực.
     * Khu vực chẩn đoán chính: 5 thẻ KPI nổi bật (Trạng thái phát hiện, Diện tích u, Tỷ lệ u/não, Độ tròn bờ u, Điểm tương đồng Dice).
     * Khu vực hiển thị Quad View và so sánh trực quan với Ground Truth.
     * Tính năng xuất file báo cáo chẩn đoán định dạng bảng.
  2. Chạy benchmark quy mô toàn bộ 3,929 lát cắt (110 bệnh nhân) thông qua `scripts/run_all_experiments.py`:
     * Xuất kết quả tổng hợp 2 nhóm (1,373 lát có u, 2,556 lát não lành) ra file `docs/BENCHMARK_RESULTS.csv`.
     * Xuất chi tiết 7,858 kết quả thực nghiệm ra `docs/BENCHMARK_RESULTS_FULL.csv`.
  3. Hoàn thiện `notebooks/04_quantitative_evaluation.ipynb`:
     * Vẽ biểu đồ cột Bar chart đối chiếu hiệu năng Dice, IoU và thời gian thực thi giữa Watershed và Region Growing.
     * Lưu các biểu đồ độ phân giải cao phục vụ chèn vào Chương 8 của Báo cáo.
* **Lệnh kiểm tra:** `streamlit run demo/app.py --server.headless true`
* **Tiêu chí nghiệm thu & Checklist:**
  - [ ] Giao diện Streamlit chạy trơn tru, phản hồi nhanh dưới 1 giây.
  - [ ] Hoàn tất 7,858 lượt đánh giá thực nghiệm trên 3,929 lát cắt chuẩn.
  - [ ] Toàn bộ file CSV và biểu đồ đánh giá định lượng được lưu hoàn chỉnh.

---

### 🔹 NGÀY 6: Biên Soạn Báo Cáo Đồ Án Toàn Văn (6 Chương Tổng Quan & Định Lượng)
* **Mục tiêu:** Biên soạn các chương tổng quan, số liệu thực nghiệm, hướng dẫn giao diện và xuất file Word đúng quy chuẩn HUIT.
* **Nhiệm vụ cụ thể:**
  * Trực tiếp biên soạn 6 chương trong Báo cáo đồ án:
    1. **Trang bìa & Mục lục:** Chuẩn hóa thông tin đề tài, Giảng viên hướng dẫn, thông tin 2 thành viên nhóm, bảng phân công nhiệm vụ Sprint 7 ngày (tỷ lệ 50% - 50%), mục lục tự động, danh mục bảng biểu và hình ảnh.
    2. **Mục 1: Mở đầu / Giới thiệu đề tài:** Đặt vấn đề lâm sàng về khối u não, ý nghĩa của ảnh MRI, mục tiêu đầu vào - đầu ra và phạm vi giải quyết của đồ án.
    3. **Mục 3: Mô tả tập dữ liệu:** Thuyết minh bộ dữ liệu quốc tế TCGA-LGG (Buda et al. 2019), kho dữ liệu thực nghiệm `data/full/`, bảng thống kê mô tả kích thước u.
    4. **Mục 5: Kiến trúc pipeline & Bộ đo định lượng:** Trình bày sơ đồ luồng dữ liệu 4 tầng và công thức toán học các chỉ số Dice, IoU, Sensitivity, Specificity, Circularity.
    5. **Mục 8 (Phần định lượng): Bảng số liệu & Biểu đồ đánh giá:** Trình bày bảng so sánh Mean $\pm$ Std của 2 thuật toán trên 3,929 lát cắt, chèn biểu đồ trực quan hóa kết quả.
    6. **Mục 9: Chương trình ứng dụng minh họa (Demo GUI):** Mô tả kiến trúc module Streamlit, hướng dẫn cài đặt và vận hành, chèn 4 ảnh chụp màn hình giao diện thao tác thực tế.
    7. **Mục 10: Kết luận & Hướng phát triển:** Đúc kết thành tựu kỹ thuật, hạn chế và đề xuất hướng mở rộng 3D thể tích.
  * Phối hợp cùng Trường ghép nối thành `docs/BAO_CAO_DO_AN_XLAS.md` và chạy `python scripts/export_report_docx.py` để xuất bản file Word `docs/BAO_CAO_DO_AN_XLAS.docx` tuân thủ nghiêm ngặt Quy chuẩn Word HUIT (Times New Roman 13pt, line spacing 1.5, lề 3-3-3-2 cm).
* **Lệnh kiểm tra:** `python scripts/export_report_docx.py`
* **Tiêu chí nghiệm thu & Checklist:**
  - [ ] Toàn bộ 6 chương tổng quan và định lượng được biên soạn chỉn chu.
  - [ ] File Word `docs/BAO_CAO_DO_AN_XLAS.docx` chuẩn thể thức in ấn, căn lề và bảng biểu hoàn hảo.

---

### 🔹 NGÀY 7: Thiết Kế Bộ Slide 20 Trang, Quay Video Demo & Đóng Gói
* **Mục tiêu:** Chuẩn bị trọn bộ tài liệu bảo vệ trực quan, ghi hình video thuyết minh hệ thống và đóng gói sản phẩm nộp.
* **Nhiệm vụ cụ thể:**
  1. Thiết kế bộ Slide thuyết trình chính thức (20 slides) theo dàn ý chi tiết tại `docs/SLIDE_THUYET_TRINH_OUTLINE.md`:
     * Đặt vấn đề & Mục tiêu đề tài.
     * Bộ dữ liệu TCGA-LGG & Chuẩn hóa kho dữ liệu full.
     * Sơ đồ khối pipeline DIP 4 tầng.
     * Kỹ thuật Tách sọ não 6 bước & 2 thuật toán phân đoạn (Trường hỗ trợ nội dung kỹ thuật).
     * Bảng kết quả thực nghiệm toàn diện trên 3,929 lát cắt và biểu đồ đối sánh.
     * Trực quan hóa các tính năng nổi bật của Web Demo Streamlit.
     * Kết luận và định hướng nghiên cứu tiếp theo.
  2. Quay Video clip demo hệ thống (thời lượng khoảng 3 phút):
     * Thuyết minh rõ ràng quy trình nạp ảnh MRI từ bộ dữ liệu.
     * Thao tác chọn thuật toán Marker-controlled Watershed và quan sát trực tiếp kết quả tách sọ, Bounding Box và các thẻ KPI.
     * Thao tác chuyển đổi sang Region Growing và điều chỉnh thanh trượt tham số.
  3. Kiểm tra tính toàn vẹn của mã nguồn: Chạy lại `pytest -v` cùng Trường để xác nhận 12/12 unit tests đạt chuẩn.
  4. Đóng gói toàn bộ sản phẩm đồ án thành file nén ZIP theo đúng quy cách của Khoa CNTT - HUIT.
* **Lệnh kiểm tra:** `pytest -v`
* **Tiêu chí nghiệm thu & Checklist:**
  - [ ] Bộ Slide 20 trang hoàn thành, thiết kế chuyên nghiệp, đồng bộ nhận diện.
  - [ ] Video demo 3 phút ghi hình rõ nét, âm thanh thuyết minh lưu loát.
  - [ ] Toàn bộ hồ sơ đồ án đóng gói sẵn sàng nộp đúng hạn.

---

## ✍️ CAM KẾT HOÀN THÀNH VÀ KÝ XÁC NHẬN

Tôi xin cam đoan bản kế hoạch Sprint 7 ngày trên phản ánh chính xác 100% khối lượng công việc, đóng góp định lượng và sự phối hợp thực tế của bản thân trong đồ án môn học Xử lý ảnh số.

*TP. Hồ Chí Minh, ngày 19 tháng 10 năm 2026*  
**Thành viên**  
*(Ký và ghi rõ họ tên)*  
**Huỳnh Tâm Trí**
