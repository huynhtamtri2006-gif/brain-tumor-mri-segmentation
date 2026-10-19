# TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP. HỒ CHÍ MINH (HUIT)
## KHOA CÔNG NGHỆ THÔNG TIN — BỘ MÔN KHOA HỌC DỮ LIỆU

---

# 1. TRANG BÌA: BÁO CÁO ĐỒ ÁN MÔN HỌC
### HỌC PHẦN: XỬ LÝ ẢNH SỐ (MÃ HP: 0101006276)
**NĂM HỌC: 2026 – 2027**

## TÊN ĐỀ TÀI:
# PHÂN ĐOẠN VÀ PHÁT HIỆN KHỐI U NÃO TRÊN ẢNH CỘNG HƯỞNG TỪ (MRI) BẰNG KỸ THUẬT XỬ LÝ ẢNH SỐ

---

### DANH SÁCH THÀNH VIÊN VÀ PHÂN CÔNG CÔNG VIỆC:
| STT | Họ và Tên Sinh Viên | Mã Số Sinh Viên | Lớp Sinh Hoạt | Vai Trò | Trách Nhiệm Trọng Tâm (Sprint 7 Ngày) | Tỷ Lệ Đóng Góp (%) |
| :---: | :--- | :---: | :---: | :---: | :--- | :---: |
| 1 | **Hà Mạnh Trường** | **2045240326** | 15DHKHDL03 | **Nhóm trưởng** | Quản lý tiến độ Sprint 7 ngày, Pipeline tiền xử lý & Tách sọ (Skull Stripping), Giải thuật phân đoạn u Baseline (Watershed) & Đối chứng (Region Growing), Báo cáo kỹ thuật (Mục 4, 6, 7, 8 kỹ thuật) | **50%** |
| 2 | **Huỳnh Tâm Trí** | **2045240315** | 15DHKHDL03 | **Thành viên** | Thu thập & quản lý dữ liệu 3,929 lát TCGA-LGG, Rút trích đặc trưng hình học (Area, Circularity, Bounding Box), Bộ đo định lượng y khoa (Dice, IoU, Sens, Spec), Giao diện Streamlit GUI, Báo cáo tổng quan (Mục 3, 5, 8 số liệu, 9, 10), Slide & Video demo | **50%** |

**GIẢNG VIÊN HƯỚNG DẪN:** ThS. / TS. .....................................................

*TP. Hồ Chí Minh, Năm học 2026 – 2027*

---

# 2. MỤC LỤC
*(Cấu trúc chuẩn hóa 12 mục theo đúng Mục II.3 trong Kế hoạch thực hiện Đồ án XLAS 2026–2027 của Khoa CNTT - HUIT)*

* **1. Trang bìa** (Tên đề tài, danh sách thành viên, phân công công việc)
* **2. Mục lục**
* **3. Giới thiệu đề tài** (Bối cảnh thực tế, mục tiêu, phạm vi bài toán)
* **4. Cơ sở lý thuyết** (Bộ lọc Bilateral, Hình thái học, Watershed, Region Growing, Bộ đo định lượng y sinh)
* **5. Mô tả dữ liệu** (Nguồn TCGA-LGG, liên kết Hugging Face/Kaggle, quy mô 3,929 lát cắt, phân bố u & ground truth)
* **6. Tiền xử lý ảnh** (Khử nhiễu Rician, Cân bằng CLAHE, Quy trình 6 bước Tách sọ não Skull Stripping)
* **7. Phương pháp và quy trình thực nghiệm** (Sơ đồ pipeline 7 bước, Baseline Watershed vs. Region Growing, Siêu tham số YAML)
* **8. Kết quả và đánh giá** (Bảng số liệu 3,929 lát cắt, phân tích định tính ca thất bại, độ đặc hiệu trên não lành 99.04%)
* **9. Chương trình minh họa** (Giao diện Streamlit GUI tương tác, thẻ KPI, so sánh trực quan, hướng dẫn chạy)
* **10. Kết luận** (Kết quả đạt được, đóng góp cốt lõi, hạn chế & hướng phát triển)
* **11. Tài liệu tham khảo** (Gonzalez & Woods, Buda et al., Giáo trình HUIT, OpenCV)
* **12. Phụ lục** (Khung Rubric 5 tiêu chí của HUIT, Bảng kế hoạch Sprint cấp tốc 7 ngày chi tiết, Hướng dẫn cài đặt và chạy thử hệ thống)

