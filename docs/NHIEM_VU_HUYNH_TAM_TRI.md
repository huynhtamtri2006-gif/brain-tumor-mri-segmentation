# KẾ HOẠCH & PHÂN CÔNG NHIỆM VỤ 15 TUẦN — HUỲNH TÂM TRÍ
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
  * Thu thập, chuẩn hóa cấu trúc thư mục và quản lý dữ liệu ảnh MRI sọ não (TCGA-LGG Benchmark).
  * Nghiên cứu cơ sở lý thuyết và cài đặt hệ thống chỉ số đánh giá y sinh (Dice, IoU, Sensitivity, Specificity).
  * Cài đặt module Rút trích đặc trưng hình học khối u (Diện tích, Tỷ lệ u/não, Độ tròn Circularity, Bounding Box).
  * Xây dựng và hoàn thiện ứng dụng web tương tác minh họa (Streamlit GUI).
  * Chạy thực nghiệm định lượng quy mô lớn (3,929 lát cắt) và phân tích thống kê trong Notebook 01 và Notebook 04.
  * Soạn thảo các chương tổng quan & định lượng trong Báo cáo (Chương 1, 3, 5, 8 số liệu, 9 GUI, 10 kết luận).
  * Thiết kế Slide thuyết trình bảo vệ cuối kỳ và quay Video demo hệ thống.

---

## 🎯 ĐỐI CHIẾU VỚI RUBRIC ĐÁNH GIÁ ĐỒ ÁN MÔN HỌC (KHOA CNTT - HUIT)

Đồ án được chấm theo thang điểm 10 theo đúng Mục III trong `9. Ke_hoach_thuc_ĐA__XLAS_2026-2027.pdf`:

