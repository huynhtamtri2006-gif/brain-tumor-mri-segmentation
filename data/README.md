# Dữ Liệu Đồ Án: Phân Đoạn & Phát Hiện Khối U Não Trên Ảnh MRI
### Brain Tumor MRI Segmentation & Detection Dataset (TCGA-LGG Benchmark)

---

## 📌 1. Nguồn Dữ Liệu Chuẩn Quốc Tế & Liên Kết Tải Về

Dữ liệu thực nghiệm của đồ án được trích xuất từ bộ dữ liệu chuẩn benchmark quốc tế:
* **Tên tập dữ liệu:** The Cancer Genome Atlas Low-Grade Glioma (**TCGA-LGG**) Brain MRI Dataset.
* **Tác giả / Nghiên cứu:** Buda et al. (2019), công bố trên tạp chí *Computers in Biology and Medicine*.
* **Phương thái chụp:** Ảnh cộng hưởng từ sọ não chuỗi xung FLAIR (Fluid-Attenuated Inversion Recovery) và T1-weighted có cản từ.
* **Gắn nhãn (Annotation):** Mỗi lát cắt MRI đi kèm mặt nạ phân đoạn nhị phân (Ground Truth Binary Mask) được các chuyên gia giải phẫu thần kinh và chẩn đoán hình ảnh khoanh vùng chi tiết.

### 🔗 Nguồn dữ liệu chính thức & Liên kết truy cập:
1. **Hugging Face Datasets (Nguồn dữ liệu chính thức của Đồ án):**  
   👉 [https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research](https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research)  
   *(Kho dữ liệu nghiên cứu chuẩn gồm 3,929 lát cắt MRI có mặt nạ u não Ground Truth; được tích hợp tự động trong script `python scripts/download_sample_data.py` của đồ án)*.
2. **Kaggle Dataset (Kho dự phòng / Đối chứng):**  
   👉 [https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation](https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation)  
   *(Bộ dữ liệu gốc của Mateusz Buda trên nền tảng Kaggle)*.
