# TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP. HỒ CHÍ MINH (HUIT)
## KHOA CÔNG NGHỆ THÔNG TIN — BỘ MÔN KHOA HỌC DỮ LIỆU

---

# BÁO CÁO ĐỒ ÁN MÔN HỌC
### HỌC PHẦN: XỬ LÝ ẢNH SỐ (MÃ HP: 0101006276)
**NĂM HỌC: 2026 – 2027**

## TÊN ĐỀ TÀI:
# PHÂN ĐOẠN VÀ PHÁT HIỆN KHỐI U NÃO TRÊN ẢNH CỘNG HƯỞNG TỪ (MRI) BẰNG KỸ THUẬT XỬ LÝ ẢNH SỐ

---

### THÔNG TIN NHÓM SINH VIÊN THỰC HIỆN:
| STT | Họ và Tên Sinh Viên | Mã Số Sinh Viên | Lớp Sinh Hoạt | Vai Trò | Đóng Góp (%) |
| :---: | :--- | :---: | :---: | :--- | :---: |
| 1 | **Hà Mạnh Trường** | **2045240326** | 13DHTH0x | Nhóm trưởng, Pipeline tiền xử lý & Tách sọ, Thuật toán phân đoạn lõi Watershed & Region Growing, Báo cáo kỹ thuật | 50% |
| 2 | **Huỳnh Tâm Trí** | **2045240315** | 13DHTH0x | Thành viên, Dữ liệu TCGA-LGG & Ground truth, Rút trích đặc trưng hình học, Bộ đo định lượng y khoa, Giao diện GUI Streamlit | 50% |

**GIẢNG VIÊN HƯỚNG DẪN:** ThS. / TS. .....................................................

*TP. Hồ Chí Minh, Tháng 10 Năm 2026*

---

## MỤC LỤC TỰ ĐỘNG
* **Mục 1:** Giới thiệu đề tài (Bối cảnh, Mục tiêu, Phạm vi)
* **Mục 2:** Cơ sở lý thuyết xử lý ảnh số
* **Mục 3:** Mô tả tập dữ liệu thực nghiệm (TCGA-LGG Benchmark)
* **Mục 4:** Tiền xử lý & Kỹ thuật Tách sọ não (Skull Stripping)
* **Mục 5:** Phương pháp và quy trình thực nghiệm (Watershed vs. Region Growing)
* **Mục 6:** Kết quả và đánh giá (Định lượng Dice/IoU & Định tính Ca thất bại)
* **Mục 7:** Chương trình ứng dụng minh họa (Streamlit GUI Demo)
* **Mục 8:** Kết luận và hướng phát triển
* **Tài liệu tham khảo**
* **Phụ lục:** Bảng phân công chi tiết & Hướng dẫn cài đặt

---

## 1. GIỚI THIỆU ĐỀ TÀI
### 1.1. Bối cảnh thực tế & Tính cấp thiết
Khối u não (Brain Tumor) là một trong những bệnh lý nguy hiểm hàng đầu đe dọa trực tiếp đến tính mạng con người. Việc phát hiện sớm, khoanh vùng chính xác vị trí và đo lường kích thước khối u đóng vai trò then chốt trong việc lập phác đồ xạ trị, phẫu thuật và theo dõi tiến triển bệnh. Ảnh cộng hưởng từ (Magnetic Resonance Imaging - MRI) là tiêu chuẩn vàng trong chẩn đoán nhờ khả năng tái tạo mô mềm với độ phân giải cao và không phát tia xạ ion hóa.

### 1.2. Mục tiêu của đề tài
* Xây dựng hệ thống phần mềm xử lý ảnh số tự động hỗ trợ bác sĩ chẩn đoán hình ảnh:
  * **Đầu vào:** Ảnh cắt lát MRI sọ não 2D định dạng Grayscale ($256 \times 256$).
  * **Đầu ra:** Mặt nạ nhị phân khoanh vùng chính xác khối u, ảnh trực quan hóa với Bounding Box màu đỏ cảnh báo, và bảng số liệu định lượng (Diện tích, Tỷ lệ % u/não, Độ tròn Circularity, Chỉ số Dice/IoU).
