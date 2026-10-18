# Hướng Dẫn & Mô Tả Bộ Dữ Liệu: ISIC Skin Lesion Segmentation
### International Skin Imaging Collaboration (ISIC 2018 / PH2)

---

## 📌 1. Nguồn Gốc và Định Danh Bộ Dữ Liệu
* **Nguồn dữ liệu:** Kho lưu trữ ảnh da liễu quốc tế [ISIC Archive (International Skin Imaging Collaboration)](https://www.isic-archive.com/) — Thử thách **ISIC 2018 Challenge (Task 1: Lesion Boundary Segmentation)**.
* **Đối tượng bài toán:** Ảnh chụp soi da kỹ thuật số (Dermoscopy) của các tổn thương da liễu nghi ngờ ung thư hắc tố (Melanoma) và các tổn thương lành tính (Benign Nevus, Seborrheic Keratosis).
* **Mặt nạ chuyên gia (Ground Truth Mask):** Mặt nạ nhị phân do các bác sĩ chuyên khoa da liễu quốc tế gán nhãn thủ công với độ tin cậy tuyệt đối.

---

## 📂 2. Cấu Trúc Thư Mục Dữ Liệu

```
data/
├── README.md                      # Tài liệu mô tả dữ liệu
├── sample/                        # Tập dữ liệu mẫu 20 ca thực nghiệm ban đầu
│   ├── metadata.csv               # Bảng tra cứu thông tin mẫu và kích thước
│   ├── images/                    # 20 ảnh soi da màu gốc (.jpg)
│   │   ├── ISIC_sample_001.jpg
│   │   ├── ...
│   │   └── ISIC_sample_020.jpg
│   └── masks/                     # 20 mặt nạ nhị phân Ground Truth tương ứng (.png)
│       ├── ISIC_sample_001_mask.png
│       ├── ...
│       └── ISIC_sample_020_mask.png
├── raw/                           # Thư mục chứa toàn bộ dữ liệu tải về khi huấn luyện
└── processed/                     # Thư mục lưu ảnh sau tiền xử lý (Bilateral, CLAHE)
```

---

## 🔬 3. Quy Cách Dữ Liệu & Giá Trị Pixel

* **Ảnh gốc (`images/*.jpg`):**
  * Định dạng: RGB 3 kênh màu, giá trị mỗi kênh trong khoảng $[0, 255]$.
  * Đặc điểm: Chứa tổn thương vùng trung tâm, một số ảnh có lông da, thước đo, bọt khí hoặc góc tối quang học (vignetting).
* **Mặt nạ chuẩn (`masks/*.png`):**
  * Định dạng: Ảnh đơn kênh Grayscale / Nhị phân.
  * Giá trị:
    * `0` (Đen): Vùng da lành / nền (Background).
    * `255` (Trắng): Vùng mô bệnh / tổn thương (Lesion Foreground).
* **Mục tiêu phân đoạn:** Dự đoán nhãn pixel sao cho mặt nạ $P$ khớp tối đa với mặt nạ chuyên gia $G$ đo qua chỉ số:
  $$\text{Dice} = \frac{2 |P \cap G|}{|P| + |G|} \ge 0.80$$

---

## 📥 4. Cách Tải Thêm Dữ Liệu Toàn Phần
Nếu nhóm cần mở rộng tập dữ liệu từ 20 mẫu lên 500+ ảnh, chạy script:
```bash
python scripts/download_sample_data.py
```
Hoặc tải trực tiếp từ cổng thử thách [ISIC Challenge Datasets](https://challenge.isic-archive.com/data/).