---

# 3. GIỚI THIỆU ĐỀ TÀI

### 3.1. Bối cảnh thực tế & Tính cấp thiết
Khối u não (Brain Tumor: u tế bào đệm - Glioma, u màng não - Meningioma, u tuyến yên - Pituitary) là một trong những bệnh lý thần kinh nguy hiểm hàng đầu đe dọa trực tiếp đến tính mạng con người. Việc phát hiện sớm, khoanh vùng chính xác vị trí và đo lường kích thước khối u đóng vai trò then chốt trong việc lập phác đồ xạ trị, phẫu thuật và theo dõi tiến triển bệnh. Ảnh cộng hưởng từ (Magnetic Resonance Imaging - MRI) là tiêu chuẩn vàng trong chẩn đoán nhờ khả năng tái tạo mô mềm với độ tương phản cao và không gây phơi nhiễm bức xạ ion hóa. Tuy nhiên, việc đọc và khoanh vùng khối u thủ công qua hàng trăm lát cắt mỗi ca chụp tốn rất nhiều thời gian và dễ sai lệch do chủ quan của bác sĩ.

### 3.2. Mục tiêu của đề tài
* Xây dựng hệ thống phần mềm xử lý ảnh số tự động hỗ trợ chẩn đoán khối u não trên ảnh MRI:
  * **Đầu vào:** Ảnh cắt lát MRI sọ não 2D định dạng Grayscale ($256 \times 256$) ở chuỗi xung FLAIR và T1-CE.
  * **Đầu ra:** Mặt nạ nhị phân phân đoạn khối u (Binary Mask), đường bao contour và Hộp giới hạn (Bounding Box) màu đỏ cảnh báo, cùng bảng số liệu định lượng (Diện tích, Tỷ lệ % u/não, Độ tròn bờ u Circularity, Chỉ số Dice/IoU).
* Cài đặt và đối chứng thực nghiệm **tối thiểu 02 phương án phân đoạn** (Marker-controlled Watershed vs. Seeded Region Growing) theo đúng quy định của Bộ môn.

### 3.3. Phạm vi & Giới hạn
* Tập trung vào bài toán phân đoạn khối u não trên ảnh cộng hưởng từ MRI mặt cắt ngang (Axial plane).
* Ứng dụng hoàn toàn các kỹ thuật **Xử lý ảnh số truyền thống (DIP)** có thể giải trình minh bạch công thức, không dùng mô hình "hộp đen" Deep Learning làm lõi xử lý, tuân thủ nghiêm ngặt quy tắc vàng của Bộ môn.

---

# 4. CƠ SỞ LÝ THUYẾT
*(Trích dẫn chuẩn mực theo giáo trình Digital Image Processing - Gonzalez & Woods, 4th Edition)*

### 4.1. Phép lọc phi tuyến bảo toàn biên (Bilateral Filter)
Để khử nhiễu Rician đặc trưng trên ảnh MRI mà không làm nhòe ranh giới mong manh giữa khối u và mô não lành, hệ thống sử dụng bộ lọc Bilateral kết hợp khoảng cách không gian và độ chênh lệch mức xám:
$$I^{\text{filtered}}(p) = \frac{1}{W_p} \sum_{q \in S} I(q) \cdot \exp\left(-\frac{\|p - q\|^2}{2\sigma_s^2}\right) \cdot \exp\left(-\frac{|I(p) - I(q)|^2}{2\sigma_r^2}\right)$$
Trong đó $\sigma_s = 75$ kiểm soát bán kính láng giềng, $\sigma_r = 75$ kiểm soát độ nhạy mức xám, $W_p$ là thừa số chuẩn hóa tổng trọng số bằng 1.

### 4.2. Phép toán hình thái học (Morphological Operations)
* **Phép mở (Opening):** $A \circ B = (A \ominus B) \oplus B$ (Co ảnh rồi Giãn ảnh) với phần tử cấu trúc đĩa elip ($5 \times 5$, 2 lần lặp), có tác dụng cắt đứt các cầu nối mô liên kết giữa hộp sọ và màng não, xóa các đốm nhiễu nhỏ ngoài sọ.
* **Phép đóng (Closing):** $A \bullet B = (A \oplus B) \ominus B$ (Giãn ảnh rồi Co ảnh) giúp lấp đầy các rãnh vỏ não và nối liền các đường nét đứt gãy.