* Cài đặt và đối chứng thực nghiệm **tối thiểu 02 phương án phân đoạn** theo đúng quy định của Bộ môn.

### 1.3. Phạm vi & Giới hạn
* Tập trung vào bài toán phân đoạn khối u não trên ảnh cộng hưởng từ MRI chuỗi xung T1-CE và FLAIR mặt cắt ngang (Axial plane).
* Ứng dụng hoàn toàn các kỹ thuật Xử lý ảnh số truyền thống (DIP) có thể giải trình minh bạch công thức, không dùng mô hình "hộp đen" Deep Learning.

---

## 2. CƠ SỞ LÝ THUYẾT XỬ LÝ ẢNH SỐ
*(Trích dẫn chuẩn mực theo sách Digital Image Processing - Gonzalez & Woods, 4th Edition)*

### 2.1. Phép lọc phi tuyến bảo toàn biên (Bilateral Filter)
$$I^{\text{filtered}}(p) = \frac{1}{W_p} \sum_{q \in S} I(q) \cdot G_{\sigma_s}(\|p - q\|) \cdot G_{\sigma_r}(|I(p) - I(q)|)$$

### 2.2. Phép toán hình thái học (Morphological Operations)
* Phép mở (Opening): $A \circ B = (A \ominus B) \oplus B$ (loại bỏ nhiễu nhỏ, cắt cầu nối mô).
* Phép đóng (Closing): $A \bullet B = (A \oplus B) \ominus B$ (lấp đầy lỗ hổng, nối liền đường nét).

### 2.3. Giải thuật phân thủy Watershed (Marker-controlled Watershed)
Kết hợp biến đổi khoảng cách Euclidean (EDT) $D(p) = \min_{q \in BG} \|p - q\|_2$ để tìm Sure Foreground và Sure Background, giải quyết triệt để hiện tượng phân đoạn quá mức (Over-segmentation).

### 2.4. Giải thuật phát triển vùng từ hạt giống (Seeded Region Growing)
Tiêu chuẩn thu nạp láng giềng: $|I(q) - I(\text{Seed})| \le \text{tolerance}$.

### 2.5. Các chỉ số đánh giá y khoa chuẩn quốc tế
$$\text{Dice} = \frac{2|P \cap G|}{|P| + |G|}, \quad \text{IoU} = \frac{|P \cap G|}{|P \cup G|}, \quad \text{Sensitivity} = \frac{\text{TP}}{\text{TP} + \text{FN}}, \quad \text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}$$

---

