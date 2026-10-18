# ĐẶC TẢ KỸ THUẬT KIẾN TRÚC PIPELINE XỬ LÝ ẢNH SỐ
## Đề tài: Phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ (MRI)
**Học phần:** Xử lý ảnh số (2026–2027) — Khoa CNTT — Trường ĐH Công Thương TP.HCM (HUIT)  
**Tác giả đặc tả:** Hà Mạnh Trường (MSSV: `2045240326`) — Nhóm trưởng  
**Người phản biện:** Huỳnh Tâm Trí (MSSV: `2045240315`)

---

## 🎯 1. Tổng Quan Kiến Trúc & Sơ Đồ Khối Hệ Thống

Hệ thống được thiết kế theo mô hình luồng dữ liệu 4 tầng độc lập (4-Tier Dataflow Pipeline), đảm bảo 100% tuân thủ các nguyên lý xử lý ảnh số kinh điển (DIP) từ sách Gonzalez & Woods:

```
[Ảnh MRI Sọ Não Gốc (256x256 uint8)]
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│ TẦNG 1: TIỀN XỬ LÝ & LỌC NHIỄU BẢO TOÀN BIÊN              │
│ - Khử nhiễu Rician: Bilateral Filter (d=9, σ_c=75, σ_s=75)│
│ - Tăng cường tương phản cục bộ: CLAHE (clip_limit=2.0)    │
└──────────────────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│ TẦNG 2: TÁCH SỌ NÃO KINH ĐIỂN (SKULL STRIPPING)          │
│ - Ngưỡng tự động Otsu phân tách phần đầu khỏi nền        │
│ - Morphological Opening (Kernel elip 5x5) cắt cuống mô   │
│ - Trích xuất thành phần liên thông lớn nhất (LCC)        │
│ - Lấp đầy lỗ hổng (FloodFill Hole Filling) tạo Brain Mask │
│ - Bitwise-AND với ảnh gốc thu được ảnh não sạch sọ       │
└──────────────────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│ TẦNG 3: PHÂN ĐOẠN KHỐI U LÕI (SO SÁNH 2 PHƯƠNG ÁN)        │
│ ├── Phương án A (Baseline chính): Marker-controlled       │
│ │   Watershed + Euclidean Distance Transform             │
│ └── Phương án B (Đối chứng): Seeded Region Growing       │
│     (Tìm hạt giống cực đại cường độ + BFS 8 láng giềng)  │
└──────────────────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│ TẦNG 4: RÚT TRÍCH ĐẶC TRƯNG, ĐO LƯỜNG & ĐÁNH GIÁ ĐỊNH LƯỢNG│
│ - Đo diện tích u (S_tumor) và tỷ lệ % u/não              │
│ - Đo độ tròn Circularity = 4π*Area / Perimeter^2         │
│ - Trích xuất tọa độ Bounding Box & vẽ viền đỏ cảnh báo   │
│ - Tính chỉ số y khoa: Dice (DSC), IoU, Sens, Spec, Latency│
└──────────────────────────────────────────────────────────┘
```

---

## 🔬 2. Cơ Sở Toán Học & Giải Thuật Chi Tiết

### 2.1. Bộ lọc phi tuyến Bilateral Filter
Thay vì sử dụng bộ lọc Gaussian thông thường làm nhòe mờ đường biên khối u, Bilateral Filter kết hợp cả trọng số khoảng cách không gian hình học và trọng số chênh lệch cường độ xám:
$$I^{\text{filtered}}(p) = \frac{1}{W_p} \sum_{q \in S} I(q) \cdot G_{\sigma_s}(\|p - q\|) \cdot G_{\sigma_r}(|I(p) - I(q)|)$$
Trong đó:
* $G_{\sigma_s}(\|p - q\|) = \exp\left(-\frac{\|p - q\|^2}{2\sigma_s^2}\right)$ đo độ gần nhau về mặt vị trí hình học.
* $G_{\sigma_r}(|I(p) - I(q)|) = \exp\left(-\frac{|I(p) - I(q)|^2}{2\sigma_r^2}\right)$ đo độ tương đồng về mặt mức xám. Nếu chênh lệch mức xám lớn (biên khối u), trọng số này tiệm cận 0, giúp bảo toàn nguyên vẹn độ dốc biên u.

