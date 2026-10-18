# Quản Lý Dữ Liệu Đa Phương Thức: Phân Đoạn & Phát Hiện Tổn Thương Y Tế
### Multi-Modal Medical Image Datasets

---

## 📌 1. Các Phương Thức Dữ Liệu Được Hỗ Trợ

Dự án được xây dựng dưới dạng **Khung hệ thống tổng quát**, hỗ trợ 3 phương thức ảnh y tế phổ biến:

| Phương thức | Tên bài toán | Nguồn Dataset Benchmark | Định dạng dữ liệu |
| :--- | :--- | :--- | :--- |
| **1. Da liễu (Dermoscopy)** | Phân đoạn tổn thương ung thư hắc tố (Melanoma) | **ISIC 2018 (Task 1) / PH2** | Ảnh màu RGB (`.jpg`) + Mask nhị phân (`.png`) |
| **2. X-quang phổi (Chest X-ray)** | Phân đoạn và định vị tổn thương viêm phổi / COVID-19 | **COVID-QU-Ex / Montgomery / Shenzhen** | Ảnh xám Grayscale (`.png`) + Mask nhị phân (`.png`) |
| **3. Não MRI (Brain MRI)** | Phân đoạn và định vị khối u não (Brain Tumor) | **Figshare Brain Tumor / BraTS** | Ảnh cắt lát MRI 2D (`.png`/`.jpg`) + Mask u não (`.png`) |

---

## 📂 2. Cấu Trúc Thư Mục Dữ Liệu

```
data/
├── README.md                      # Tài liệu mô tả dữ liệu
├── sample/                        # Bộ dữ liệu mẫu phục vụ thử nghiệm nhanh
│   ├── skin/                      # Dữ liệu ảnh da liễu ISIC
│   │   ├── images/                # 20 ảnh soi da màu gốc (.jpg)
│   │   ├── masks/                 # 20 mặt nạ Ground Truth chuyên gia (.png)
│   │   └── metadata.csv           # Bảng thông tin 20 mẫu da liễu
│   ├── xray/                      # Dữ liệu ảnh X-quang phổi (CXR)
│   │   ├── images/
│   │   └── masks/
│   └── mri/                       # Dữ liệu ảnh cộng hưởng từ Não MRI
│       ├── images/
│       └── masks/
├── raw/                           # (Đã cấu hình .gitignore) Chứa bộ dữ liệu lớn khi mở rộng
└── processed/                     # (Đã cấu hình .gitignore) Lưu ảnh sau tiền xử lý (CLAHE, Bilateral)
```

---

## 🔬 3. Quy Cách Mặt Nạ Ground Truth (Binary Mask)

Mọi phương thức đều được chuẩn hóa về quy cách chung:
* **Giá trị 0 (Đen):** Vùng mô lành / Nền (Background).
* **Giá trị 255 (Trắng):** Vùng mô bệnh / Ổ tổn thương (Lesion Foreground).
* **Chỉ số đánh giá định lượng:**
  $$\text{Dice}(P, G) = \frac{2 |P \cap G|}{|P| + |G|}, \quad \text{IoU}(P, G) = \frac{|P \cap G|}{|P \cup G|}$$