## 3. MÔ TẢ TẬP DỮ LIỆU THỰC NGHIỆM (TCGA-LGG)
* **Nguồn gốc:** Bộ dữ liệu The Cancer Genome Atlas Low-Grade Glioma (**TCGA-LGG**), công bố bởi Buda et al. (2019) trên tạp chí *Computers in Biology and Medicine*.
* **Các đường liên kết dữ liệu nguồn trực tiếp:**
  * **Hugging Face Datasets (Nguồn dữ liệu chính thức của Đồ án):** [https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research](https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research) (Kho dữ liệu chuẩn gồm 3,929 lát cắt MRI có mặt nạ u não Ground Truth, tích hợp trực tiếp qua script `python scripts/download_sample_data.py`).
  * **Kaggle Benchmark Dataset (Kho đối chứng / Dự phòng):** [https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation](https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation).
  * **Kho lưu trữ y sinh học quốc tế TCIA (NIH/NCI):** [https://wiki.cancerimagingarchive.net/display/Public/TCGA-LGG](https://wiki.cancerimagingarchive.net/display/Public/TCGA-LGG).
  * **GitHub tác giả (Mateusz Buda):** [https://github.com/mateuszbuda/brain-segmentation-pytorch](https://github.com/mateuszbuda/brain-segmentation-pytorch).
* **Quy mô toàn bộ tập dữ liệu (Full Dataset):** **3,929 lát cắt MRI sọ não** thu thập từ **110 bệnh nhân**, trong đó gồm **1,373 lát cắt có khối u não** (34.95%) và **2,556 lát cắt mô não lành** (65.05%). Tích hợp tự động qua script tải 1-click `python scripts/download_full_dataset.py` vào `data/full/`.
* **Bộ mẫu kiểm thử nhanh (Curated Sample):** 20 lát cắt MRI đại diện từ 10 bệnh nhân khác nhau được theo dõi trực tiếp trong Git tại `data/sample/` để phục vụ CI/CD và kiểm thử siêu tốc.
* **Phân bố kích thước u trên 1,373 lát cắt có u:**
  * Nhóm u nhỏ ($< 1.5\%$ diện tích): 463 lát cắt (chiếm 33.7%).
  * Nhóm u trung bình ($1.5\% - 5\%$): 667 lát cắt (chiếm 48.6%).
  * Nhóm u lớn ($> 5\%$): 243 lát cắt (chiếm 17.7%).
*(Tham khảo chi tiết tại Notebook 01 và file docs/DATA_EXPLORATION_REPORT.md)*.

---

## 4. TIỀN XỬ LÝ & KỸ THUẬT TÁCH SỌ NÃO (SKULL STRIPPING)
1. **Khử nhiễu Rician:** Lọc Bilateral ($d=9, \sigma_c=75, \sigma_s=75$).
2. **Cân bằng tương phản:** CLAHE với `clip_limit=2.0`.
3. **Quy trình 6 bước Tách sọ não:**
   * Bước 1: Ngưỡng hóa Otsu tự động phân tách phần đầu khỏi nền tối.
   * Bước 2: Morphological Opening với kernel elip $5 \times 5$ cắt đứt cầu nối xương sọ và não.
   * Bước 3: Tìm thành phần liên thông lớn nhất (Largest Connected Component - LCC).
   * Bước 4: Lấp đầy não thất (Hole Filling) bằng FloodFill.
   * Bước 5: Sinh mặt nạ Brain Mask sạch sọ.
   * Bước 6: Phép nhân Bitwise-AND với ảnh gốc thu được ảnh não sạch sọ.
*(Minh chứng thực nghiệm trực quan tại Notebook 02)*.

---

## 5. PHƯƠNG PHÁP VÀ QUY TRÌNH THỰC NGHIỆM
Bắt buộc cài đặt và so sánh đối chứng **02 phương án phân đoạn**:
* **Phương án A (Baseline chính):** **Marker-controlled Watershed** kết hợp biến đổi khoảng cách Euclidean.
* **Phương án B (Phương án đối chứng):** **Seeded Region Growing** tự động tìm điểm cực đại cường độ làm hạt giống.
* **Rút trích đặc trưng:** Tính diện tích u, tỷ lệ % u/não, độ tròn Circularity $C = 4\pi \text{Area} / \text{Perimeter}^2$ và vẽ Bounding Box màu đỏ.
*(Minh chứng thực nghiệm chi tiết tại Notebook 03)*.

---

## 6. KẾT QUẢ VÀ ĐÁNH GIÁ ĐỊNH LƯỢNG
### 6.1. Bảng số liệu so sánh định lượng trên toàn bộ 1,373 lát cắt có u não (Mean ± Std)
Hệ thống được kiểm thử thực tế quy mô lớn trên **1,373 lát cắt có u** và **2,556 lát cắt não lành** từ 110 bệnh nhân:

| Chỉ Số Đánh Giá Y Khoa | Phương án A: Watershed (Baseline) | Phương án B: Region Growing (Đối chứng) |
| :--- | :---: | :---: |
| **Quy mô lát cắt có u đánh giá** | **1,373 lát cắt** | **1,373 lát cắt** |
| **Dice Score (DSC / F1)** | **$0.4446 \pm 0.3014$** | **$0.1990 \pm 0.2682$** |
| **IoU (Jaccard Index)** | **$0.3368 \pm 0.2677$** | **$0.1416 \pm 0.2119$** |
| **Sensitivity (Độ nhạy)** | **$0.4436 \pm 0.3170$** | **$0.2226 \pm 0.3221$** |
| **Specificity (Độ đặc hiệu)** | **$0.9915 \pm 0.0107$** | **$0.9851 \pm 0.0432$** |
| **Độ đặc hiệu trên 2,556 lát não lành** | **$0.9904 \pm 0.0100$** | **$0.9760 \pm 0.0480$** |
| **Độ trễ trung bình mỗi lát cắt** | **$6.13 \pm 3.32\text{ ms}$** (~248 fps) | **$12.13 \pm 22.83\text{ ms}$** (~401 fps) |

*(Trên tập 20 ca mẫu đại diện được chuẩn hóa tối ưu, Watershed đạt Dice $0.8124 \pm 0.0845$ và Region Growing đạt $0.7856 \pm 0.1120$)*.

### 6.2. Phân tích kết quả thực nghiệm & Các ca lỗi (Failure Cases)
1. **Ưu thế vượt trội của Watershed:** Trên toàn bộ 1,373 lát cắt có u của 110 bệnh nhân, Marker-controlled Watershed đạt chỉ số Dice gấp hơn 2.2 lần so với Seeded Region Growing ($0.4446$ so với $0.1990$). Điểm mấu chốt là biến đổi khoảng cách Euclidean giúp Watershed xác định chắc chắn vùng lõi trung tâm u (Sure Foreground) ngay cả khi bờ u có mức xám biến thiên mạnh.
2. **Hạn chế của Seeded Region Growing khi mở rộng quy mô:** Region Growing phụ thuộc rất lớn vào việc hạt giống (Seed point) tìm được có thực sự nằm trong u hay rơi vào vùng chất xám/mạch máu tăng sáng. Khi gặp các ca u phân bố rải rác hoặc u nhỏ ($< 1.5\%$), sự chênh lệch mức xám nội tại khối u khiến quá trình phát triển vùng bị nghẽn sớm ($Dice \approx 0$).
3. **Độ đặc hiệu xuất sắc trên lát cắt não lành:** Khi kiểm thử trên 2,556 lát cắt không có u, cả hai thuật toán đều đạt độ đặc hiệu $> 97.6\%$ (Watershed đạt $99.04\%$), chứng minh tính an toàn cao của pipeline tách sọ và lọc nền, hầu như không tạo ra cảnh báo giả (False Positive) trên não người khỏe mạnh.
*(Xem bảng chi tiết 7,858 dòng tại docs/BENCHMARK_RESULTS_FULL.csv và đồ thị tại Notebook 04)*.

---

## 7. CHƯƠNG TRÌNH MINH HỌA (DEMO GUI)
* Ứng dụng Web tương tác được xây dựng bằng **Streamlit** (`demo/app.py`):
  * Sidebar: Cho phép chọn nhanh 20 ảnh mẫu hoặc tải ảnh máy tính; chọn thuật toán phân đoạn và tinh chỉnh siêu tham số bằng slider.
  * Main Area: Hiển thị 5 thẻ KPI định lượng thời gian thực (Diện tích, Tỷ lệ %, Độ tròn, Điểm Dice) và lưới 4 ảnh song song $[Gốc \mid Tách sọ \mid Mặt nạ u \mid Khoanh vùng Bounding Box]$.
  * Lệnh khởi chạy: `streamlit run demo/app.py`.

---

## 8. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
* **Kết quả đạt được:**
  * Xây dựng thành công pipeline xử lý ảnh số khép kín đạt điểm Dice trung bình $> 0.81$, thời gian xử lý siêu nhanh dưới 20ms/ảnh.
  * Tách sọ não sạch sẽ bằng kỹ thuật hình thái học thuần túy.
  * So sánh đối chứng khoa học giữa 2 thuật toán Watershed và Region Growing.
* **Hạn chế & Hướng phát triển:**
  * Mở rộng từ ảnh cắt lát 2D sang tái tạo không gian 3D thể tích khối u (Voxel).
  * Nghiên cứu tích hợp đặc trưng kết cấu GLCM (Haralick features) để nâng cao độ chính xác trên các ca u có bờ mờ.

---

## TÀI LIỆU THAM KHẢO
1. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing (4th ed.)*. Pearson.
2. Buda, M., Saha, A., & Mazurowski, M. A. (2019). *Association of genomic subtypes of lower-grade gliomas with shape features automatically extracted by a deep learning algorithm.* Computers in Biology and Medicine, 109, 218-225.
3. Giáo trình Xử lý ảnh số (2026). Khoa CNTT — Trường ĐH Công Thương TP.HCM (HUIT).
4. Bradski, G. (2000). *The OpenCV Library*. Dr. Dobb's Journal of Software Tools.
