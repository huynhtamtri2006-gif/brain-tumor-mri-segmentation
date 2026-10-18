# BÁO CÁO KHÁM PHÁ & ĐẶC TẢ TẬP DỮ LIỆU THỰC NGHIỆM (TCGA-LGG)
## Đề tài: Phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ (MRI)
**Học phần:** Xử lý ảnh số (2026–2027) — Khoa CNTT — HUIT  
**Người thực hiện:** Huỳnh Tâm Trí (MSSV: `2045240315`) — Thành viên phụ trách Dữ liệu & Đánh giá  
**Người duyệt:** Hà Mạnh Trường (MSSV: `2045240326`) — Nhóm trưởng

---

## 📌 1. Nguồn Gốc & Quy Cách Dữ Liệu Y Khoa

* **Tên bộ dữ liệu:** The Cancer Genome Atlas Low-Grade Glioma (**TCGA-LGG**) Brain MRI Dataset.
* **Nguồn dữ liệu chính thức:** Hugging Face Datasets — [Ehsan-rmz/lgg-mri-segmentation-research](https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research) (Kho chuẩn 3,929 lát cắt tích hợp trong script `download_sample_data.py`).
* **Kho đối chứng bổ trợ:** Kaggle — [mateuszbuda/lgg-mri-segmentation](https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation).
* **Tài liệu khoa học công bố:** Buda, M., Saha, A., & Mazurowski, M. A. (2019). *Association of genomic subtypes of lower-grade gliomas with shape features automatically extracted by a deep learning algorithm.* Computers in Biology and Medicine, 109, 218-225.
* **Phương thái chụp:** Ảnh cắt lát cộng hưởng từ sọ não (Axial MRI slices) chuỗi xung FLAIR (Fluid-Attenuated Inversion Recovery) và T1-weighted có tiêm thuốc cản từ (T1-CE).
* **Quy cách chuẩn hóa trong đồ án:**
  * Định dạng: Lossless PNG (24-bit RGB hoặc 8-bit Grayscale).
  * Kích thước ma trận ảnh: $256 \times 256$ pixels.
  * Mặt nạ Ground Truth (Binary Mask): Kích thước $256 \times 256$, nhị phân $0$ (mô não lành / xương sọ) và $255$ (khối u não do bác sĩ chẩn đoán hình ảnh khoanh vùng).

---

## 📊 2. Bảng Thống Kê Chi Tiết 20 Ca Mẫu Trong `data/sample/`

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

---

## 📈 3. Phân Nhóm Dữ Liệu Theo Thách Thức Kỹ Thuật

1. **Nhóm U Nhỏ ($< 1.5\%$ diện tích ảnh — 7 ca):**
   * *Đặc điểm:* Kích thước chỉ từ 610 px đến 916 px. Ranh giới chuyển tiếp mức xám rất hẹp.
   * *Thách thức DIP:* Watershed dễ bị under-segmentation nếu ngưỡng khoảng cách đặt quá cao, hoặc Region Growing dễ bị dừng sớm nếu ngưỡng dung sai quá khắt khe.
2. **Nhóm U Trung Bình ($1.5\% - 5\%$ — 9 ca):**
   * *Đặc điểm:* Diện tích từ 1,257 px đến 2,897 px. Khối u rõ nét, tăng sáng điển hình.
   * *Thách thức DIP:* Cả hai phương pháp đều cho kết quả tốt (Dice thường đạt $> 0.80$).
3. **Nhóm U Lớn ($> 5\%$ — 4 ca):**
   * *Đặc điểm:* Diện tích từ 4,132 px đến 6,189 px. Khối u to, xâm lấn và làm biến dạng cấu trúc não thất.
   * *Thách thức DIP:* Tách sọ cần cẩn thận không cắt nhầm phần u nằm sát màng cứng vào phần xương sọ.
