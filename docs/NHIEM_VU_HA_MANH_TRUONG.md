# KẾ HOẠCH & PHÂN CÔNG NHIỆM VỤ 15 TUẦN — HÀ MẠNH TRƯỜNG
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
  * Điều phối chung tiến độ làm việc của nhóm theo đúng kế hoạch 15 tuần của Bộ môn.
  * Thiết kế kiến trúc tổng thể pipeline Xử lý ảnh số (DIP).
  * Nghiên cứu cơ sở lý thuyết toán học và cài đặt module Tiền xử lý & Tách sọ não (*Skull Stripping*).
  * Cài đặt giải thuật phân đoạn u não lõi Baseline (*Marker-controlled Watershed*) và Phương án đối chứng (*Seeded Region Growing*).
  * Viết các chương kỹ thuật trong Báo cáo đồ án (Chương 2, 4, 6 và phân tích kỹ thuật Chương 8).
  * Đảm bảo tính toàn vẹn của mã nguồn xử lý ảnh và hệ thống kiểm thử đơn vị (*Unit Tests*).

---

## 🎯 ĐỐI CHIẾU VỚI RUBRIC ĐÁNH GIÁ ĐỒ ÁN MÔN HỌC (KHOA CNTT - HUIT)

Đồ án được chấm theo thang điểm 10 theo đúng Mục III trong `9. Ke_hoach_thuc_ĐA__XLAS_2026-2027.pdf`:

| Tiêu chí đánh giá | Trọng số | Đóng góp và minh chứng chính của Hà Mạnh Trường |
| :--- | :---: | :--- |
| **1. Phân tích & lựa chọn đúng phương pháp (PLO2, CLO1)** | **15% (1.5đ)** | - Phân tích đặc trưng ảnh MRI FLAIR/T1-CE, đề xuất giải pháp tách sọ não bằng hình thái học.<br>- Lựa chọn và so sánh 2 giải thuật phân đoạn kinh điển: Watershed phân thủy và Region Growing. |
| **2. Áp dụng được các phương pháp xử lý (PLO2, CLO2)** *(Trọng tâm)* | **50% (5.0đ)** | - Cài đặt bộ lọc Bilateral khử nhiễu Rician bảo toàn biên và CLAHE tăng tương phản mô não.<br>- Xây dựng pipeline 6 bước tách sọ não kinh điển triệt tiêu xương sọ.<br>- Cài đặt thuật toán phân đoạn Watershed và Region Growing kèm khảo sát siêu tham số.<br>- Đạt 100% test cases trong `tests/test_preprocessing.py` và `tests/test_segmentation.py`. |
| **3. Đọc tài liệu, nghiên cứu giải quyết bài toán (PLO4, CLO3)** | **10% (1.0đ)** | - Nghiên cứu sâu giáo trình chuẩn *Gonzalez & Woods, Digital Image Processing (4th Ed.)* các Chương 3, 5, 9, 10.<br>- Soạn thảo tài liệu đặc tả kỹ thuật toán học chi tiết [SPEC_PIPELINE_MRI.md](file:///C:/Users/xpaga/Documents/xlas/docs/SPEC_PIPELINE_MRI.md). |
| **4. Trình bày báo cáo (PLO7, CLO5)** | **15% (1.5đ)** | - Chịu trách nhiệm biên soạn 4 chương kỹ thuật trọng tâm trong Báo cáo toàn văn (Word/PDF).<br>- Trình bày sơ đồ khối pipeline, công thức toán học và ảnh chụp thực nghiệm minh chứng. |
| **5. Phân công & phối hợp làm việc nhóm (PLO6, CLO4)** | **10% (1.0đ)** | - Đảm nhiệm vai trò Nhóm trưởng: Lập kế hoạch 15 tuần, phân công rõ ràng cho thành viên.<br>- Duy trì kho mã nguồn Git, quản lý issues và review chất lượng sản phẩm trước khi tích hợp. |

---

## 🗺️ LỘ TRÌNH 15 TUẦN CHI TIẾT CỦA HÀ MẠNH TRƯỜNG

```
[Tuần 1]      Đăng ký đề tài, phân công vai trò & lập kế hoạch 15 tuần
   │
[Tuần 2–3]    Nghiên cứu lý thuyết DIP (Gonzalez & Woods), xây dựng pipeline dự kiến & SPEC
   │
[Tuần 4]      Phối hợp rà soát tập dữ liệu 3,929 lát cắt TCGA-LGG & thống nhất chuẩn nhãn
   │
[Tuần 5]      Cài đặt module Tiền xử lý & Tách sọ não (Skull Stripping) + Notebook 02
   │
[Tuần 6]      Cài đặt phương pháp chính 1 (Baseline): Marker-controlled Watershed + Unit Test
   │
[Tuần 7]      Hoàn thiện Pipeline cơ sở từ ảnh thô đến u não phân đoạn (BrainTumorPipeline)
   │
[Tuần 8]      BÁO CÁO TIẾN ĐỘ NỘI BỘ VỚI GIẢNG VIÊN (Dữ liệu, pipeline, kết quả baseline)
   │
[Tuần 9]      Cài đặt phương pháp đối chứng 2: Seeded Region Growing & khảo sát siêu tham số
   │
[Tuần 10]     Tối ưu hóa hậu xử lý hình thái học & khớp nối module đo đặc trưng của Trí
   │
[Tuần 11]     Phối hợp tích hợp toàn bộ pipeline DIP vào ứng dụng tương tác Streamlit GUI
   │
[Tuần 12]     Phân tích chuyên sâu các ca thất bại (Failure Cases) trên dữ liệu quy mô lớn
   │
[Tuần 13]     Biên soạn bản nháp Báo cáo đồ án: 4 Chương Kỹ thuật (Chương 2, 4, 6, 8 kỹ thuật)
   │
[Tuần 14]     Rà soát mã nguồn toàn bộ src/, chuẩn hóa docstrings & đảm bảo 12/12 unit tests đạt
   │
[Tuần 15]     Hoàn thiện Báo cáo bản cuối, slide thuyết trình kỹ thuật & đóng gói hồ sơ nộp
   │
[Sau kết thúc 01 tuần] NỘP TRỌN BỘ HỒ SƠ ĐỒ ÁN HOÀN CHỈNH
```

---

## 📋 NỘI DUNG THỰC HIỆN CHI TIẾT TỪNG TUẦN

### 🔹 Tuần 1: Khởi động Đề tài, Phân công Nhóm & Lập Kế hoạch
* **Nhiệm vụ:**
  1. Thống nhất chọn đề tài *Phân đoạn và phát hiện khối u não trên ảnh MRI*, đăng ký lên hệ thống của Bộ môn.
  2. Bầu Nhóm trưởng, phân chia phạm vi trách nhiệm giữa Trường và Trí theo đúng sở trường và năng lực.
  3. Lập bản kế hoạch làm việc 15 tuần chi tiết kèm tiêu chí nghiệm thu rõ ràng.
* **Sản phẩm đạt được:** Đề tài được phê duyệt; Bản phân công công việc chi tiết.

### 🔹 Tuần 2 – Tuần 3: Nghiên cứu Lý thuyết Xử lý ảnh số & Soạn thảo Đặc tả
* **Nhiệm vụ:**
  1. Đọc và tổng hợp kiến thức từ giáo trình *Digital Image Processing (4th Ed.)* của Gonzalez & Woods:
     * Chương 3: Biến đổi cường độ sáng & cân bằng thích nghi tương phản (CLAHE).
     * Chương 5: Khôi phục ảnh, lọc Bilateral bảo toàn biên đối tượng.
     * Chương 9: Hình thái học ảnh nhị phân & xám (Opening, Closing, phần tử cấu trúc đĩa elip).
     * Chương 10: Phân đoạn ảnh (Distance Transform, Watershed, Region Growing).
  2. Xây dựng sơ đồ khối quy trình xử lý 7 bước chuẩn HUIT.
  3. Soạn thảo tài liệu đặc tả kỹ thuật `docs/SPEC_PIPELINE_MRI.md` với 13 chữ ký hàm, 7 bất biến dữ liệu (I1–I7) và giải thích toán học chặt chẽ.
* **Sản phẩm đạt được:** `docs/SPEC_PIPELINE_MRI.md`, sơ đồ khối quy trình xử lý.

### 🔹 Tuần 4: Phối hợp Chuẩn bị Dữ liệu Thực nghiệm
* **Nhiệm vụ:**
  1. Phối hợp cùng Trí kiểm tra chất lượng dữ liệu đầu vào (ảnh cộng hưởng từ FLAIR/T1-CE, kích thước $256 \times 256$, dải mức xám uint8).
  2. Kiểm tra tính hợp lệ của mặt nạ nhãn Ground Truth (chỉ chứa giá trị nhị phân $\{0, 255\}$).
  3. Xác nhận hai tầng dữ liệu: `data/sample/` (20 mẫu kiểm thử nhanh) và `data/full/` (3,929 lát cắt chuẩn TCGA-LGG).
* **Sản phẩm đạt được:** Bộ dữ liệu kiểm thử được xác nhận hợp lệ.

### 🔹 Tuần 5: Cài đặt Module Tiền xử lý & Tách sọ não (Skull Stripping)
* **Nhiệm vụ:**
  1. Cài đặt các hàm lọc trong `src/preprocessing/filters.py`: `apply_bilateral_filter` ($d=9, \sigma_c=75, \sigma_s=75$) và `apply_clahe` ($\text{clip}=2.0, \text{grid}=8\times 8$).
  2. Cài đặt kỹ thuật Tách sọ não trong `src/preprocessing/skull_strip.py`:
     * Phân ngưỡng Otsu tạo mask thô.
     * Phép toán hình thái học Opening với phần tử đĩa elip ($5 \times 5$, 2 lần lặp) để cắt đứt cầu nối mô liên kết giữa hộp sọ và não.
     * Thuật toán tìm thành phần liên thông lớn nhất (Largest Connected Component - LCC) để giữ lại nhu mô não nguyên vẹn.
     * Phép toán Closing lấp đầy các rãnh vỏ não.
  3. Xây dựng và chạy hoàn thiện `notebooks/02_skull_stripping.ipynb`, xuất bộ ảnh 6 bước tách sọ chất lượng cao.
* **Sản phẩm đạt được:** `src/preprocessing/`, `notebooks/02_skull_stripping.ipynb`, `tests/test_preprocessing.py` (3/3 passed).

### 🔹 Tuần 6: Cài đặt Phương pháp Phân đoạn Chính 1 — Marker-controlled Watershed
* **Nhiệm vụ:**
  1. Cài đặt lớp `WatershedSegmenter` trong `src/segmentation/watershed.py`:
     * Áp dụng biến đổi khoảng cách Euclidean (`cv2.distanceTransform`) trên vùng não đã tách sọ.
     * Xác định vùng chắc chắn u (Sure Foreground) qua ngưỡng tỷ lệ `dist_thresh_ratio = 0.4` so với cực đại khoảng cách.
     * Xác định vùng chắc chắn nền (Sure Background) bằng phép giãn nở hình thái học (`cv2.dilate`).
     * Xác định vùng không chắc chắn (Unknown) và đánh số nhãn hạt giống (Markers).
     * Áp dụng thuật toán phân thủy `cv2.watershed` để tìm ranh giới chính xác của khối u.
  2. Xử lý an toàn các ca âm tính (lát não lành không có u).
* **Sản phẩm đạt được:** `src/segmentation/watershed.py`, `tests/test_segmentation.py` (test Watershed passed).

### 🔹 Tuần 7: Hoàn thiện Pipeline Cơ sở Từ Đầu vào Đến Đầu ra
* **Nhiệm vụ:**
  1. Xây dựng lớp điều phối trung tâm `BrainTumorPipeline` trong `src/pipeline.py`:
     * Nhận ảnh đầu vào $\rightarrow$ Lọc Bilateral $\rightarrow$ Tách sọ não $\rightarrow$ Cân bằng CLAHE $\rightarrow$ Phân đoạn u não $\rightarrow$ Trích xuất đặc trưng $\rightarrow$ Vẽ trực quan hóa cảnh báo.
  2. Kiểm tra khả năng chạy liên tục, không rò rỉ bộ nhớ, bắt lỗi ngoại lệ an toàn khi nhận ảnh rỗng hoặc sai kích thước.
* **Sản phẩm đạt được:** `src/pipeline.py` chạy ổn định trên toàn bộ các ca thử nghiệm ban đầu.

### 🔹 Tuần 8: Báo Cáo Tiến Độ Nội Bộ Với Giảng Viên Hướng Dẫn
* **Nhiệm vụ:**
  1. Tổng hợp bản báo cáo tiến độ ngắn: Tình hình dữ liệu, sơ đồ pipeline, kết quả ban đầu của phương pháp Baseline (Watershed), các vấn đề tồn tại cần cải thiện.
  2. Báo cáo trực tiếp với Giảng viên trong buổi hướng dẫn Tuần 8, tiếp thu các ý kiến đóng góp về cách xử lý các ca u bờ mờ.
  3. Lập kế hoạch tinh chỉnh cho giai đoạn nửa sau học phần.
* **Sản phẩm đạt được:** Báo cáo tiến độ nội bộ hoàn thành; Biên bản ghi nhận ý kiến giảng viên.

### 🔹 Tuần 9: Cài đặt Phương pháp Đối chứng 2 — Seeded Region Growing & Tinh chỉnh
* **Nhiệm vụ:**
  1. Cài đặt lớp `RegionGrowingSegmenter` trong `src/segmentation/region_growing.py`:
     * Hàm tự động tìm điểm hạt giống cực đại cường độ `find_seed_point()` trong vùng não đã lọc sọ.
     * Thuật toán lan truyền vùng theo láng giềng 8 điểm (8-connectivity) dựa trên ngưỡng dung sai `intensity_tolerance = 15`.
     * Bộ lọc diện tích u hợp lệ `[min_tumor_area, max_tumor_area] = [50, 25000]` pixels.
  2. Khảo sát siêu tham số: Thay đổi tolerance từ 10 đến 25, kích thước kernel từ 3 đến 7.
  3. Xây dựng và chạy hoàn thiện `notebooks/03_tumor_segmentation_comparison.ipynb`, tạo lưới ảnh so sánh song song giữa Watershed và Region Growing.
* **Sản phẩm đạt được:** `src/segmentation/region_growing.py`, `notebooks/03_tumor_segmentation_comparison.ipynb`.

### 🔹 Tuần 10: Tối ưu Hậu xử lý & Khớp nối Hệ thống Đo lường
* **Nhiệm vụ:**
  1. Bổ sung các bước hậu xử lý hình thái học (Morphological Filtering) để làm mịn đường biên u và xóa các đảo pixel cô lập sau phân đoạn.
  2. Khớp nối mặt nạ u đầu ra với module đo đặc trưng hình học của Trí (`src/measurement/features.py`), đảm bảo định dạng contour và bounding box chuẩn.
* **Sản phẩm đạt được:** Pipeline liên kết mượt mà với module đo lường.

### 🔹 Tuần 11: Phối hợp Tích hợp Demo Streamlit GUI Hoàn Chỉnh
* **Nhiệm vụ:**
  1. Hỗ trợ Trí tích hợp `BrainTumorPipeline` vào giao diện web Streamlit `demo/app.py`.
  2. Tối ưu hóa hiệu năng nạp ảnh và hiển thị các bước trung gian (ảnh gốc, ảnh tách sọ, mặt nạ u, ảnh phủ viền đỏ cảnh báo) theo thời gian thực (< 100 ms).
* **Sản phẩm đạt được:** Ứng dụng demo tương tác hoàn chỉnh.

### 🔹 Tuần 12: Đánh Giá Quy Mô Lớn & Phân Tích Chuyên Sâu Các Ca Thất Bại
* **Nhiệm vụ:**
  1. Chạy thực nghiệm phân đoạn trên toàn bộ 3,929 lát cắt dữ liệu TCGA-LGG thông qua script xử lý đa tiến trình `scripts/run_all_experiments.py`.
  2. Thực hiện phân tích chuyên sâu các ca thất bại (Failure Cases):
     * *Nhóm u nhỏ (< 1.5% diện tích não):* Phân tích hiện tượng mất dấu vết biên khi độ chênh lệch mức xám thấp.
     * *Nhóm u lớn (> 5% diện tích não):* Phân tích hiệu ứng chèn ép não thất và phù não quanh u.
     * *Lát não lành (không u):* Khẳng định độ đặc hiệu Specificity đạt 99.04%, chứng minh bước tách sọ não loại bỏ 100% báo động giả ngoài sọ.
* **Sản phẩm đạt được:** Bảng phân tích chi tiết các ca thất bại, nguyên nhân và bài học kinh nghiệm.

### 🔹 Tuần 13: Biên Soạn Bản Nháp Báo Cáo Đồ Án (4 Chương Kỹ Thuật Trọng Tâm)
* **Nhiệm vụ:**
  * Trực tiếp biên soạn 4 chương kỹ thuật trọng tâm theo cấu trúc 12 mục chuẩn của Bộ môn:
    * **Mục 4: Cơ sở lý thuyết:** Trình bày toán học phép toán hình thái học, biến đổi khoảng cách Euclidean, thuật toán Watershed và nguyên lý Region Growing.
    * **Mục 6: Tiền xử lý ảnh:** Mô tả chi tiết kỹ thuật khử nhiễu Bilateral và thuật toán Tách sọ não (Skull Stripping), đính kèm sơ đồ khối và hình ảnh 6 bước thực nghiệm.
    * **Mục 7: Phương pháp và quy trình thực nghiệm:** Trình bày sơ đồ pipeline 7 bước, bảng thông số cấu hình và so sánh chi tiết giữa 2 giải thuật.
    * **Mục 8 (Phần phân tích kỹ thuật):** Bình luận định tính về hình ảnh kết quả phân đoạn, đối chiếu ưu/nhược điểm bản chất giữa Watershed và Region Growing.
* **Sản phẩm đạt được:** Bản nháp 4 chương kỹ thuật đầy đủ công thức toán và hình ảnh minh chứng.

### 🔹 Tuần 14: Rà Soát Mã Nguồn Kỹ Thuật, Chuẩn Hóa Docstrings & Chốt Kết Quả
* **Nhiệm vụ:**
  1. Kiểm tra toàn bộ mã nguồn trong `src/`: Bổ sung 100% chú thích tiếng Việt, chuẩn hóa type hints, loại bỏ mã thừa, tuân thủ nghiêm ngặt chuẩn PEP8.
  2. Chạy toàn bộ bộ kiểm thử tự động: `pytest -v` (đảm bảo 12/12 unit tests đều PASSED).
  3. Cùng Trí chốt lại toàn bộ các bảng số liệu định lượng (Dice, IoU, Sensitivity, Specificity, Latency) đưa vào báo cáo bản cuối.
* **Sản phẩm đạt được:** Bộ mã nguồn kỹ thuật chuẩn hóa, kiểm thử tự động đạt 100%.

### 🔹 Tuần 15: Hoàn Thiện Báo Cáo Bản Cuối, Slide Thuyết Trình & Đóng Gói
* **Nhiệm vụ:**
  1. Ghép nối và rà soát Báo cáo toàn văn bản cuối, xuất file Word `BAO_CAO_DO_AN_XLAS.docx` chuẩn lề 3-3-3-2 cm và xuất file PDF.
  2. Thiết kế phần Slide thuyết trình kỹ thuật (8–10 slides): Bối cảnh đề tài, quy trình tách sọ não, nguyên lý 2 thuật toán phân đoạn, hình ảnh minh chứng và phân tích ca lỗi.
  3. Đóng gói toàn bộ sản phẩm theo đúng cấu trúc thư mục quy định của Bộ môn.
* **Sản phẩm đạt được:** Báo cáo bản cuối (Word + PDF), Slide thuyết trình, Bộ hồ sơ đóng gói hoàn chỉnh.

### 🔹 Sau Khi Kết Thúc Học Phần 01 Tuần: Nộp Đồ Án Chính Thức
* **Nhiệm vụ:** Nộp trọn bộ hồ sơ đồ án đúng hạn trên hệ thống của Trường: Code + Dữ liệu/Link + Demo GUI + Báo cáo + Slide. Sẵn sàng cho buổi bảo vệ đồ án trước Hội đồng chấm thi.