### 2.2. Kỹ thuật Tách sọ não (Skull Stripping Pipeline)
* **Bước 1: Ngưỡng tự động Otsu:**
  Tìm ngưỡng $T^*$ cực đại hóa phương sai giữa các lớp (Between-Class Variance):
  $$\sigma_B^2(T) = \omega_0(T) \cdot \omega_1(T) \cdot [\mu_0(T) - \mu_1(T)]^2$$
* **Bước 2: Phép mở hình thái học (Morphological Opening):**
  $$A \circ B = (A \ominus B) \oplus B$$
  Sử dụng phần tử cấu trúc dạng đĩa elip kích thước $5 \times 5$ để cắt đứt các cầu nối mô mỏng giữa màng cứng sọ và vỏ não.
* **Bước 3: Trích xuất thành phần liên thông lớn nhất (LCC):**
  Lập chỉ mục các vùng liên thông 8 điểm:
  $$LCC = \arg\max_{k \in \{1, \dots, K\}} \text{Area}(R_k)$$
* **Bước 4: Lấp đầy lỗ trống não thất (Hole Filling):**
  Lấp đầy các hốc dịch não tủy bên trong nhu mô não bằng phép bù và FloodFill xuất phát từ biên $(0, 0)$.

### 2.3. Thuật toán Phân đoạn A: Marker-controlled Watershed
1. **Biến đổi khoảng cách Euclidean (Euclidean Distance Transform - EDT):**
   $$D(p) = \min_{q \in \text{Background}} \|p - q\|_2$$
   Tâm khối u có khoảng cách lớn nhất đến đường biên u, tạo thành các "đỉnh núi" cục bộ trên bản đồ khoảng cách.
2. **Xác định điểm hạt giống đánh dấu (Markers):**
   * *Sure Foreground:* Vùng chắc chắn là u: $D(p) > \text{threshold\_ratio} \times \max(D)$.
   * *Sure Background:* Giãn nở (Dilation) mặt nạ ban đầu.
   * *Unknown Region:* $\text{Unknown} = \text{Sure Background} - \text{Sure Foreground}$.
3. **Phân thủy địa hình:** Đổ nước từ các markers, xây dựng các đập chắn nước (watershed lines) khi các lưu vực gặp nhau.

### 2.4. Thuật toán Phân đoạn B: Seeded Region Growing
1. **Tự động tìm hạt giống (Seed Selection):**
   $$\text{Seed} = \arg\max_{(x, y) \in \text{Brain}} I(x, y)$$
2. **Quy tắc thu nạp láng giềng:**
   Một pixel láng giềng $q$ (trong kết nối 8 điểm) được kết nạp vào khối u $R$ nếu thỏa mãn:
   $$|I(q) - I(\text{Seed})| \le \text{tolerance}$$
3. **Điều kiện dừng:** Hàng đợi BFS rỗng hoặc kích thước vùng vượt quá diện tích tối đa cho phép.

---

## ⚙️ 3. Danh Mục Siêu Tham Số Hệ Thống

| Tên tham số | Module áp dụng | Giá trị mặc định | Giải thích ý nghĩa kỹ thuật |
| :--- | :--- | :---: | :--- |
| `d` | `filters.py` | 9 | Đường kính cửa sổ lân cận của bộ lọc Bilateral |
| `sigma_color` | `filters.py` | 75.0 | Độ nhạy lọc theo chênh lệch mức xám |
| `sigma_space` | `filters.py` | 75.0 | Độ nhạy lọc theo khoảng cách không gian |
| `clip_limit` | `filters.py` | 2.0 | Giới hạn độ dốc histogram trong CLAHE |
| `kernel_size` | `skull_strip.py` | 5 | Kích thước phần tử cấu trúc đĩa elip phép Opening |
| `dist_thresh_ratio` | `watershed.py` | 0.4 | Ngưỡng trích xuất đỉnh khoảng cách cực đại |
| `intensity_tolerance` | `region_growing.py`| 15 | Dung sai độ xám cho phép lan truyền vùng u |