| Tiêu chí đánh giá | Trọng số | Đóng góp và minh chứng chính của Huỳnh Tâm Trí |
| :--- | :---: | :--- |
| **1. Phân tích & lựa chọn đúng phương pháp (PLO2, CLO1)** | **15% (1.5đ)** | - Khảo sát các bộ độ tương đồng y khoa chuẩn quốc tế (Dice Similarity Coefficient, Jaccard Index).<br>- Lựa chọn các đặc trưng hình học (Area, Perimeter, Circularity) phản ánh độ gồ ghề bờ u theo góc nhìn chẩn đoán lâm sàng. |
| **2. Áp dụng được các phương pháp xử lý (PLO2, CLO2)** *(Trọng tâm)* | **50% (5.0đ)** | - Tổ chức kiến trúc dữ liệu 2 tầng: `data/sample/` (20 mẫu) và `data/full/` (3,929 lát cắt chuẩn).<br>- Cài đặt module `src/evaluation/metrics.py` và `src/measurement/features.py`.<br>- Xây dựng ứng dụng Web tương tác Streamlit GUI (`demo/app.py`).<br>- Chạy thực nghiệm định lượng toàn diện trên 3,929 lát cắt và xuất báo cáo CSV chi tiết.<br>- Đạt 100% test cases trong `tests/test_metrics.py` và `tests/test_measurement.py`. |
| **3. Đọc tài liệu, nghiên cứu giải quyết bài toán (PLO4, CLO3)** | **10% (1.0đ)** | - Nghiên cứu bài báo gốc của Buda et al. (2019) công bố trên tạp chí *Computers in Biology and Medicine* về bộ dữ liệu TCGA-LGG.<br>- Soạn thảo tài liệu phân tích dữ liệu chuyên sâu [DATA_EXPLORATION_REPORT.md](file:///C:/Users/xpaga/Documents/xlas/docs/DATA_EXPLORATION_REPORT.md). |
| **4. Trình bày báo cáo (PLO7, CLO5)** | **15% (1.5đ)** | - Biên soạn các chương tổng quan, dữ liệu, bảng số liệu định lượng, giới thiệu GUI và kết luận.<br>- Chuẩn hóa bảng biểu, biểu đồ phân bố và hình ảnh chụp giao diện Streamlit rõ nét. |
| **5. Phân công & phối hợp làm việc nhóm (PLO6, CLO4)** | **10% (1.0đ)** | - Phối hợp chặt chẽ với Nhóm trưởng Trường trong suốt 15 tuần theo đúng tiến độ Bộ môn.<br>- Phụ trách toàn bộ khâu thiết kế Slide thuyết trình chuyên nghiệp và video clip minh họa hệ thống. |

---

## 🗺️ LỘ TRÌNH 15 TUẦN CHI TIẾT CỦA HUỲNH TÂM TRÍ

```
[Tuần 1]      Thống nhất đề tài, ký bản phân công nhiệm vụ & tiếp nhận kế hoạch 15 tuần
   │
[Tuần 2–3]    Nghiên cứu cơ sở lý thuyết bộ đo định lượng y sinh (Dice, IoU, Sens, Spec, Circularity)
   │
[Tuần 4]      Thu thập, kiểm tra & tổ chức dữ liệu chuẩn TCGA-LGG (3,929 lát) + Notebook 01
   │
[Tuần 5]      Phối hợp kiểm thử module Tiền xử lý trên dữ liệu thực tế & rà soát ảnh sau tách sọ
   │
[Tuần 6]      Cài đặt module tính toán độ đo y tế src/evaluation/metrics.py + Unit Tests
   │
[Tuần 7]      Thử nghiệm đo lường sơ bộ trên kết quả phân đoạn Baseline Watershed
   │
[Tuần 8]      CÙNG NHÓM TRƯỞNG BÁO CÁO TIẾN ĐỘ NỘI BỘ VỚI GIẢNG VIÊN HƯỚNG DẪN
   │
[Tuần 9]      Xây dựng framework benchmark tự động so sánh đa thuật toán (benchmark.py)
   │
[Tuần 10]     Cài đặt module Rút trích đặc trưng hình học u não (features.py & visualization.py)
   │
[Tuần 11]     Xây dựng & hoàn thiện ứng dụng web tương tác Streamlit GUI (demo/app.py)
   │
[Tuần 12]     Thực thi benchmark quy mô lớn trên toàn bộ 3,929 lát cắt + Notebook 04
   │
[Tuần 13]     Biên soạn bản nháp Báo cáo đồ án: 6 Chương Tổng quan & Định lượng
   │
[Tuần 14]     Rà soát unit tests (test_metrics, test_measurement), chốt số liệu thực nghiệm
   │
[Tuần 15]     Thiết kế toàn bộ Slide thuyết trình, quay Video Demo 3 phút & đóng gói nộp
   │
[Sau kết thúc 01 tuần] PHỐI HỢP NỘP TRỌN BỘ HỒ SƠ ĐỒ ÁN VÀ BẢO VỆ CUỐI KỲ
```

---

## 📋 NỘI DUNG THỰC HIỆN CHI TIẾT TỪNG TUẦN

### 🔹 Tuần 1: Khởi động Đề tài, Phân công Nhóm & Lập Kế hoạch
* **Nhiệm vụ:**
  1. Họp nhóm cùng Nhóm trưởng Trường, thống nhất lựa chọn đề tài u não MRI.
  2. Ký nhận bản phân công trách nhiệm chi tiết, tiếp nhận các mốc thời gian 15 tuần của Bộ môn.
  3. Thiết lập môi trường làm việc cá nhân (Python 3.12, OpenCV, Streamlit, Git).
* **Sản phẩm đạt được:** Bản phân công công việc chi tiết; môi trường phát triển đồng bộ.

### 🔹 Tuần 2 – Tuần 3: Nghiên cứu Lý thuyết Độ đo Định lượng Y sinh & Đặc trưng Hình học
* **Nhiệm vụ:**
  1. Tìm hiểu các tiêu chuẩn đánh giá định lượng phân đoạn ảnh y tế:
     * Chỉ số tương đồng Dice (Dice Similarity Coefficient / F1-score): Đo mức độ trùng khớp giữa mặt nạ dự đoán và Ground Truth.
     * Chỉ số Jaccard (Intersection over Union - IoU).
     * Độ nhạy (Sensitivity/Recall): Tỷ lệ phát hiện đúng vùng bệnh lý (cực kỳ quan trọng trong y tế để tránh bỏ sót u).
     * Độ đặc hiệu (Specificity): Tỷ lệ nhận diện đúng mô lành, đánh giá khả năng tránh dương tính giả.
  2. Nghiên cứu ý nghĩa lâm sàng của các đặc trưng hình học khối u: Diện tích ($S_{\text{tumor}}$), Tỷ lệ chiếm chỗ não thất, và Độ tròn ($C = 4\pi \cdot \text{Area} / \text{Perimeter}^2$) — phân biệt khối u có bờ tròn đều (lành tính) hay bờ gồ ghề đa cung (ác tính).
* **Sản phẩm đạt được:** Bản tổng hợp lý thuyết các độ đo định lượng y sinh.

### 🔹 Tuần 4: Thu thập, Chuẩn hóa & Khám phá Dữ liệu (TCGA-LGG Benchmark)
* **Nhiệm vụ:**
  1. Tải và chuẩn hóa bộ dữ liệu nghiên cứu chuẩn quốc tế The Cancer Genome Atlas Low-Grade Glioma (TCGA-LGG) gồm 3,929 lát cắt MRI từ 110 bệnh nhân.
  2. Thiết kế cấu trúc thư mục dữ liệu hai tầng:
     * `data/sample/`: 20 lát cắt đại diện phục vụ kiểm thử nhanh CI/CD (< 1.5s).
     * `data/full/`: 3,929 lát cắt chuẩn (tải tự động qua `python scripts/download_full_dataset.py`).
  3. Xây dựng và chạy hoàn thiện `notebooks/01_data_exploration.ipynb`:
     * Thống kê mô tả: Diện tích u Min (7 px), Max (7,929 px), Trung vị (1,529 px), Trung bình (1,931 px).
     * Vẽ biểu đồ phân bố kích thước u và phân loại 3 nhóm: U nhỏ (< 1.5%), U trung bình (1.5%–5%), U lớn (> 5%).
  4. Xuất tài liệu [DATA_EXPLORATION_REPORT.md](file:///C:/Users/xpaga/Documents/xlas/docs/DATA_EXPLORATION_REPORT.md).
* **Sản phẩm đạt được:** `data/sample/`, `data/full/`, `notebooks/01_data_exploration.ipynb`, `docs/DATA_EXPLORATION_REPORT.md`.

### 🔹 Tuần 5: Phối hợp Kiểm thử Tiền xử lý Trên Dữ liệu Thực tế
* **Nhiệm vụ:**
  1. Chạy thử nghiệm module tiền xử lý do Trường cài đặt trên các ca chụp có đặc điểm khác nhau (ảnh có độ tương phản thấp, ảnh có nhiễu sọc).
  2. Kiểm tra tính ổn định của mặt nạ não (Brain Mask) sau tách sọ, ghi nhận các trường hợp ranh giới màng não còn sót để phản hồi cho Trường tối ưu tham số morphological opening.
* **Sản phẩm đạt được:** Biên bản kiểm thử tiền xử lý trên dữ liệu thực tế.

### 🔹 Tuần 6: Cài đặt Module Tính toán Độ đo Định lượng Y tế
* **Nhiệm vụ:**
  1. Cài đặt module `src/evaluation/metrics.py`:
     * `calculate_dice(y_true, y_pred)`
     * `calculate_iou(y_true, y_pred)`
     * `calculate_sensitivity(y_true, y_pred)`
     * `calculate_specificity(y_true, y_pred)`
     * `calculate_all_metrics(y_true, y_pred)`
  2. Xử lý an toàn các ca biên (edge cases): Trường hợp cả ảnh ground truth và dự đoán đều là não lành không có u ($0/0 \rightarrow Dice=1.0, Sens=1.0$).
  3. Viết unit tests kiểm thử độ chính xác số học: `tests/test_metrics.py` (4 test cases passed).
* **Sản phẩm đạt được:** `src/evaluation/metrics.py`, `tests/test_metrics.py` (100% passed).

### 🔹 Tuần 7: Thử nghiệm Đo lường Sơ bộ Trên Kết quả Phân đoạn Baseline
* **Nhiệm vụ:**
  1. Áp dụng bộ đo metrics để đánh giá sơ bộ kết quả phân đoạn của Watershed trên 20 mẫu kiểm thử.
  2. Ghi nhận thời gian thực thi (Latency ms/ảnh) và lập bảng so sánh bước đầu.
* **Sản phẩm đạt được:** Bảng kết quả định lượng sơ bộ của phương pháp Baseline.

### 🔹 Tuần 8: Cùng Nhóm Trưởng Báo Cáo Tiến Độ Nội Bộ Với Giảng Viên
* **Nhiệm vụ:**
  1. Phối hợp cùng Trường chuẩn bị báo cáo tiến độ Tuần 8: Trình bày nguồn dữ liệu TCGA-LGG, phương pháp kiểm tra ground truth, công thức các chỉ số đánh giá và kết quả bước đầu.
  2. Ghi chép các yêu cầu điều chỉnh của giảng viên về cách phân tích độ đặc hiệu trên các lát não lành.
* **Sản phẩm đạt được:** Hoàn thành báo cáo tiến độ giai đoạn 1.

### 🔹 Tuần 9: Xây dựng Framework Benchmark Tự động
* **Nhiệm vụ:**
  1. Xây dựng module `src/evaluation/benchmark.py` cho phép tự động duyệt qua danh sách ảnh, áp dụng phương pháp phân đoạn, tính toán 4 chỉ số và tổng hợp kết quả (Mean $\pm$ Std).
  2. Xây dựng script thực nghiệm xử lý đa tiến trình `scripts/run_all_experiments.py` bằng `concurrent.futures.ProcessPoolExecutor` đạt tốc độ ~250 fps.
* **Sản phẩm đạt được:** `src/evaluation/benchmark.py`, `scripts/run_all_experiments.py`.

### 🔹 Tuần 10: Cài đặt Module Rút trích Đặc trưng Hình học & Trực quan hóa
* **Nhiệm vụ:**
  1. Cài đặt module `src/measurement/features.py`:
     * Hàm `calculate_circularity()`: Tính độ tròn của khối u.
     * Hàm `extract_tumor_features()`: Trích xuất Bounding Box $(x, y, w, h)$, diện tích pixel u, tỷ lệ % u/não và đóng gói vào `DiagnosticResult`.
  2. Cài đặt module `src/measurement/visualization.py`:
     * Hàm `draw_tumor_overlay()`: Vẽ Bounding Box màu đỏ cảnh báo và đường bao contour màu vàng quanh khối u.
     * Hàm `create_comparison_quad()`: Ghép lưới 4 ảnh song song $[Gốc \mid Tách sọ \mid Mặt nạ \mid Bounding Box]$.
  3. Viết unit tests: `tests/test_measurement.py` (3 test cases passed).
* **Sản phẩm đạt được:** `src/measurement/`, `tests/test_measurement.py` (100% passed).

### 🔹 Tuần 11: Xây dựng Ứng dụng Web Tương tác Hoàn chỉnh (Streamlit GUI)
* **Nhiệm vụ:**
  1. Xây dựng ứng dụng web tương tác hoàn chỉnh `demo/app.py`:
     * Sidebar: Chuyển đổi linh hoạt giữa "Toàn bộ 3,929 lát cắt" và "20 mẫu nhanh", chọn ca bệnh, chọn thuật toán (Watershed / Region Growing), thanh trượt tinh chỉnh siêu tham số.
     * Vùng chính: Thẻ KPI chẩn đoán nhanh (Trạng thái u, Diện tích, Tỷ lệ %, Độ tròn, Dice Score).
     * Lưới hiển thị trực quan các bước trung gian và so sánh trực tiếp với Ground Truth.
     * Chức năng xuất báo cáo chẩn đoán y tế.
  2. Kiểm tra tính ổn định, phản hồi thời gian thực và trải nghiệm người dùng.
* **Sản phẩm đạt được:** `demo/app.py`, `demo/utils.py`.

### 🔹 Tuần 12: Thực thi Benchmark Quy mô Lớn & Hoàn thiện Notebook 04
* **Nhiệm vụ:**
  1. Chạy thực nghiệm định lượng toàn diện trên toàn bộ 3,929 lát cắt dữ liệu TCGA-LGG cho cả 2 thuật toán Watershed và Region Growing.
  2. Phân tích kết quả theo 2 nhóm: 1,373 lát cắt có u và 2,556 lát cắt não lành.
  3. Hoàn thiện `notebooks/04_quantitative_evaluation.ipynb`:
     * Bảng so sánh toàn diện: Watershed đạt Dice 0.4446 (gấp 2.23 lần Region Growing: 0.1990).
     * Phân tích Specificity trên lát não lành: Đạt 99.04% (Watershed) và 97.60% (Region Growing).
     * Vẽ biểu đồ cột so sánh điểm Dice, IoU và độ trễ xử lý.
  4. Xuất các bảng số liệu ra `docs/BENCHMARK_RESULTS.csv` và `docs/BENCHMARK_RESULTS_FULL.csv` (7,858 kết quả).
* **Sản phẩm đạt được:** `notebooks/04_quantitative_evaluation.ipynb`, `docs/BENCHMARK_RESULTS.csv`.

### 🔹 Tuần 13: Biên Soạn Bản Nháp Báo Cáo Đồ Án (6 Chương Tổng quan & Định lượng)
* **Nhiệm vụ:**
  * Soạn thảo 6 chương trong Báo cáo đồ án toàn văn theo cấu trúc 12 mục chuẩn HUIT:
    * **Trang bìa & Mục lục:** Danh sách thành viên, bảng phân công 15 tuần, tỷ lệ đóng góp (Trường 50% - Trí 50%), mục lục tự động.
    * **Mục 3: Giới thiệu đề tài:** Đặt vấn đề y tế, mục tiêu đầu vào - đầu ra, ý nghĩa thực tiễn.
    * **Mục 5: Mô tả dữ liệu:** Tổng quan bộ dữ liệu TCGA-LGG, bảng thống kê phân bố kích thước u, quy cách mặt nạ ground truth nhị phân.
    * **Mục 8 (Phần định lượng):** Bảng số liệu thống kê Mean $\pm$ Std của Dice, IoU, Sensitivity, Specificity, Latency trên 3,929 lát cắt, biểu đồ so sánh cột trực quan.
    * **Mục 9: Chương trình minh họa:** Giới thiệu giao diện Streamlit, hướng dẫn cài đặt và sử dụng, các ảnh chụp màn hình minh họa.
    * **Mục 10: Kết luận:** Đúc kết kết quả, hạn chế và hướng phát triển.
* **Sản phẩm đạt được:** Bản nháp 6 chương báo cáo hoàn chỉnh.

### 🔹 Tuần 14: Rà Soát Unit Tests, Kiểm Thử Hệ Thống & Chốt Số Liệu
* **Nhiệm vụ:**
  1. Chạy toàn bộ các test cases phụ trách: `pytest tests/test_measurement.py tests/test_metrics.py -v`.
  2. Rà soát file `requirements.txt` đảm bảo đầy đủ các thư viện phụ thuộc (`streamlit`, `pandas`, `opencv-python`, `python-docx`, `scikit-learn`).
  3. Cùng Trường kiểm tra tính nhất quán giữa số liệu trong Báo cáo Word, Notebooks và file CSV.
* **Sản phẩm đạt được:** Hệ sinh thái kiểm thử đạt 100%, số liệu thực nghiệm khớp tuyệt đối.

### 🔹 Tuần 15: Thiết Kế Slide Thuyết Trình, Quay Video Demo & Đóng Gói
* **Nhiệm vụ:**
  1. Thiết kế bộ Slide thuyết trình chính thức (18–20 slides) theo chuẩn nhận diện HUIT:
     * Đặt vấn đề y tế, Mục tiêu & Phạm vi.
     * Bộ dữ liệu nghiên cứu TCGA-LGG.
     * Sơ đồ pipeline xử lý ảnh số 7 bước.
     * Kỹ thuật Tách sọ não và 2 thuật toán phân đoạn (Trường hỗ trợ nội dung).
     * Bảng kết quả định lượng trên 3,929 lát cắt và biểu đồ đối chiếu.
     * Trực quan hóa ứng dụng Streamlit GUI.
     * Kết luận và bài học kinh nghiệm.
  2. Quay Video clip demo hệ thống (thời lượng 2–3 phút) thuyết minh các tính năng chính của GUI.
  3. Đóng gói toàn bộ hồ sơ đồ án nộp đúng quy định.
* **Sản phẩm đạt được:** Bộ Slide thuyết trình hoàn chỉnh, Video clip demo, Hồ sơ đóng gói sẵn sàng nộp.

### 🔹 Sau Khi Kết Thúc Học Phần 01 Tuần: Phối Hợp Nộp Đồ Án & Bảo Vệ
* **Nhiệm vụ:** Phối hợp cùng Nhóm trưởng nộp trọn bộ hồ sơ đồ án trên Google Classroom / cổng nộp bài của Trường đúng hạn. Sẵn sàng bảo vệ đồ án trước Hội đồng chấm thi.
