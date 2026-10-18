# Dữ Liệu Đồ Án: Phân Đoạn & Phát Hiện Khối U Não Trên Ảnh MRI
### Brain Tumor MRI Segmentation & Detection Dataset (TCGA-LGG Benchmark)

---

## 📌 1. Nguồn Dữ Liệu Chuẩn Quốc Tế

Dữ liệu thực nghiệm của đồ án được trích xuất từ bộ dữ liệu chuẩn benchmark quốc tế:
* **Tên tập dữ liệu:** The Cancer Genome Atlas Low-Grade Glioma (**TCGA-LGG**) Brain MRI Dataset.
* **Tác giả / Nghiên cứu:** Buda et al. (2019), công bố trên tạp chí *Computers in Biology and Medicine*.
* **Phương thái chụp:** Ảnh cộng hưởng từ sọ não chuỗi xung FLAIR (Fluid-Attenuated Inversion Recovery) và T1-weighted có cản từ.
* **Gắn nhãn (Annotation):** Mỗi lát cắt MRI đi kèm mặt nạ phân đoạn nhị phân (Ground Truth Binary Mask) được các chuyên gia giải phẫu thần kinh và chẩn đoán hình ảnh khoanh vùng chi tiết.

---

## 📂 2. Cấu Trúc Thư Mục Dữ Liệu

```
data/
├── README.md                      # Tài liệu thuyết minh dữ liệu thực nghiệm
├── sample/                        # Bộ 20 mẫu chuẩn phục vụ phát triển & kiểm thử nhanh
│   ├── images/                    # 20 ảnh cắt lát MRI não (.png, 256x256)
│   ├── masks/                     # 20 mặt nạ Ground Truth khối u nhị phân (.png, 256x256)
│   └── metadata.csv               # Bảng metadata thống kê diện tích và tỷ lệ u của 20 mẫu
├── raw/                           # (Đã cấu hình .gitignore) Lưu toàn bộ 3,929 lát cắt khi mở rộng
└── processed/                     # (Đã cấu hình .gitignore) Lưu kết quả sau tách sọ và tiền xử lý
```

---

## 🔬 3. Quy Cách Mặt Nạ Ground Truth (Binary Mask)

Mỗi file ảnh mặt nạ trong `data/sample/masks/` tương ứng 1-1 với ảnh MRI trong `data/sample/images/`:
* **Kích thước chuẩn:** $256 \times 256$ pixels.
* **Giá trị 0 (Đen):** Mô não lành / Hộp sọ / Vùng ngoài sọ (Background).
* **Giá trị 255 (Trắng):** Vùng nhu mô u não (Core Tumor / Lesion Foreground).
* **Định lượng diện tích u:**
  * Diện tích u: $S_{\text{tumor}} = \sum_{(x,y)} \mathbb{I}(M(x, y) = 255)$ (đơn vị: pixels).
  * Tỷ lệ phần trăm u trên thiết diện não: $\text{Ratio} = \frac{S_{\text{tumor}}}{256 \times 256} \times 100\%$.

---

## 📊 4. Thống Kê 20 Mẫu Mẫu Đang Có Trong `data/sample/`

Bộ 20 mẫu được lựa chọn kỹ lưỡng từ 10 bệnh nhân khác nhau, đảm bảo đầy đủ các kịch bản thực tế:
* **U nhỏ (< 1.5% diện tích ảnh):** Ca 05, 11, 12, 13, 16, 19, 20 (Thách thức với thuật toán phân ngưỡng toàn cục).
* **U trung bình (1.5% – 5%):** Ca 01, 02, 03, 04, 06, 14, 15, 17, 18.
* **U lớn (> 5% – 10%):** Ca 07, 08, 09, 10 (U lan rộng, có hiệu ứng chèn ép não thất).

Toàn bộ thông tin chi tiết từng lát cắt được lưu tại [data/sample/metadata.csv](file:///C:/Users/xpaga/Documents/xlas/data/sample/metadata.csv).
