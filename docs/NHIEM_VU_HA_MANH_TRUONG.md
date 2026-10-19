# KẾ HOẠCH & PHÂN CÔNG NHIỆM VỤ CẤP TỐC 7 NGÀY — HÀ MẠNH TRƯỜNG
### Học phần: Xử lý ảnh số (0101006276) — Học kỳ 2026–2027
**Đơn vị:** Bộ môn Khoa học Dữ liệu — Khoa Công nghệ Thông tin — Trường ĐH Công Thương TP.HCM (HUIT)  
**Đề tài:** Phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ MRI (TCGA-LGG Benchmark)

---

## 👤 THÔNG TIN SINH VIÊN
* **Họ và tên:** **HÀ MẠNH TRƯỜNG**
* **Mã số sinh viên:** **2045240326**
* **Lớp sinh hoạt:** 15DHKHDL03
* **Vai trò:** **Nhóm trưởng**
* **Trách nhiệm trọng tâm:**
  * Điều phối tiến độ Sprint cấp tốc 7 ngày của nhóm theo đúng chuẩn mực của Bộ môn.
  * Thiết kế kiến trúc tổng thể pipeline Xử lý ảnh số (DIP) 4 tầng và soạn thảo đặc tả kỹ thuật `docs/SPEC_PIPELINE_MRI.md`.
  * Nghiên cứu cơ sở toán học và cài đặt module Tiền xử lý & Tách sọ não (*Skull Stripping*) 6 bước kinh điển.
  * Cài đặt giải thuật phân đoạn u não lõi Baseline (*Marker-controlled Watershed*) và Phương án đối chứng (*Seeded Region Growing*).
  * Phân tích chuyên sâu các ca thất bại (*Failure Cases*) trên tập dữ liệu quy mô 3,929 lát cắt TCGA-LGG.
  * Viết các chương kỹ thuật trong Báo cáo đồ án (Chương 2, 4, 6 và phân tích kỹ thuật Chương 8).
  * Đảm bảo tính toàn vẹn của mã nguồn xử lý ảnh và hệ thống kiểm thử tự động 12/12 Unit Tests (`pytest`).

---

## 🎯 ĐỐI CHIẾU VỚI RUBRIC ĐÁNH GIÁ ĐỒ ÁN MÔN HỌC (KHOA CNTT - HUIT)

Đồ án được chấm theo thang điểm 10 theo đúng Mục III trong `9. Ke_hoach_thuc_ĐA__XLAS_2026-2027.pdf`:

| Tiêu chí đánh giá | Trọng số | Đóng góp và minh chứng chính của Hà Mạnh Trường |
| :--- | :---: | :--- |
| **1. Phân tích & lựa chọn đúng phương pháp (PLO2, CLO1)** | **15% (1.5đ)** | - Phân tích đặc trưng ảnh MRI FLAIR/T1-CE, đề xuất giải pháp tách sọ não bằng hình thái học.<br>- Lựa chọn và so sánh 2 giải thuật phân đoạn kinh điển: Watershed phân thủy và Region Growing. |
| **2. Áp dụng được các phương pháp xử lý (PLO2, CLO2)** *(Trọng tâm)* | **50% (5.0đ)** | - Cài đặt bộ lọc Bilateral khử nhiễu Rician bảo toàn biên và CLAHE tăng tương phản mô não.<br>- Xây dựng pipeline 6 bước tách sọ não kinh điển triệt tiêu xương sọ.<br>- Cài đặt thuật toán phân đoạn Watershed và Region Growing kèm khảo sát siêu tham số.<br>- Đạt 100% test cases trong `tests/test_preprocessing.py` và `tests/test_segmentation.py`. |
| **3. Đọc tài liệu, nghiên cứu giải quyết bài toán (PLO4, CLO3)** | **10% (1.0đ)** | - Nghiên cứu sâu giáo trình chuẩn *Gonzalez & Woods, Digital Image Processing (4th Ed.)* các Chương 3, 5, 9, 10.<br>- Soạn thảo tài liệu đặc tả kỹ thuật toán học chi tiết [SPEC_PIPELINE_MRI.md](file:///C:/Users/xpaga/Documents/xlas/docs/SPEC_PIPELINE_MRI.md). |
| **4. Trình bày báo cáo (PLO7, CLO5)** | **15% (1.5đ)** | - Chịu trách nhiệm biên soạn 4 chương kỹ thuật trọng tâm trong Báo cáo toàn văn (Word/PDF).<br>- Trình bày sơ đồ khối pipeline, công thức toán học và ảnh chụp thực nghiệm minh chứng. |
| **5. Phân công & phối hợp làm việc nhóm (PLO6, CLO4)** | **10% (1.0đ)** | - Đảm nhiệm vai trò Nhóm trưởng: Lập kế hoạch Sprint 7 ngày, phân công rõ ràng cho thành viên.<br>- Duy trì kho mã nguồn Git, quản lý issues và review chất lượng sản phẩm trước khi tích hợp. |

---

## 🗺️ LỘ TRÌNH SPRINT CẤP TỐC 7 NGÀY CỦA HÀ MẠNH TRƯỜNG

```
[Ngày 1] Khởi động Sprint, Thiết kế Kiến trúc Pipeline & Soạn Đặc tả Kỹ thuật (SPEC_PIPELINE_MRI.md)
   │
[Ngày 2] Cài đặt Module Tiền xử lý & Quy trình 6 bước Tách sọ não (Skull Stripping) + Notebook 02
   │
[Ngày 3] Cài đặt Phương pháp Baseline 1: Marker-controlled Watershed & Khảo sát Siêu tham số
   │
[Ngày 4] Cài đặt Phương pháp Đối chứng 2: Seeded Region Growing & Tích hợp Pipeline Trung tâm
   │
[Ngày 5] Phối hợp Benchmark Quy mô lớn (3,929 lát cắt) & Phân tích Chuyên sâu Ca Thất bại (Failure Cases)
   │
[Ngày 6] Biên soạn Báo cáo Đồ án Toàn văn (4 Chương Kỹ thuật Trọng tâm: Mục 2, 4, 6, 8 kỹ thuật)
   │
[Ngày 7] Chuẩn hóa Mã nguồn src/, Đạt 12/12 Unit Tests, Soạn Slide Kỹ thuật & Đóng gói Hồ sơ
   │
[Nghiệm thu] BẢO VỆ ĐỒ ÁN TRƯỚC HỘI ĐỒNG CHẤM THI KHOA CNTT - HUIT
```

---

## 📋 NỘI DUNG THỰC HIỆN CHI TIẾT TỪNG NGÀY

### 🔹 NGÀY 1: Khởi Động Sprint, Thiết Kế Pipeline & Soạn Thảo Đặc Tả Kỹ Thuật
* **Mục tiêu:** Thống nhất kiến trúc hệ thống xử lý ảnh y tế, chốt luồng xử lý 4 tầng, và hoàn thành tài liệu đặc tả kỹ thuật toán học.
* **Nhiệm vụ cụ thể:**
  1. Họp khởi động Sprint cùng Trí: Phân chia phạm vi trách nhiệm 50% - 50%, thiết lập môi trường Git repository (`brain-tumor-mri-segmentation`).
  2. Nghiên cứu các chương liên quan trong giáo trình chuẩn *Gonzalez & Woods (4th Ed.)*:
     * Chương 3: Cải thiện độ tương phản thích nghi CLAHE.
     * Chương 5: Khử nhiễu Rician bảo toàn biên u bằng lọc song phương (Bilateral Filtering).
     * Chương 9: Hình thái học ảnh nhị phân (Opening cắt cầu nối mô, Closing lấp lỗ rỗng, LCC).
     * Chương 10: Phân đoạn ảnh bằng biến đổi khoảng cách Euclidean (EDT), Watershed và Region Growing.
  3. Xây dựng sơ đồ khối pipeline xử lý ảnh 4 tầng: Tiền xử lý $\rightarrow$ Tách sọ $\rightarrow$ Phân đoạn $\rightarrow$ Đánh giá & Trích xuất đặc trưng.
  4. Soạn thảo tài liệu đặc tả kỹ thuật `docs/SPEC_PIPELINE_MRI.md` bao gồm:
     * 13 chữ ký hàm chuẩn hóa với kiểu dữ liệu rõ ràng (`np.ndarray`, `uint8`, `float`).
     * 7 bất biến dữ liệu (I1–I7) đảm bảo tính ổn định của hệ thống.
     * Cơ sở toán học chi tiết của từng thuật toán.
* **Lệnh kiểm tra:** `python -c "import yaml; print(yaml.safe_load(open('configs/default_params.yaml')))"`
* **Tiêu chí nghiệm thu & Checklist:**
  - [x] Đề tài và kế hoạch Sprint 7 ngày được thống nhất.
  - [x] Hoàn tất tài liệu đặc tả kỹ thuật `docs/SPEC_PIPELINE_MRI.md`.
  - [x] Khớp nối hợp đồng giao diện hàm (API interface) với thành viên Trí.

---

### 🔹 NGÀY 2: Hoàn Thiện Module Tiền Xử Lý, Tách Sọ Não & Notebook 02
* **Mục tiêu:** Loại bỏ hoàn toàn hộp sọ và da đầu khỏi ảnh chụp MRI, bảo toàn nguyên vẹn nhu mô não và vùng u.
* **Nhiệm vụ cụ thể:**
  1. Cài đặt các hàm lọc trong `src/preprocessing/filters.py`:
     * `apply_bilateral_filter()` ($d=9, \sigma_c=75, \sigma_s=75$): Làm mịn nhiễu hạt Rician nhưng giữ nguyên độ dốc sắc nét tại bờ khối u.
     * `apply_clahe()` ($\text{clip\_limit}=2.0, \text{tile\_grid}=(8, 8)$): Tăng tương phản mô mềm não.
  2. Cài đặt thuật toán Tách sọ não (Skull Stripping) 6 bước trong `src/preprocessing/skull_strip.py`:
     * Bước 1: Khử nhiễu sơ bộ bằng lọc Gauss.
     * Bước 2: Phân ngưỡng tự động Otsu tạo mặt nạ nhị phân thô ban đầu.
     * Bước 3: Phép toán hình thái học Opening với cấu trúc phần tử đĩa elip ($5 \times 5$, 2 lần lặp) nhằm cắt đứt cầu nối mô liên kết giữa xương sọ và nhu mô não.
     * Bước 4: Thuật toán tìm thành phần liên thông lớn nhất (Largest Connected Component - LCC) bằng hàm `cv2.connectedComponentsWithStats` để giữ lại khoang não lớn nhất và loại bỏ các vụn mô ngoại vi.
     * Bước 5: Phép toán hình thái học Closing ($11 \times 11$) và lấp đầy lỗ rỗng (Hole filling) để bảo toàn nhu mô não nguyên khối.
     * Bước 6: Phép nhân bitwise (`cv2.bitwise_and`) giữa ảnh gốc và mặt nạ nhu mô não để trích xuất ảnh não đã bóc sọ.
  3. Hoàn thiện và chạy thử nghiệm `notebooks/02_preprocessing_and_skull_stripping.ipynb`: Kiểm tra tính bền vững trên các ca u não ở các vị trí giải phẫu khác nhau.
  4. Chạy kiểm thử tự động: `pytest tests/test_preprocessing.py -v`.
* **Lệnh kiểm tra:** `pytest tests/test_preprocessing.py -v`
* **Tiêu chí nghiệm thu & Checklist:**
  - [x] 100% test cases trong `test_preprocessing.py` đều đạt kết quả PASSED.
  - [x] Chạy hoàn thiện `notebooks/02_preprocessing_and_skull_stripping.ipynb` không phát sinh lỗi.
  - [x] Xuất bộ ảnh minh họa 6 bước trung gian để phục vụ đưa vào Chương 4 Báo cáo.

---

### 🔹 NGÀY 3: Cài Đặt Thuật Toán Phân Đoạn Baseline 1 — Marker-Controlled Watershed
* **Mục tiêu:** Hiện thực hóa giải thuật phân đoạn u não lõi kinh điển dựa trên phân thủy mầm đánh dấu.
* **Nhiệm vụ cụ thể:**
  1. Cài đặt lớp `WatershedSegmenter` trong `src/segmentation/watershed.py`:
     * Áp dụng biến đổi khoảng cách Euclidean (`cv2.distanceTransform` với cự ly Euclidean $L_2$) trên mặt nạ nhị phân vùng nghi ngờ bệnh lý.
     * Xác định vùng chắc chắn u (Sure Foreground) bằng cách áp dụng ngưỡng tỷ lệ so với khoảng cách cực đại: $T_{fg} = \text{ratio} \cdot \max(D)$.
     * Xác định vùng chắc chắn nền (Sure Background) bằng phép giãn nở hình thái học (`cv2.dilate`).
     * Xác định vùng tranh chấp biên (Unknown Region) bằng phép trừ ảnh nhị phân: $\text{Unknown} = \text{Sure BG} - \text{Sure FG}$.
     * Đánh số nhãn hạt giống (Markers) và thực thi thuật toán phân thủy `cv2.watershed`.
     * Hậu xử lý nhị phân hóa mặt nạ u: Giữ lại vùng mang nhãn u và lọc bỏ các đảo nhiễu nhỏ hơn `min_tumor_area`.
  2. Xử lý an toàn các ca âm tính: Nếu ảnh não lành không có điểm hạt giống u, trả về mặt nạ nhị phân toàn số 0 an toàn mà không làm sập pipeline.
  3. Khảo sát siêu tham số: Khảo sát độ nhạy của `dist_thresh_ratio` từ 0.2 đến 0.6 để chọn giá trị tối ưu 0.4.
  4. Chạy kiểm thử tự động: `pytest tests/test_segmentation.py -k watershed -v`.
* **Lệnh kiểm tra:** `pytest tests/test_segmentation.py -k watershed -v`
* **Tiêu chí nghiệm thu & Checklist:**
  - [ ] Test `test_watershed_segmentation` đạt kết quả PASSED.
  - [ ] Watershed phân đoạn chính xác trên các ca u kích thước trung bình và lớn.
  - [ ] Cơ chế xử lý ca âm tính (lát não lành) hoạt động an toàn tuyệt đối.

---

### 🔹 NGÀY 4: Cài Đặt Thuật Toán Đối Chứng 2 — Seeded Region Growing & Tích Hợp Pipeline
* **Mục tiêu:** Cài đặt phương án phân đoạn đối chứng và tích hợp luồng điều phối pipeline trung tâm từ ảnh thô đến u não.
* **Nhiệm vụ cụ thể:**
  1. Cài đặt lớp `RegionGrowingSegmenter` trong `src/segmentation/region_growing.py`:
     * Hàm tự động định vị hạt giống `find_seed_point()`: Tìm điểm pixel có cường độ sáng cực đại trong vùng não đã bóc sọ (loại trừ biên viền não).
     * Thuật toán lan truyền phát triển vùng dựa trên hàng đợi (BFS Queue) với liên thông 8 láng giềng: Pixel láng giềng $p$ được thu nhận nếu $|I(p) - I(\text{seed})| \le \text{tolerance}$.
     * Khảo sát tham số dung sai `intensity_tolerance = 15` và kiểm soát vùng kích thước u `[min_tumor_area, max_tumor_area] = [50, 25000]`.
  2. Tích hợp lớp điều phối trung tâm `BrainTumorPipeline` trong `src/pipeline.py`:
     * Khớp nối liên hoàn: Nhận ảnh đầu vào $\rightarrow$ Lọc Bilateral $\rightarrow$ Tách sọ não $\rightarrow$ Cân bằng CLAHE $\rightarrow$ Phân đoạn (Watershed/Region Growing) $\rightarrow$ Đo đặc trưng hình học $\rightarrow$ Vẽ trực quan hóa.
     * Bắt lỗi ngoại lệ an toàn khi nhận ảnh rỗng hoặc sai định dạng.
  3. Hoàn thiện nội dung so sánh thuật toán trong `notebooks/03_tumor_segmentation_comparison.ipynb`.
* **Lệnh kiểm tra:** `pytest tests/test_segmentation.py tests/test_pipeline.py -v`
* **Tiêu chí nghiệm thu & Checklist:**
  - [ ] 100% test cases trong `test_segmentation.py` và `test_pipeline.py` đều đạt (PASSED).
  - [ ] `BrainTumorPipeline` hỗ trợ chuyển đổi linh hoạt giữa 2 giải thuật qua cờ cấu hình `method='watershed'` hoặc `'region_growing'`.
  - [ ] Lưới ảnh so sánh đối chứng 2 giải thuật được xuất đầy đủ.

---

### 🔹 NGÀY 5: Benchmark Quy Mô Lớn (3,929 Lát Cắt) & Phân Tích Chuyên Sâu Ca Thất Bại
* **Mục tiêu:** Thực thi đánh giá định lượng trên toàn bộ 3,929 lát cắt chuẩn TCGA-LGG và phân tích toán học các ca thất bại (*Failure Cases*).
* **Nhiệm vụ cụ thể:**
  1. Phối hợp cùng Trí chạy đánh giá đa tiến trình trên toàn bộ 3,929 lát cắt (110 bệnh nhân) thông qua `scripts/run_all_experiments.py`.
  2. Phân tích định lượng số liệu thực nghiệm:
     * Watershed đạt điểm Dice trung bình **0.4446 ± 0.3014** (vượt trội gấp 2.23 lần so với Region Growing: 0.1990).
     * Độ đặc hiệu Specificity trên 2,556 lát não lành đạt **99.04%** (Watershed) và **97.60%** (Region Growing), chứng minh bước tách sọ não triệt tiêu hầu như 100% dương tính giả ngoài sọ.
  3. Lập hồ sơ phân tích chuyên sâu các nhóm ca thất bại điển hình:
     * **Nhóm u nhỏ (< 1.5% diện tích não):** Gradient biên u mờ nhạt khiến Euclidean Distance Transform sinh sure foreground bị teo nhỏ hoặc biến mất, dẫn đến under-segmentation.
     * **Nhóm u thâm nhiễm / phù não:** Vùng phù não quanh u (peritumoral edema) có mức xám gần tương đương u, khiến Region Growing lan rộng ra ngoài bờ u thực tế nếu đặt tolerance cao.
     * **Đề xuất giải pháp khắc phục:** Bổ sung lọc đẳng hướng đa tỷ lệ (multiscale vesselness/blob filter) hoặc kết hợp ngưỡng thích ứng gradient cục bộ.
* **Lệnh kiểm tra:** `python -c "import pandas as pd; df=pd.read_csv('docs/BENCHMARK_RESULTS.csv'); print(df)"`
* **Tiêu chí nghiệm thu & Checklist:**
  - [ ] Hoàn tất phân tích dữ liệu 7,858 lượt thực nghiệm.
  - [ ] Lập bảng phân tích 3 trường hợp lâm sàng điển hình (ca xuất sắc, ca trung bình, ca thất bại).
  - [ ] Soạn thảo toàn văn phần phân tích kỹ thuật phục vụ Mục 8 của Báo cáo đồ án.

---

### 🔹 NGÀY 6: Biên Soạn Báo Cáo Đồ Án Toàn Văn (4 Chương Kỹ Thuật Trọng Tâm)
* **Mục tiêu:** Hoàn thiện 4 chương kỹ thuật chuyên sâu theo cấu trúc 12 mục chuẩn của Bộ môn Khoa học Dữ liệu - HUIT.
* **Nhiệm vụ cụ thể:**
  * Trực tiếp biên soạn 4 chương trọng tâm trong Báo cáo:
    1. **Mục 2: Cơ sở lý thuyết:** Trình bày chi tiết toán học của các phép toán hình thái học (Erosion, Dilation, Opening, Closing), biến đổi khoảng cách Euclidean EDT, thuật toán Marker-controlled Watershed và nguyên lý lan truyền vùng Seeded Region Growing. Chèn công thức toán gõ chuẩn và sơ đồ nguyên lý.
    2. **Mục 4: Tiền xử lý ảnh:** Mô tả chi tiết kỹ thuật khử nhiễu Bilateral và thuật toán Tách sọ não (Skull Stripping) 6 bước. Chèn hình minh họa trực quan 6 bước trích xuất từ thực nghiệm.
    3. **Mục 6: Phương pháp và quy trình thực nghiệm:** Trình bày sơ đồ pipeline tổng thể 4 tầng, chi tiết thông số cấu hình tối ưu trong `configs/default_params.yaml`, so sánh cơ chế hoạt động của 2 thuật toán.
    4. **Mục 8 (Phần phân tích kỹ thuật):** Bình luận định tính về hình ảnh kết quả phân đoạn, phân tích bản chất toán học dẫn đến sự chênh lệch hiệu năng giữa Watershed và Region Growing, giải trình chi tiết các ca thất bại.
  * Phối hợp cùng Trí ghép nối toàn bộ 12 mục thành file `docs/BAO_CAO_DO_AN_XLAS.md` và chạy script xuất bản Word `docs/BAO_CAO_DO_AN_XLAS.docx` tuân thủ nghiêm ngặt Quy chuẩn Word HUIT (Times New Roman 13pt, giãn dòng 1.5, lề 3-3-3-2 cm).
* **Lệnh kiểm tra:** `python scripts/export_report_docx.py`
* **Tiêu chí nghiệm thu & Checklist:**
  - [ ] 4 chương kỹ thuật hoàn thiện đầy đủ công thức toán và hình ảnh minh chứng sắc nét.
  - [ ] File Word `docs/BAO_CAO_DO_AN_XLAS.docx` xuất thành công, không bị lỗi bảng biểu hay tràn lề.

---

### 🔹 NGÀY 7: Chuẩn Hóa Mã Nguồn, Đạt 12/12 Tests, Soạn Slide & Đóng Gói
* **Mục tiêu:** Rà soát chất lượng kỹ thuật mã nguồn, đảm bảo kiểm thử tự động đạt 100%, chuẩn bị slide kỹ thuật và đóng gói hồ sơ nộp.
* **Nhiệm vụ cụ thể:**
  1. Rà soát toàn diện mã nguồn trong `src/`:
     * Bổ sung đầy đủ type hints và docstring tiếng Việt chuẩn PEP8 cho 100% các hàm và lớp.
     * Dọn dẹp các biến tạm, hàm thừa không sử dụng.
  2. Chạy toàn bộ bộ kiểm thử tự động: `pytest -v` (đảm bảo cả 12/12 unit tests PASSED).
  3. Soạn phần Slide thuyết trình kỹ thuật (8–10 slides): Bối cảnh đề tài, quy trình 6 bước tách sọ não, nguyên lý 2 thuật toán phân đoạn, hình ảnh minh chứng định tính và phân tích ca lỗi.
  4. Đóng gói trọn bộ sản phẩm theo đúng quy định nộp đồ án: Mã nguồn `src/`, Notebooks, Dữ liệu thực nghiệm `data/full/`, Báo cáo (Word + PDF), Slide (PPTX + PDF), Video demo.
* **Lệnh kiểm tra:** `pytest -v`
* **Tiêu chí nghiệm thu & Checklist:**
  - [ ] Toàn bộ 12/12 unit tests PASSED (100% green).
  - [ ] Slide kỹ thuật hoàn thiện, thiết kế trực quan, súc tích.
  - [ ] Trọn bộ sản phẩm đồ án đóng gói sẵn sàng nộp đúng hạn.

---

## ✍️ CAM KẾT HOÀN THÀNH VÀ KÝ XÁC NHẬN

Tôi xin cam đoan bản kế hoạch Sprint 7 ngày trên phản ánh chính xác 100% khối lượng công việc, đóng góp kỹ thuật và tiến độ thực tế của bản thân trong đồ án môn học Xử lý ảnh số.

*TP. Hồ Chí Minh, ngày 19 tháng 10 năm 2026*  
**Nhóm trưởng**  
*(Ký và ghi rõ họ tên)*  
**Hà Mạnh Trường**
