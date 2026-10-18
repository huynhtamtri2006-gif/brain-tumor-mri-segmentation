# LỘ TRÌNH 7 NGÀY HOÀN THÀNH ĐỒ ÁN — HÀ MẠNH TRƯỜNG
## Thành viên phụ trách: HÀ MẠNH TRƯỜNG (MSSV: 2045240326)
* **Vai trò:** Nhóm trưởng — Chịu trách nhiệm kiến trúc kỹ thuật, Thuật toán Xử lý ảnh số (Core DIP), Pipeline Tách sọ & Phân đoạn u, Quản lý Unit Tests Kỹ thuật và 4 Chương Kỹ thuật trong Báo cáo.
* **Thời gian thực hiện:** Chiến dịch 7 ngày liên tục.
* **Phạm vi file phụ trách chính:**
  * `configs/default_params.yaml` (Cấu hình tham số DIP)
  * `src/preprocessing/filters.py` & `src/preprocessing/skull_strip.py`
  * `src/segmentation/base.py`, `src/segmentation/watershed.py`, `src/segmentation/region_growing.py`
  * `src/pipeline.py` (Lớp điều phối)
  * `notebooks/02_skull_stripping.ipynb` & `notebooks/03_tumor_segmentation_comparison.ipynb`
  * `tests/test_preprocessing.py` & `tests/test_segmentation.py`
  * `docs/SPEC_PIPELINE_MRI.md`

---

## 🗺️ TỔNG QUAN PHÂN CHIA TRÁCH NHIỆM 7 NGÀY (TRƯỜNG)

```
[NGÀY 1] Rà Soát Config & Soạn Thảo Đặc Tả Kỹ Thuật Pipeline (SPEC_PIPELINE_MRI.md)
    │
[NGÀY 2] Hoàn Thiện Module Tiền Xử Lý & Tách Sọ Não + Notebook 02_skull_stripping.ipynb
    │
[NGÀY 3] Hoàn Thiện Thuật Toán Phân Đoạn Baseline 1: Watershed + Unit Test
    │
[NGÀY 4] Hoàn Thiện Thuật Toán Phân Đoạn Đối Chứng 2: Region Growing + Notebook 03
    │
[NGÀY 5] Chạy Pipeline Trên 20 Mẫu, Phân Tích Các Ca Lỗi (Failure Cases) & Ca U Nhỏ
    │
[NGÀY 6] Viết Báo Cáo Đồ Án: 4 Chương Kỹ Thuật (Chương 2, 4, 5 & Phần Kỹ Thuật Chương 6)
    │
[NGÀY 7] Soạn Slide Kỹ Thuật DIP, Rà Soát Docstring Toàn Bộ src/ & Tổng Duyệt Hệ Thống
```

---

## 📋 CHI TIẾT TỪNG NGÀY & CHECKLIST CỦA TRƯỜNG

### 🔹 NGÀY 1: Rà Soát Kiến Trúc & Biên Soạn Đặc Tả Kỹ Thuật (`SPEC_PIPELINE_MRI.md`)
* **Nhiệm vụ cụ thể:**
  1. Kiểm tra file cấu hình `configs/default_params.yaml`, đảm bảo các giá trị mặc định (kernel size, clip limit, dist ratio, tolerance) khớp với lý thuyết Gonzalez & Woods.
  2. Soạn thảo tài liệu đặc tả kỹ thuật `docs/SPEC_PIPELINE_MRI.md`:
     * Nguyên lý toán học của bộ lọc Bilateral: hàm trọng số không gian và hàm trọng số mức xám.
     * Thuật toán tách sọ não: Giải thích chi tiết phép toán hình thái học Opening, cấu trúc phần tử đĩa elip và thuật toán tìm thành phần liên thông lớn nhất (LCC).
     * Thuật toán Marker-controlled Watershed: Biến đổi khoảng cách Euclidean Distance Transform, cách tạo Sure Foreground và Sure Background.
     * Thuật toán Seeded Region Growing: Tiêu chuẩn tìm cực đại cường độ và điều kiện thu nạp láng giềng 8 điểm.
* **Lệnh kiểm tra:** `python -c "import yaml; print(yaml.safe_load(open('configs/default_params.yaml')))"`
* **Checklist hoàn thành Ngày 1:**
  - [ ] Nộp xác nhận đề tài trên Google Classroom.
  - [ ] Hoàn thành tài liệu `docs/SPEC_PIPELINE_MRI.md`.
  - [ ] Khớp nối hợp đồng hàm với Trí (không thay đổi signature trong `src/`).