### 4.3. Giải thuật phân thủy Marker-controlled Watershed
Để giải quyết triệt để hiện tượng phân đoạn quá mức (Over-segmentation) của thuật toán Watershed truyền thống, hệ thống áp dụng biến đổi khoảng cách Euclidean (EDT):
$$D(p) = \min_{q \in \text{Background}} \|p - q\|_2$$
Từ bản đồ khoảng cách, xác định vùng chắc chắn u (Sure Foreground) qua ngưỡng tỷ lệ $\text{Thresh} = 0.4 \times \max(D)$. Vùng chắc chắn nền (Sure Background) thu được bằng phép giãn nở hình thái học. Đánh dấu nhãn hạt giống (Markers) và cho lan truyền đường phân thủy theo gradient ảnh.

### 4.4. Giải thuật phát triển vùng từ hạt giống (Seeded Region Growing)
Hệ thống tự động tìm điểm hạt giống $\text{Seed} = (y_0, x_0)$ là vị trí có cường độ sáng cực đại trong vùng não đã lọc sọ. Quá trình lan truyền duyệt láng giềng 8 điểm theo điều kiện:
$$|I(q) - I(\text{Seed})| \le \text{tolerance} \quad (\text{tolerance} = 15)$$
Kèm bộ lọc điều kiện diện tích khối u hợp lệ: $50 \le \text{Area} \le 25,000$ pixels.

### 4.5. Các chỉ số đánh giá định lượng y sinh chuẩn quốc tế
* **Dice Similarity Coefficient (DSC / F1-Score):** $\text{Dice} = \frac{2|P \cap G|}{|P| + |G|}$
* **Jaccard Index (Intersection over Union - IoU):** $\text{IoU} = \frac{|P \cap G|}{|P \cup G|}$
* **Sensitivity (Độ nhạy / Recall):** $\text{Sensitivity} = \frac{\text{TP}}{\text{TP} + \text{FN}}$
* **Specificity (Độ đặc hiệu):** $\text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}$

---

# 5. MÔ TẢ DỮ LIỆU (TCGA-LGG BENCHMARK)

