# BÁO CÁO KHÁM PHÁ & ĐẶC TẢ TẬP DỮ LIỆU THỰC NGHIỆM (TCGA-LGG BENCHMARK)
## Đề tài: Phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ (MRI)
**Học phần:** Xử lý ảnh số (2026–2027) — Khoa CNTT — HUIT  
**Người thực hiện:** Huỳnh Tâm Trí (MSSV: `2045240315`) — Thành viên phụ trách Dữ liệu & Đánh giá  
**Người duyệt:** Hà Mạnh Trường (MSSV: `2045240326`) — Nhóm trưởng

---

## 📌 1. Nguồn Gốc & Quy Cách Dữ Liệu Y Khoa

* **Tên bộ dữ liệu:** The Cancer Genome Atlas Low-Grade Glioma (**TCGA-LGG**) Brain MRI Dataset.
* **Nguồn dữ liệu chính thức:** Hugging Face Datasets — [Ehsan-rmz/lgg-mri-segmentation-research](https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research).
* **Kho đối chứng bổ trợ:** Kaggle — [mateuszbuda/lgg-mri-segmentation](https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation).
* **Tài liệu khoa học công bố:** Buda, M., Saha, A., & Mazurowski, M. A. (2019). *Association of genomic subtypes of lower-grade gliomas with shape features automatically extracted by a deep learning algorithm.* Computers in Biology and Medicine, 109, 218-225.
* **Phương thái chụp:** Ảnh cắt lát cộng hưởng từ sọ não (Axial MRI slices) chuỗi xung FLAIR (Fluid-Attenuated Inversion Recovery) và T1-weighted có tiêm thuốc cản từ (T1-CE).
* **Quy cách chuẩn hóa trong đồ án:**
  * Định dạng: Lossless PNG (8-bit Grayscale chuẩn hóa).
  * Kích thước ma trận ảnh: $256 \times 256$ pixels.
  * Mặt nạ Ground Truth (Binary Mask): Kích thước $256 \times 256$, nhị phân $0$ (mô não lành / xương sọ) và $255$ (khối u não do chuyên gia chẩn đoán hình ảnh khoanh vùng).

---

## 📊 2. Thống Kê Tổng Thể Toàn Bộ 3,929 Lát Cắt (110 Bệnh Nhân)

Tập dữ liệu full gồm 3.929 lát cắt MRI từ 110 bệnh nhân. Trong đó, 1.373 lát (34,95%) có vùng u trong mask Ground Truth và 2.556 lát (65,05%) không có vùng u trong mask. Các thống kê dưới đây được tính từ data/full/metadata.csv

| Chỉ Số Thống Kê Toàn Tập | Giá Trị Đo Lường | Tỷ Lệ (%) | Ý Nghĩa Chẩn Đoán Lâm Sàng |
| :--- | :---: | :---: | :--- |
| **Tổng số bệnh nhân nghiên cứu** | **110** | 100% | Đại diện đa dạng về độ tuổi, giới tính và phân độ mô học glioma |
| **Tổng số lát cắt MRI thu thập** | **3,929** | 100% | Chuỗi lát cắt ngang sọ não liên tục (trung bình 35.7 lát/bệnh nhân) |
| **Lát cắt dương tính (Có khối u)** | **1,373** | **34.95%** | Lát cắt đi qua tổn thương u — dùng đo Dice, IoU, Sensitivity |
| **Lát cắt âm tính (Não lành)** | **2,556** | **65.05%** | Lát cắt đỉnh đầu hoặc đáy sọ không có u — dùng đo Specificity |

---

## 📈 3. Phân Tích Thống Kê Đặc Trưng Khối U (Trên 1,373 Lát Cắt Có U)

Đo lường chi tiết trên toàn bộ 1,373 lát cắt chứa u não:

| Thống kê mô tả | Diện tích khối u (Pixels) | Tỷ lệ khối u trên sọ não (%) |
| :--- | :---: | :---: |
| **Giá trị nhỏ nhất (Min)** | 7 px | 0.01% |
| **Phân vị 25% (Q1)** | 735 px | 1.12% |
| **Trung vị (Median / Q2)** | **1,529 px** | **2.33%** |
| **Phân vị 75% (Q3)** | 2,765 px | 4.22% |
| **Giá trị lớn nhất (Max)** | 7,929 px | 12.10% |
| **Trung bình ± Độ lệch chuẩn (Mean ± Std)** | **1,931.4 ± 1,529.6 px** | **2.95 ± 2.33%** |
Tập dữ liệu có nhiều lát không chứa vùng u trong mask hơn lát có u. Vì vậy, cần trình bày kết quả phân đoạn riêng cho nhóm có u và nhóm không có u; chỉ số gộp toàn tập có thể che khuất khả năng phát hiện u. Lát không có vùng u trong mask không đồng nghĩa với bệnh nhân khỏe mạnh.
### Phân tầng độ khó xử lý ảnh số (3 nhóm tổn thương):
1. **Nhóm U Nhỏ ($< 1.5\%$ diện tích ảnh — 463 lát cắt, chiếm 33.7%):**
   * *Đặc điểm:* Tổn thương vi mô hoặc rìa mép ngoài cùng của khối u, kích thước từ vài chục đến dưới 983 pixel.
   * *Thách thức DIP:* Ngưỡng khoảng cách cực đại trong Watershed rất dễ bị triệt tiêu; thuật toán Region Growing dễ dừng sớm do độ dốc mức xám không đủ rõ.