3. **The Cancer Imaging Archive (TCIA) - Nguồn viện Y tế Quốc gia Hoa Kỳ (NIH):**  
   👉 [https://wiki.cancerimagingarchive.net/display/Public/TCGA-LGG](https://wiki.cancerimagingarchive.net/display/Public/TCGA-LGG)  
   *(Kho lưu trữ ảnh y khoa lâm sàng gốc định dạng DICOM)*.
4. **Mã nguồn gốc & Bài báo của tác giả (Mateusz Buda):**  
   👉 GitHub: [https://github.com/mateuszbuda/brain-segmentation-pytorch](https://github.com/mateuszbuda/brain-segmentation-pytorch)  
   👉 DOI Bài báo: [https://doi.org/10.1016/j.compbiomed.2019.04.018](https://doi.org/10.1016/j.compbiomed.2019.04.018)

---

## 📂 2. Cấu Trúc Thư Mục Dữ Liệu Hai Tầng (Two-Tier Architecture)

Để tối ưu hóa dung lượng repository Git (< 3 MB) đồng thời đảm bảo khả năng tái lập thực nghiệm 100% trên tập dữ liệu quy mô lớn, dữ liệu được thiết kế theo cấu trúc hai tầng:

```
data/
├── README.md                      # Tài liệu thuyết minh dữ liệu thực nghiệm
├── sample/                        # [Tầng 1 - Tracked in Git] Bộ 20 mẫu chuẩn phục vụ kiểm thử nhanh
│   ├── images/                    # 20 ảnh cắt lát MRI não (.png, 256x256)
│   ├── masks/                     # 20 mặt nạ Ground Truth khối u nhị phân (.png, 256x256)
│   └── metadata.csv               # Bảng metadata thống kê diện tích và tỷ lệ u của 20 mẫu
├── full/                          # [Tầng 2 - Gitignored] Toàn bộ 3,929 lát cắt chuẩn TCGA-LGG
│   ├── images/                    # 3,929 ảnh cắt lát MRI não (.png, 256x256)
│   ├── masks/                     # 3,929 mặt nạ Ground Truth u não (.png, 256x256)
│   └── metadata.csv               # Bảng metadata chi tiết 3,929 lát cắt từ 110 bệnh nhân
└── processed/                     # Kết quả tiền xử lý và tách sọ não
```

> **Cách tải toàn bộ dữ liệu 3,929 lát cắt (1-click script):**
> ```bash
> python scripts/download_full_dataset.py
> ```
> Script tự động tải parquet từ Hugging Face, giải nén ảnh và mặt nạ thành PNG $256 \times 256$, sinh `metadata.csv` và dọn dẹp bộ nhớ đệm tự động.

---

## 🔬 3. Quy Cách Mặt Nạ Ground Truth (Binary Mask)

Mỗi file ảnh mặt nạ trong `data/sample/masks/` hoặc `data/full/masks/` tương ứng 1-1 với ảnh MRI trong thư mục `images/`:
* **Kích thước chuẩn:** $256 \times 256$ pixels.
* **Giá trị 0 (Đen):** Mô não lành / Hộp sọ / Vùng ngoài sọ (Background).
* **Giá trị 255 (Trắng):** Vùng nhu mô u não (Core Tumor / Lesion Foreground).
* **Định lượng diện tích u:**
  * Diện tích u: $S_{\text{tumor}} = \sum_{(x,y)} \mathbb{I}(M(x, y) = 255)$ (đơn vị: pixels).
  * Tỷ lệ phần trăm u trên thiết diện não: $\text{Ratio} = \frac{S_{\text{tumor}}}{256 \times 256} \times 100\%$.

---

## 📊 4. Thống Kê Chi Tiết Toàn Bộ Dữ Liệu Thực Nghiệm (3,929 Lát Cắt)

| Chỉ số thống kê | Toàn bộ tập dữ liệu (`data/full`) | Tập mẫu nhanh (`data/sample`) |
| :--- | :--- | :--- |
| **Tổng số lát cắt MRI** | **3,929 lát cắt** | **20 lát cắt** |
| **Số lượng bệnh nhân** | **110 bệnh nhân** (TCGA-LGG) | **10 bệnh nhân** |
| **Lát cắt có khối u (Positive)** | **1,373 lát cắt** (34.95%) | **20 lát cắt** (100%) |
| **Lát cắt não lành (Healthy/Negative)** | **2,556 lát cắt** (65.05%) | **0 lát cắt** |
| **Diện tích u trung bình (Mean Area)** | **1,931.4 pixels** (2.95% ảnh) | **2,060.0 pixels** (3.14% ảnh) |
| **Trung vị diện tích u (Median Area)** | **1,529.0 pixels** (2.33% ảnh) | **1,725.5 pixels** (2.63% ảnh) |
| **Diện tích u nhỏ nhất (Min Area)** | **7 pixels** (0.01% ảnh) | **120 pixels** (0.18% ảnh) |
| **Diện tích u lớn nhất (Max Area)** | **7,929 pixels** (12.10% ảnh) | **5,348 pixels** (8.16% ảnh) |

### Phân bố nhóm diện tích u trong 1,373 lát cắt bệnh lý:
1. **Khối u nhỏ (< 1.5% diện tích ảnh):** 463 lát cắt (33.72%) — Thử thách phân đoạn do biên mờ và tín hiệu yếu.
2. **Khối u trung bình (1.5% – 5.0% diện tích ảnh):** 667 lát cắt (48.58%) — Vùng chuyển tiếp chất xám/chất trắng rõ nét.
3. **Khối u lớn (> 5.0% diện tích ảnh):** 243 lát cắt (17.70%) — U chiếm phần lớn bán cầu đại não, gây hiệu ứng chèn ép não thất.

Xem báo cáo khám phá dữ liệu toàn diện tại: [docs/DATA_EXPLORATION_REPORT.md](file:///C:/Users/xpaga/Documents/xlas/docs/DATA_EXPLORATION_REPORT.md).