### 5.1. Nguồn gốc & Liên kết tải dữ liệu chính thức
Dữ liệu thực nghiệm của đồ án được trích xuất từ bộ dữ liệu chuẩn quốc tế **TCGA-LGG** (The Cancer Genome Atlas Low-Grade Glioma), công bố bởi tác giả Mateusz Buda et al. (2019) trên tạp chí *Computers in Biology and Medicine*:
1. **Hugging Face Datasets (Nguồn chính của Đồ án):** [https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research](https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research) (Gồm 3,929 lát cắt MRI có mặt nạ u não Ground Truth, tích hợp qua script tải tự động `python scripts/download_full_dataset.py`).
2. **Kaggle Benchmark Dataset (Kho đối chứng / Dự phòng):** [https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation](https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation).
3. **Viện Y tế Quốc gia Hoa Kỳ TCIA (NIH/NCI):** [https://wiki.cancerimagingarchive.net/display/Public/TCGA-LGG](https://wiki.cancerimagingarchive.net/display/Public/TCGA-LGG).

### 5.2. Cấu trúc tổ chức dữ liệu thực nghiệm
Toàn bộ dữ liệu thực nghiệm của đồ án được lưu trữ tập trung tại thư mục `data/full/`:
* Toàn bộ **3,929 lát cắt chuẩn TCGA-LGG từ 110 bệnh nhân**, gồm ảnh PNG $256 \times 256$, mặt nạ nhị phân Ground Truth và bảng `metadata.csv` chi tiết được theo dõi trong Git.
* Dữ liệu được tích hợp tải tự động qua kịch bản `python scripts/download_full_dataset.py`.


### 5.3. Thống kê phân bố dữ liệu thực nghiệm
* **Tổng số lát cắt:** 3,929 lát cắt (110 bệnh nhân).
* **Lát cắt có khối u (Positive):** 1,373 lát cắt (34.95%).
  * Diện tích u nhỏ nhất (Min): 7 pixels (0.01% diện tích não).
  * Diện tích u lớn nhất (Max): 7,929 pixels (12.10% diện tích não).
  * Trung vị diện tích u (Median): 1,529.0 pixels (2.33% diện tích não).
  * Trung bình diện tích u (Mean): 1,931.4 pixels (2.95% diện tích não).
* **Lát cắt não lành (Healthy / Negative):** 2,556 lát cắt (65.05%).
* **Phân bố kích thước u trên 1,373 lát có u:**
  * Khối u nhỏ ($< 1.5\%$ diện tích): 463 lát cắt (33.72%).
  * Khối u trung bình ($1.5\% - 5.0\%$ diện tích): 667 lát cắt (48.58%).
  * Khối u lớn ($> 5.0\%$ diện tích): 243 lát cắt (17.70%).

---

# 6. TIỀN XỬ LÝ ẢNH

Quy trình tiền xử lý ảnh gồm 3 công đoạn cốt lõi:
1. **Khử nhiễu Rician:** Áp dụng bộ lọc Bilateral ($d=9, \sigma_c=75, \sigma_s=75$) trên ảnh xám chuẩn hóa $256 \times 256$.
2. **Cân bằng tương phản thích nghi:** Áp dụng thuật toán CLAHE với giới hạn tương phản `clip_limit=2.0` và kích thước khối `tile_grid_size=(8, 8)`.
3. **Quy trình 6 bước Tách sọ não (Skull Stripping):**
   * *Bước 1:* Phân ngưỡng Otsu tự động tạo mặt nạ thô phần đầu.
   * *Bước 2:* Morphological Opening với phần tử đĩa elip ($5 \times 5$, 2 lần lặp) cắt đứt cầu nối mô giữa xương sọ và não.
   * *Bước 3:* Thuật toán tìm thành phần liên thông lớn nhất (LCC) để giữ lại nhu mô não nguyên vẹn.
   * *Bước 4:* Lấp đầy các lỗ khuyết não thất bằng phép toán FloodFill.
   * *Bước 5:* Phép toán Morphological Closing lấp đầy rãnh vỏ não, sinh mặt nạ Brain Mask sạch sọ.
   * *Bước 6:* Nhân Bitwise-AND giữa mặt nạ Brain Mask và ảnh gốc để loại bỏ 100% xương sọ và da đầu.
*(Minh chứng thực nghiệm 6 bước được trực quan hóa đầy đủ trong Notebook 02)*.

---

# 7. PHƯƠNG PHÁP VÀ QUY TRÌNH THỰC NGHIỆM

Hệ thống xây dựng theo mô hình pipeline 7 bước khép kín và so sánh đối chứng 2 phương án phân đoạn:
```
[Ảnh MRI Gốc (FLAIR/T1-CE)] 
          │
          ▼
1. Chuẩn hóa kích thước (256x256) & Lọc Bilateral khử nhiễu
          │
          ▼
2. Tách sọ não (Skull Stripping) bằng hình thái học & LCC
          │
          ▼
3. Cân bằng tương phản CLAHE vùng nhu mô não
          │
          ▼
4. Phân đoạn khối u lõi (So sánh đối chứng 2 phương án)
   ├── Phương án A (Baseline chính): Marker-controlled Watershed
   └── Phương án B (Đối chứng): Seeded Region Growing
          │
          ▼
5. Rút trích đặc trưng hình học (Diện tích u, Circularity, Bounding Box)
          │
          ▼
6. Đánh giá định lượng với Ground Truth chuyên gia (Dice, IoU, Sens, Spec)
          │
          ▼
7. Hiển thị tương tác và xuất báo cáo trên Streamlit GUI
```

### Khảo sát siêu tham số cấu hình hệ thống (`configs/default_params.yaml`):
* `dist_thresh_ratio = 0.4`: Tỷ lệ ngưỡng khoảng cách EDT tối ưu để tách hạt giống u mà không bị phân mảnh.
* `bg_dilate_kernel = 3`: Bán kính giãn nở vùng nền chắc chắn.
* `intensity_tolerance = 15`: Ngưỡng dung sai chênh lệch mức xám tối ưu cho giải thuật phát triển vùng.
* `min_tumor_area = 50, max_tumor_area = 25000`: Giới hạn diện tích pixel của ổ u não hợp lệ.

---

# 8. KẾT QUẢ VÀ ĐÁNH GIÁ ĐỊNH LƯỢNG

### 8.1. Bảng số liệu so sánh định lượng trên toàn bộ 3,929 lát cắt dữ liệu TCGA-LGG (Mean ± Std)

| Nhóm dữ liệu kiểm thử | Phương pháp | Dice Score ($F_1$) | IoU (Jaccard) | Sensitivity | Specificity | Độ trễ (ms/ảnh) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Lát cắt có u (1,373 lát)** | **Marker-controlled Watershed** | **0.4446 ± 0.3014** | **0.3368 ± 0.2677** | **0.4436 ± 0.3170** | **0.9915 ± 0.0107** | **6.13 ± 3.32 ms** |
| | Region Growing | 0.1990 ± 0.2682 | 0.1416 ± 0.2119 | 0.2226 ± 0.3221 | 0.9851 ± 0.0432 | 12.13 ± 22.83 ms |
| **Lát não lành (2,556 lát)** | **Marker-controlled Watershed** | N/A (Không u) | N/A | N/A | **0.9904 ± 0.0100** | **6.15 ± 3.40 ms** |
| | Region Growing | N/A (Không u) | N/A | N/A | 0.9760 ± 0.0480 | 12.05 ± 21.50 ms |

*(Trên tập mẫu 20 ca đại diện được tối ưu hóa tham số, Watershed đạt Dice $0.8124 \pm 0.0845$ và Region Growing đạt $0.7856 \pm 0.1120$)*.

### 8.2. Phân tích kết quả thực nghiệm & Các ca lỗi (Failure Cases)
1. **Ưu thế vượt trội của Marker-controlled Watershed:** Nhờ cơ chế gieo mầm dựa trên biến đổi khoảng cách Euclidean (EDT), Watershed đạt chỉ số Dice trung bình $0.4446$ (gấp 2.23 lần Region Growing: $0.1990$) và thời gian thực thi ổn định chỉ ~6.13 ms/lát cắt. Thuật toán neo hạt giống vững chắc ở tâm u ngay cả khi biên u có độ dốc mức xám yếu.
2. **Hạn chế của Seeded Region Growing khi mở rộng quy mô:** Việc tìm hạt giống bằng giá trị cực đại cường độ đơn lẻ rất nhạy cảm với các tàn dư mạch máu hoặc vùng chất xám tăng quang. Ở các ca u nhỏ ($< 1.5\%$), hạt giống dễ bị lệch ra ngoài ổ u dẫn đến độ tương đồng thấp ($Dice \approx 0$).
3. **Khả năng triệt tiêu dương tính giả xuất sắc:** Trên toàn bộ 2,556 lát não lành, cả hai thuật toán đều đạt độ đặc hiệu $> 97.6\%$ (Watershed đạt $99.04\%$). Điều này chứng minh thuật toán Tách sọ não (Skull Stripping) đã loại bỏ triệt để tín hiệu xương sọ và mô mềm ngoài sọ, không gây báo động giả trên người khỏe mạnh.

---

# 9. CHƯƠNG TRÌNH MINH HỌA (STREAMLIT GUI DEMO)

* **Kiến trúc ứng dụng:** Xây dựng bằng thư viện mã nguồn mở **Streamlit** (`demo/app.py` và `demo/utils.py`):
  * **Thanh điều khiển (Sidebar):** Cho phép duyệt kho 3,929 lát cắt chuẩn (data/full), lọc theo mã bệnh nhân (110 bệnh nhân), lựa chọn thuật toán phân đoạn (Watershed / Region Growing), và thanh trượt tinh chỉnh siêu tham số.

  * **Khu vực hiển thị chính (Main Area):** 5 thẻ KPI chẩn đoán nổi bật (Trạng thái khối u, Diện tích pixel, Tỷ lệ u/não, Độ tròn Circularity, Điểm tương đồng Dice).
  * **Lưới ảnh trực quan hóa:** Hiển thị song song 4 ảnh trung gian $[Gốc \mid Tách sọ \mid Mặt nạ u \mid Khoanh vùng Bounding Box]$ và so sánh đối chiếu trực tiếp với Ground Truth.
* **Hướng dẫn khởi chạy demo:**
  ```bash
  streamlit run demo/app.py
  ```

---

# 10. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 10.1. Kết quả đạt được
* Xây dựng thành công hệ thống xử lý ảnh số tự động, khép kín, minh bạch toán học phục vụ phân đoạn u não MRI.
* Cài đặt thành công kỹ thuật Tách sọ não kinh điển bằng hình thái học và thuật toán LCC, đạt độ đặc hiệu $99.04\%$ trên não lành.
* Thực hiện so sánh đối chứng khoa học, khách quan trên toàn bộ 3,929 lát cắt dữ liệu TCGA-LGG giữa 2 thuật toán Watershed và Region Growing.

### 10.2. Hạn chế & Hướng phát triển
* Mở rộng từ ảnh 2D sang tái tạo không gian 3D thể tích khối u (3D Voxel Rendering).
* Nghiên cứu tích hợp đặc trưng kết cấu GLCM (Haralick Texture Features) để nâng cao độ nhạy trên các ca u nhỏ biên mờ.

---

# 11. TÀI LIỆU THAM KHẢO

1. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing (4th ed.)*. Pearson.
2. Buda, M., Saha, A., & Mazurowski, M. A. (2019). *Association of genomic subtypes of lower-grade gliomas with shape features automatically extracted by a deep learning algorithm.* Computers in Biology and Medicine, 109, 218-225.
3. Bộ môn Khoa học Dữ liệu — Khoa CNTT (2026). *Giáo trình Xử lý ảnh số (Mã HP: 0101006276)*. Trường Đại học Công Thương TP. Hồ Chí Minh (HUIT).
4. Khoa Công nghệ Thông tin — HUIT (2026). *Kế hoạch thực hiện Đồ án Xử lý ảnh số năm học 2026–2027 (Kèm Rubric chấm đồ án)*.
5. Bradski, G. (2000). *The OpenCV Library*. Dr. Dobb's Journal of Software Tools.

---

# 12. PHỤ LỤC

### Phụ lục A: Khung Rubric Đánh Giá Đồ Án Môn Học Của Khoa CNTT — HUIT (Thang điểm 10)
*(Chiếm 100% phần thi cuối kỳ, tương đương 70% tổng điểm học phần)*

| STT | Tiêu chí đánh giá | Chuẩn đầu ra (PLO/CLO) | Trọng số | Điểm tối đa |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Phân tích và lựa chọn đúng phương pháp | PLO2 / CLO1 | 15% | 1.5 điểm |
| 2 | Áp dụng được các phương pháp xử lý *(Trọng tâm)* | PLO2 / CLO2 | 50% | 5.0 điểm |
| 3 | Đọc tài liệu, nghiên cứu giải quyết bài toán | PLO4 / CLO3 | 10% | 1.0 điểm |
| 4 | Trình bày báo cáo | PLO7 / CLO5 | 15% | 1.5 điểm |
| 5 | Phân công và phối hợp làm việc nhóm | PLO6 / CLO4 | 10% | 1.0 điểm |
| **TỔNG** | **ĐIỂM ĐÁNH GIÁ CUỐI KỲ** | | **100%** | **10.0 điểm** |

### Phụ lục B: Bảng Tổng Hợp Phân Công Nhiệm Vụ Sprint Cấp Tốc 7 Ngày Chi Tiết
| Ngày | Nội dung công việc trọng tâm | Hà Mạnh Trường (Nhóm trưởng) | Huỳnh Tâm Trí (Thành viên) | Sản phẩm nghiệm thu |
| :---: | :--- | :--- | :--- | :--- |
| **Ngày 1** | Khởi động Sprint, Chuẩn hóa Dữ liệu & Đặc tả Kỹ thuật | Chủ trì lập kế hoạch Sprint 7 ngày, soạn thảo đặc tả `SPEC_PIPELINE_MRI.md` (13 signatures, 7 invariants) | Chuẩn hóa toàn bộ 3,929 lát cắt dữ liệu TCGA-LGG, chạy Notebook 01 EDA, xuất `DATA_EXPLORATION_REPORT.md` | `SPEC_PIPELINE_MRI.md`, Notebook 01, Báo cáo dữ liệu |

| **Ngày 2** | Tiền xử lý, Tách sọ não 6 bước & Bộ đo Y sinh | Cài đặt `filters.py` (Bilateral + CLAHE), `skull_strip.py` 6 bước kinh điển, hoàn thiện Notebook 02 | Cài đặt module `metrics.py` (Dice, IoU, Sens, Spec), xử lý an toàn mẫu rỗng $0/0$, viết test unit | `src/preprocessing/`, `src/evaluation/metrics.py`, Unit tests (test_preprocessing, test_metrics) |
| **Ngày 3** | Phân đoạn Baseline Watershed & Đo Đặc trưng Hình học | Cài đặt `watershed.py` với biến đổi khoảng cách EDT, khảo sát ngưỡng `dist_thresh_ratio` | Cài đặt `features.py` (diện tích u, circularity, bounding box) và `visualization.py` (hộp đỏ, viền vàng, Quad view) | `src/segmentation/watershed.py`, `src/measurement/`, Unit tests (test_segmentation, test_measurement) |
| **Ngày 4** | Phân đoạn Đối chứng Region Growing & Ghép nối Pipeline | Cài đặt `region_growing.py` (tự tìm seed cực đại cường độ, BFS 8 láng giềng), tích hợp `BrainTumorPipeline` | Hoàn thiện Notebook 03 (so sánh song song Watershed vs Region Growing), xây dựng framework benchmark | `src/pipeline.py`, Notebook 03, Bảng nhận xét định tính |
| **Ngày 5** | Benchmark Quy mô lớn (3,929 lát cắt) & Web Demo GUI | Phân tích chuyên sâu các ca thất bại (Failure cases: u nhỏ <1.5%, u biên mờ, u chèn ép não thất) | Hoàn thiện Streamlit GUI (`demo/app.py`) Dual-mode, chạy benchmark đa tiến trình 3,929 lát cắt và Notebook 04 | `BENCHMARK_RESULTS.csv`, Notebook 04, Streamlit Web App |
| **Ngày 6** | Biên soạn Toàn văn Báo cáo Đồ án 12 Mục chuẩn HUIT | Soạn thảo 4 chương kỹ thuật (Mục 2: Lý thuyết; Mục 4: Tiền xử lý & Sọ; Mục 6: Thực nghiệm; Mục 8: Kỹ thuật) | Soạn thảo 6 chương tổng quan (Mục 1: Mở đầu; Mục 3: Dữ liệu; Mục 5: Chỉ số; Mục 8: Số liệu; Mục 9: GUI; Mục 10: Kết luận) | `BAO_CAO_DO_AN_XLAS.md`, `BAO_CAO_DO_AN_XLAS.docx` (Word chuẩn lề 3-3-3-2 cm) |
| **Ngày 7** | Chuẩn hóa Mã nguồn, Slide Thuyết trình, Video Demo & Đóng gói | Rà soát toàn bộ code `src/`, bổ sung 100% docstring tiếng Việt, bảo đảm 12/12 unit tests PASSED | Thiết kế bộ Slide 20 trang (`SLIDE_THUYET_TRINH_OUTLINE.md`), quay Video demo 3 phút, đóng gói ZIP trọn bộ hồ sơ | Slide PPTX/PDF, Video Demo MP4, Bộ mã nguồn sạch, Hồ sơ nộp hoàn chỉnh |
| **Nghiệm thu** | BẢO VỆ ĐỒ ÁN TRƯỚC HỘI ĐỒNG CHẤM THI HUIT | Thuyết trình phần kỹ thuật, giải thuật và phân tích ca lỗi | Thuyết trình phần dữ liệu, số liệu định lượng và trình diễn Demo GUI | Bảo vệ thành công đồ án, đạt chuẩn đầu ra môn học |

### Phụ lục C: Hướng Dẫn Cài Đặt & Chạy Thử Toàn Bộ Hệ Thống
```bash
# 1. Cài đặt thư viện phụ thuộc
pip install -r requirements.txt

# 2. Tải toàn bộ 3,929 lát cắt chuẩn TCGA-LGG (tùy chọn mở rộng)
python scripts/download_full_dataset.py

# 3. Chạy benchmark định lượng đa tiến trình
python scripts/run_all_experiments.py

# 4. Khởi chạy giao diện demo tương tác Web Streamlit
streamlit run demo/app.py

# 5. Chạy kiểm thử tự động (Unit Tests)
pytest -v
```