---

### 🔹 NGÀY 2: Hoàn Thiện Module Tiền Xử Lý, Tách Sọ Não & Notebook 02
* **Nhiệm vụ cụ thể:**
  1. Rà soát và tối ưu mã nguồn trong `src/preprocessing/filters.py` và `src/preprocessing/skull_strip.py`.
  2. Chạy kiểm thử tự động module tiền xử lý: `pytest tests/test_preprocessing.py -v`.
  3. Mở và chạy toàn bộ notebook `notebooks/02_skull_stripping.ipynb`:
     * Kiểm tra hiển thị trực quan 6 bước tách sọ trên ca mẫu 01.
     * Chạy kiểm thử tính bền vững trên 4 ca bệnh khác nhau (u ở các vị trí khác nhau).
     * Xuất các hình ảnh trung gian lưu vào thư mục báo cáo.
* **Lệnh kiểm tra:** `pytest tests/test_preprocessing.py -v`
* **Checklist hoàn thành Ngày 2:**
  - [ ] 100% test trong `test_preprocessing.py` đều đạt (PASSED).
  - [ ] Chạy mượt mà `notebooks/02_skull_stripping.ipynb` không phát sinh lỗi.
  - [ ] Lưu bộ ảnh 6 bước tách sọ chất lượng cao để chèn vào Báo cáo Chương 4.

---

### 🔹 NGÀY 3: Hoàn Thiện Thuật Toán Phân Đoạn Baseline 1 — Watershed Phân Thủy
* **Nhiệm vụ cụ thể:**
  1. Tinh chỉnh thuật toán Watershed trong `src/segmentation/watershed.py`:
     * Khảo sát tham số `dist_thresh_ratio` từ 0.2 đến 0.6 để tìm ngưỡng tối ưu cho u não.
     * Xử lý trường hợp đặc biệt: vùng não không chứa điểm u (trả về mặt nạ rỗng an toàn).
  2. Chạy kiểm thử tự động: `pytest tests/test_segmentation.py -k watershed -v`.
  3. Bắt đầu chạy thử nghiệm phần Watershed trong `notebooks/03_tumor_segmentation_comparison.ipynb`.
* **Lệnh kiểm tra:** `pytest tests/test_segmentation.py -v`
* **Checklist hoàn thành Ngày 3:**
  - [ ] Test `test_watershed_segmentation` đạt kết quả PASSED.
  - [ ] Thuật toán Watershed phân đoạn thành công trên các ca u kích thước trung bình và lớn.

---

### 🔹 NGÀY 4: Hoàn Thiện Thuật Toán Đối Chứng 2 — Region Growing & Notebook 03
* **Nhiệm vụ cụ thể:**
  1. Tinh chỉnh thuật toán phát triển vùng trong `src/segmentation/region_growing.py`:
     * Tối ưu hóa hàm `find_seed_point()`: Đảm bảo hạt giống luôn rơi vào tâm vùng u sáng nhất.
     * Khảo sát tham số `tolerance` từ 10 đến 25 trong `configs/default_params.yaml`.
  2. Chạy kiểm thử tự động: `pytest tests/test_segmentation.py -k region_growing -v`.
  3. Hoàn thiện toàn bộ nội dung notebook `notebooks/03_tumor_segmentation_comparison.ipynb`:
     * So sánh song song Watershed vs Region Growing trên 3 nhóm: Ca u nhỏ (ca 11), Ca u trung bình (ca 02), Ca u lớn (ca 07).
     * Xuất lưới ảnh so sánh chất lượng cao để chuẩn bị cho Báo cáo Chương 5.
* **Lệnh kiểm tra:** `pytest tests/test_segmentation.py -v`
* **Checklist hoàn thành Ngày 4:**
  - [ ] 100% test trong `test_segmentation.py` đều đạt (PASSED).
  - [ ] Chạy thành công toàn bộ `notebooks/03_tumor_segmentation_comparison.ipynb`.
  - [ ] Đúc kết bảng nhận xét ưu nhược điểm định tính giữa 2 phương pháp.

---