2. **Nhóm U Trung Bình ($1.5\% - 5.0\%$ — 667 lát cắt, chiếm 48.6%):**
   * *Đặc điểm:* Lát cắt đi qua phần thân chính của ổ u, ranh giới tăng sáng tương phản cao so với nhu mô não lành.
   * *Thách thức DIP:* Là nhóm phù hợp nhất với các thuật toán phân đoạn hình thái học cổ điển; Watershed cho độ chính xác cao nhất (Dice $> 0.70$).
3. **Nhóm U Lớn ($> 5.0\%$ — 243 lát cắt, chiếm 17.7%):**
   * *Đặc điểm:* U kích thước lớn (lên tới 7,929 px, chiếm $> 12\%$ diện tích sọ), gây hiệu ứng khối (mass effect) chèn ép não thất và đè đẩy đường giữa não.
   * *Thách thức DIP:* Quá trình tách sọ não kinh điển (Skull Stripping) cần bảo toàn bờ u nằm sát màng cứng xương sọ.

---

## 🔬 4. Tổ Chức Dữ Liệu Thực Nghiệm (TCGA-LGG Benchmark)

Toàn bộ dữ liệu thực nghiệm chuẩn quốc tế gồm 3,929 lát cắt chuẩn TCGA-LGG từ 110 bệnh nhân được lưu trữ tập trung tại `data/full/`:
* Thư mục `data/full/images/` và `data/full/masks/` chứa toàn bộ ảnh MRI xám và mặt nạ Ground Truth $256 \times 256$.
* Bảng `data/full/metadata.csv` được theo dõi trực tiếp trong Git repository, ghi nhận chi tiết diện tích u và tỷ lệ phần trăm cho từng lát cắt.
* Người dùng có thể tái tạo hoặc cập nhật kho dữ liệu bằng script `python scripts/download_full_dataset.py`.

---

## 📑 5. Bảng Dữ Liệu 20 Ca Bệnh Tiêu Biểu Trong Tập Thực Nghiệm (TCGA-LGG)

| STT | Mã Ca Mẫu (`sample_id`) | Bệnh Nhân Nguồn | Kích Thước | Diện Tích U (px) | Tỷ Lệ U / Não (%) | Phân Loại Độ Khó |

| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| 1 | `mri_brain_tumor_01` | `TCGA_CS_4941_19960909` | $256 \times 256$ | 1,426 | 2.18% | Trung bình |
| 2 | `mri_brain_tumor_02` | `TCGA_CS_4941_19960909` | $256 \times 256$ | 2,646 | 4.04% | Trung bình |
| 3 | `mri_brain_tumor_03` | `TCGA_CS_4942_19970222` | $256 \times 256$ | 1,257 | 1.92% | Trung bình |
| 4 | `mri_brain_tumor_04` | `TCGA_CS_4942_19970222` | $256 \times 256$ | 1,539 | 2.35% | Trung bình |
| 5 | `mri_brain_tumor_05` | `TCGA_CS_4943_20000902` | $256 \times 256$ | 801 | 1.22% | **U Nhỏ (Khó)** |
| 6 | `mri_brain_tumor_06` | `TCGA_CS_4943_20000902` | $256 \times 256$ | 1,582 | 2.41% | Trung bình |
| 7 | `mri_brain_tumor_07` | `TCGA_CS_4944_20010208` | $256 \times 256$ | 6,189 | 9.44% | **U Lớn (Chèn ép)** |
| 8 | `mri_brain_tumor_08` | `TCGA_CS_4944_20010208` | $256 \times 256$ | 5,178 | 7.90% | **U Lớn (Chèn ép)** |
| 9 | `mri_brain_tumor_09` | `TCGA_CS_5393_19990606` | $256 \times 256$ | 5,326 | 8.13% | **U Lớn (Chèn ép)** |
| 10 | `mri_brain_tumor_10` | `TCGA_CS_5393_19990606` | $256 \times 256$ | 4,132 | 6.30% | **U Lớn (Chèn ép)** |
| 11 | `mri_brain_tumor_11` | `TCGA_CS_5395_19981004` | $256 \times 256$ | 735 | 1.12% | **U Nhỏ (Khó)** |
| 12 | `mri_brain_tumor_12` | `TCGA_CS_5395_19981004` | $256 \times 256$ | 840 | 1.28% | **U Nhỏ (Khó)** |
| 13 | `mri_brain_tumor_13` | `TCGA_CS_5396_20010302` | $256 \times 256$ | 916 | 1.40% | **U Nhỏ (Khó)** |
| 14 | `mri_brain_tumor_14` | `TCGA_CS_5396_20010302` | $256 \times 256$ | 2,897 | 4.42% | Trung bình |
| 15 | `mri_brain_tumor_15` | `TCGA_CS_5397_20010315` | $256 \times 256$ | 1,463 | 2.23% | Trung bình |
| 16 | `mri_brain_tumor_16` | `TCGA_CS_5397_20010315` | $256 \times 256$ | 845 | 1.29% | **U Nhỏ (Khó)** |
| 17 | `mri_brain_tumor_17` | `TCGA_CS_6186_20000601` | $256 \times 256$ | 1,485 | 2.27% | Trung bình |
| 18 | `mri_brain_tumor_18` | `TCGA_CS_6186_20000601` | $256 \times 256$ | 2,079 | 3.17% | Trung bình |
| 19 | `mri_brain_tumor_19` | `TCGA_CS_6188_20010812` | $256 \times 256$ | 847 | 1.29% | **U Nhỏ (Khó)** |
| 20 | `mri_brain_tumor_20` | `TCGA_CS_6188_20010812` | $256 \times 256$ | 610 | 0.93% | **U Nhỏ (Khó)** |