### 🔹 NGÀY 5: Phân Tích Chuyên Sâu Các Ca Lỗi (Failure Cases) & Tích Hợp Pipeline
* **Nhiệm vụ cụ thể:**
  1. Phối hợp cùng Trí chạy đánh giá toàn diện trên 20 mẫu ảnh thông qua `src/pipeline.py`.
  2. Lập danh sách phân tích chuyên sâu các ca lỗi điển hình (Failure Cases):
     * **Ca u nhỏ (< 1.5% diện tích):** Phân tích nguyên nhân tại sao Watershed dễ bị over-segmentation hoặc under-segmentation khi gradient bờ u yếu.
     * **Ca u bờ mờ / xâm lấn:** Phân tích tại sao Region Growing có xu hướng lan truyền ra mô xám bình thường nếu đặt dung sai quá cao.
     * **Giải pháp khắc phục:** Đề xuất giải pháp cải tiến (ví dụ: tinh chỉnh ngưỡng thích ứng cục bộ, kết hợp thông tin gradient).
* **Lệnh kiểm tra:** `python -c "from src.pipeline import BrainTumorPipeline; print('Pipeline OK')"`
* **Checklist hoàn thành Ngày 5:**
  - [ ] Hoàn thành bảng phân tích 3 ca bệnh đặc biệt (1 ca xuất sắc, 1 ca trung bình, 1 ca thất bại).
  - [ ] Soạn thảo bản nháp phần "Phân tích trường hợp thất bại" để đưa vào Mục 6 của Báo cáo.

---

### 🔹 NGÀY 6: Biên Soạn Báo Cáo Đồ Án (4 Chương Kỹ Thuật Trọng Tâm)
* **Nhiệm vụ cụ thể:**
  * Chịu trách nhiệm viết 4 chương nòng cốt trong Báo cáo đồ án chuẩn Khoa CNTT (Word/PDF):
    1. **Mục 2: Cơ sở lý thuyết:** Trình bày chi tiết toán học của phép toán hình thái học (Erosion, Dilation, Opening, Closing), biến đổi khoảng cách Euclidean, giải thuật phân thủy Watershed và nguyên lý phát triển vùng Region Growing. Có sơ đồ khối và hình minh họa.
    2. **Mục 4: Tiền xử lý ảnh:** Thuyết minh quy trình khử nhiễu Bilateral và kỹ thuật Tách sọ não (Skull Stripping), chèn hình minh họa 6 bước trích xuất từ Notebook 02.
    3. **Mục 5: Phương pháp và quy trình thực nghiệm:** Trình bày sơ đồ khối pipeline tổng thể, mô tả chi tiết 2 phương pháp đối chứng (Watershed vs Region Growing), bảng tham số đã chọn từ `configs/default_params.yaml`.
    4. **Mục 6 (Phần kỹ thuật): Phân tích định tính & Các trường hợp thất bại:** Bình luận chi tiết hình ảnh kết quả phân đoạn, phân tích nguyên nhân lỗi và so sánh bản chất 2 thuật toán.
* **Checklist hoàn thành Ngày 6:**
  - [ ] Hoàn tất 4 chương kỹ thuật, đảm bảo đầy đủ hình ảnh minh chứng và công thức toán học gõ chuẩn Equation.
  - [ ] Chuyển giao các chương kỹ thuật cho Trí để ghép nối vào bản báo cáo tổng hợp duy nhất.

---

### 🔹 NGÀY 7: Soạn Slide Thuyết Trình Kỹ Thuật, Tối Ưu Mã Nguồn & Đóng Gói
* **Nhiệm vụ cụ thể:**
  1. Soạn phần Slide thuyết trình của mình (khoảng 8–10 slides):
     * Bối cảnh kỹ thuật và mục tiêu xử lý ảnh y tế.
     * Sơ đồ khối pipeline 4 tầng của hệ thống.
     * Trực quan hóa quy trình tách sọ não kinh điển.
     * So sánh cơ chế Watershed vs Region Growing.
     * Minh họa các ca phân đoạn thành công và phân tích ca lỗi.
  2. Rà soát, dọn dẹp mã nguồn trong `src/preprocessing/` và `src/segmentation/`:
     * Đảm bảo 100% hàm có docstring chuẩn tiếng Việt và type hints.
     * Xóa các biến thừa, đảm bảo tuân thủ chuẩn PEP8.
  3. Chạy lại toàn bộ test suite lần cuối: `pytest tests/ -v` (đảm bảo 12/12 test PASSED).
* **Lệnh kiểm tra:** `pytest tests/ -v`
* **Checklist hoàn thành Ngày 7:**
  - [ ] Slide phần kỹ thuật hoàn tất, sẵn sàng thuyết trình trước hội đồng.
  - [ ] Mã nguồn sạch sẽ, vượt qua 100% unit tests.
  - [ ] Họp tổng kết cùng Trí, sẵn sàng nộp đồ án.
