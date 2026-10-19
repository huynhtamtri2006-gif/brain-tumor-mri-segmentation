# ĐẶC TẢ KỸ THUẬT KIẾN TRÚC PIPELINE XỬ LÝ ẢNH SỐ
## Đề tài: Phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ (MRI)
**Học phần:** Xử lý ảnh số (2026–2027) — Khoa CNTT — Trường ĐH Công Thương TP.HCM (HUIT)  
**Tác giả đặc tả:** Hà Mạnh Trường (MSSV: `2045240326`) — Nhóm trưởng  
**Người phản biện:** Huỳnh Tâm Trí (MSSV: `2045240315`)  
**Phiên bản:** 1.1 — Ngày 1 (18/10/2026) · Hợp đồng interface đóng băng, không thay đổi chữ ký hàm trong `src/`

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

Nguồn duy nhất (single source of truth) cho siêu tham số là `configs/default_params.yaml`. Bảng dưới đây ánh xạ từng khoá cấu hình sang keyword argument thực thi kèm căn cứ lý thuyết DIP; giá trị đã được đối chiếu với giá trị mặc định trong mã nguồn tại Ngày 1.

| # | Khoá trong `default_params.yaml` | Giá trị | Keyword argument đích | Căn cứ lý thuyết DIP |
| :---: | :--- | :---: | :--- | :--- |
| 1 | `preprocessing.bilateral_filter.d` | 9 | `apply_bilateral_filter(d=9)` | G&W §5.3.4: cửa sổ lẻ đối xứng quanh điểm ảnh trung tâm; `d=9` tương ứng bán kính lân cận 4 pixel, đủ mẫu cho cả hai nhân Gauss. |
| 2 | `preprocessing.bilateral_filter.sigma_color` | 75.0 | `apply_bilateral_filter(sigma_color=75.0)` | Với ảnh 8-bit, $\sigma_r \approx 0.3 \times L = 76.5$: chênh lệch mức xám vượt ~$1\sigma_r$ bị coi là khác mô nên trọng số tiến về 0, bảo toàn độ dốc biên u. |
| 3 | `preprocessing.bilateral_filter.sigma_space` | 75.0 | `apply_bilateral_filter(sigma_space=75.0)` | $\sigma_s$ điều khiển phạm vi không gian của nhân; giá trị chuẩn OpenCV cho ảnh 8-bit. Do $\sigma_s \gg d/2$, cửa sổ `d` mới là giới hạn không gian hiệu dụng (xem phát hiện R5). |
| 4 | `preprocessing.clahe.clip_limit` | 2.0 | `apply_clahe(clip_limit=2.0)` | G&W §3.3.3: clip limit chặn việc khuếch đại nhiễu ở các bin histogram thấp; 2.0 là mức tăng cường vừa phải cho MRI. |
| 5 | `preprocessing.clahe.tile_grid_size` | `[8, 8]` | `apply_clahe(tile_grid_size=(8, 8))` | Chia ảnh 256×256 thành 64 ô 32×32: đủ lớn để histogram cục bộ ổn định, đủ nhỏ để thích ứng theo vùng mô. |
| 6 | `preprocessing.skull_stripping.kernel_size` | 5 | `extract_brain_mask(kernel_size=5)` | G&W §9.6: phần tử cấu trúc elip xấp xỉ đĩa bán kính 2; đủ cắt cầu nối mô mỏng giữa màng cứng và vỏ não mà không ăn mòn nhu mô. |
| 7 | `preprocessing.skull_stripping.morph_iterations` | 2 | `cv2.morphologyEx(..., iterations=2)` (cố định trong mã) | Hai lần Opening liên tiếp tương đương một phần tử cấu trúc hiệu dụng 9×9, đủ cắt cầu nối dày 3–4 pixel. |
| 8 | `segmentation.watershed.dist_thresh_ratio` | 0.4 | `segment_watershed(dist_thresh_ratio=0.4)` | Sure Foreground $= 0.4 \times \max(D)$: chỉ giữ các đỉnh khoảng cách ≥ 40% bán kính u, triệt tiêu marker nhiễu nhỏ. |
| 9 | `segmentation.watershed.bg_dilate_kernel` | 3 | `segment_watershed(bg_dilate_kernel=3)` | Dilation 3×3 lặp 2 vòng tạo dải Unknown hẹp quanh biên u, tránh hiện tượng watershed tràn sang nhu mô lành. |
| 10 | `segmentation.region_growing.intensity_tolerance` | 15 | `segment_region_growing(tolerance=15)` | $\lvert I(q) - I(\text{seed}) \rvert \le 15 \approx 5.9\%$ dải động 8-bit: đủ thu nạp mô u đồng nhất, chặn lan sang nhu mô tối. |
| 11 | `segmentation.region_growing.min_tumor_area` | 50 | `segment_region_growing(min_area=50)` | 50 px ≈ 0.076% diện tích 256×256 — sàn loại bỏ nhiễu đốm đơn lẻ. |
| 12 | `segmentation.region_growing.max_tumor_area` | 25000 | `segment_region_growing(max_area=25000)` | 25 000 px ≈ 38.1% diện tích não — chặn trường hợp vùng lan tràn toàn bộ nhu mô. |
| 13 | `measurement.min_contour_area` | 30 | `extract_tumor_features(min_area_thresh=30)` | Sàn công nhận u ở tầng đo lường, đặt thấp hơn `min_tumor_area` để không loại oan các u nhỏ do Watershed phát hiện (ràng buộc R6). |
| 14 | `measurement.bbox_color` | `[0, 0, 255]` | `draw_tumor_overlay(color_bgr=(0, 0, 255))` | Không gian màu BGR của OpenCV: $(0, 0, 255)$ là đỏ — màu cảnh báo tổn thương. |
| 15 | `measurement.bbox_thickness` | 2 | `draw_tumor_overlay(thickness=2)` | Nét 2 px đủ hiển thị trên ảnh 256×256 mà không che khuất mô u. |

### 3.1. Kết quả rà soát cấu hình — Ngày 1

**Kết luận:** toàn bộ 15 giá trị mặc định trong YAML khớp với giá trị mặc định của mã nguồn và nằm trong dải hợp lý của lý thuyết DIP; **không cần đổi giá trị nào**. Các phát hiện dưới đây là bất cập về *nối dây cấu hình* (wiring) và *tài liệu hoá*, được xử lý bằng ghi chú thay vì sửa chữ ký hàm (theo checklist Ngày 1: hợp đồng hàm với Trí được đóng băng).

| Mã | Phát hiện | Ảnh hưởng | Hành động |
| :---: | :--- | :--- | :--- |
| **R1** | `preprocessing.clahe.*` chưa được `BrainTumorPipeline.process()` gọi — Tầng 1 hiện chỉ chạy Bilateral Filter. | Thiếu tăng cường tương phản cục bộ trước ngưỡng Otsu; có thể lệch ngưỡng trên ca tương phản thấp. | Giữ nguyên chữ ký hàm; bổ sung lời gọi `apply_clahe` trong `process()` ở Ngày 5 (một dòng, không phá hợp đồng). |
| **R2** | `morph_iterations` và số vòng lặp dilation của Watershed (`iterations=2`) không phải keyword argument — mã cố định giá trị. | Sửa YAML không làm thay đổi hành vi thực thi. | Ghi rõ tại §4.3 và §4.4; nếu cần khảo sát thì mở rộng chữ ký ở Ngày 2/3 và cập nhật tài liệu này. |
| **R3** | Pipeline không truyền `min_tumor_area`, `max_tumor_area`, `bg_dilate_kernel`, `min_contour_area`, `bbox_color`, `bbox_thickness`. | Giá trị hiệu dụng = giá trị mặc định của hàm; hiện trùng khớp YAML nên **không sai lệch kết quả**. | Nối dây đầy đủ ở Ngày 5 khi hoàn thiện `pipeline.py`. |
| **R4** | Watershed dùng phân vị cường độ 85 cố định (`np.percentile(non_zero_pixels, 85)`) — hằng số chưa có trong YAML. | Không thể khảo sát ngưỡng tiền lọc vùng tăng sáng qua cấu hình. | Ghi nhận; đưa thành tham số cấu hình khi mở rộng chữ ký (Ngày 3). |
| **R5** | $\sigma_s = 75 \gg d/2 = 4.5$ nên trọng số không gian gần như hằng trong cửa sổ 9×9; tính bảo toàn biên chủ yếu nhờ $\sigma_r$. | Không sai lý thuyết (nhân vẫn tách được), nhưng bộ lọc thiên về trung bình có trọng số cường độ hơn là lọc không gian cục bộ. | Giữ giá trị baseline; khảo sát cặp $(d, \sigma_s)$ ở Ngày 5 trước khi chốt số liệu báo cáo. |
| **R6** | `min_contour_area` (30) < `min_tumor_area` (50). | Hợp lý: Watershed không có bộ lọc diện tích, nên tầng đo lường cần sàn riêng; Region Growing đã tự lọc dưới 50 px. | Giữ nguyên; ghi ràng buộc `0 < min_contour_area <= min_tumor_area` trong YAML. |

---

## 🔌 4. Hợp Đồng Interface 5 Module Lõi

Đây là **hợp đồng đóng băng (frozen contract)** tại Ngày 1 giữa Hà Mạnh Trường (module tiền xử lý/phân đoạn/pipeline) và Huỳnh Tâm Trí (module đo lường/đánh giá + GUI). Mọi thay đổi chữ ký hàm trong `src/` phải được cập nhật vào mục này và thông báo cho đầu mối còn lại trước khi merge.

### 4.1. Quy ước kiểu dữ liệu dùng chung

| Ký hiệu | Định nghĩa | Ràng buộc |
| :--- | :--- | :--- |
| `Image` | `np.ndarray`, shape `(H, W)` | `dtype=np.uint8`, miền giá trị `[0, 255]`; ảnh mẫu `H = W = 256`. |
| `Mask` | `np.ndarray`, shape `(H, W)` | `dtype=np.uint8`, **nhị phân cứng** `{0, 255}` (không dùng `bool`). |
| `Point` | `Tuple[int, int]` | Thứ tự `(y, x)` = (hàng, cột) — **ngược** với `(x, y)` của OpenCV. |
| `BBox` | `Tuple[int, int, int, int]` | `(x, y, w, h)` theo `cv2.boundingRect`. |
| `Params` | `Dict[str, Any]` | Dict **phẳng**, không phải cây YAML lồng nhau (xem §4.7). |

**Bất biến chung của cả 5 module:**
1. **Pure function:** không sửa dữ liệu đầu vào, không đọc/ghi file, không dùng RNG $\Rightarrow$ cùng input cho cùng output (tất định).
2. **Shape-preserving:** đầu ra ảnh/mặt nạ luôn cùng `(H, W)` với đầu vào trừ `overlay` `(H, W, 3)` và `quad` `(2H, 2W, 3)`.
3. **Fail-safe:** không ném ngoại lệ với dữ liệu hợp lệ; trường hợp suy biến (ảnh rỗng, không có foreground) trả mặt nạ toàn `0` thay vì lỗi.
4. **Không kiểm tra kiểu phòng vệ:** người gọi chịu trách nhiệm đảm bảo `dtype`/`shape`; truyền `float32` cho CLAHE hoặc mask sai kích thước sẽ để OpenCV ném lỗi.
5. **Constructor:** các `__init__` trả về `None` ngầm định; riêng `WatershedSegmenter.__init__` khai báo tường minh `-> None` từ Ngày 3 — cột chữ ký dưới đây phản ánh đúng `inspect.signature`.

### 4.2. Module `src/preprocessing/filters.py`

| Hàm | Chữ ký (type hints) | Input | Output |
| :--- | :--- | :--- | :--- |
| `apply_bilateral_filter` | `apply_bilateral_filter(image: np.ndarray, d: int = 9, sigma_color: float = 75.0, sigma_space: float = 75.0) -> np.ndarray` | `image`: ảnh xám `(H, W)` uint8 [0, 255]. Nếu là 3 kênh BGR, hàm tự chuyển sang xám trước khi lọc. `d`: số nguyên lẻ ≥ 5. | Ảnh `(H, W)` uint8 cùng shape; nhiễu Rician giảm, biên cường độ được bảo toàn. Ảnh gốc không bị thay đổi. |
| `apply_clahe` | `apply_clahe(image: np.ndarray, clip_limit: float = 2.0, tile_grid_size: Tuple[int, int] = (8, 8)) -> np.ndarray` | `image`: ảnh xám `(H, W)` uint8 (hoặc uint16). `clip_limit > 0`; `tile_grid_size` là `(rows, cols)` chia hết hoặc không chia hết đều được OpenCV xử lý. | Ảnh `(H, W)` uint8 đã cân bằng histogram cục bộ; vùng nền tối không bị khuếch đại nhiễu quá mức. |

*Hành vi phụ thuộc:* cả hai hàm đều trả về **ảnh mới**; khi đầu vào 3 kênh, đầu ra là ảnh xám 2D (thay đổi số chiều có kiểm soát). Có thể unpack trực tiếp từ YAML (`apply_clahe(image, **cfg['preprocessing']['clahe'])`) vì OpenCV chấp nhận `tile_grid_size` dạng `list` `[8, 8]` tương đương `tuple`.

### 4.3. Module `src/preprocessing/skull_strip.py`

| Hàm | Chữ ký (type hints) | Input | Output |
| :--- | :--- | :--- | :--- |
| `extract_brain_mask` | `extract_brain_mask(image: np.ndarray, kernel_size: int = 5, return_intermediates: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, Dict[str, np.ndarray]]]` | `image`: ảnh xám `(H, W)` uint8 (hoặc BGR). `kernel_size`: số lẻ ≥ 3 cho phần tử cấu trúc elip. Số vòng lặp Opening **cố định 2** (R2). | `Mask` `(H, W)` uint8 `{0, 255}` = hợp của thành phần liên thông lớn nhất (8-connectivity) và các lỗ được lấp. Trả toàn `0` nếu ảnh rỗng/không tách được foreground (`num_labels <= 1`). |
| `strip_skull` | `strip_skull(image: np.ndarray, brain_mask: Optional[np.ndarray] = None, return_intermediates: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, np.ndarray]]]` | `image`: ảnh xám `(H, W)` uint8. `brain_mask`: mặt nạ tính trước, **phải cùng shape**; `None` ⇒ tự gọi `extract_brain_mask(image)`. | `(stripped, mask)`: `stripped` `(H, W)` uint8 thoả `stripped[mask == 0] == 0`; `mask` `(H, W)` uint8 `{0, 255}`. |

*Tuỳ chọn trung gian (từ Ngày 2):* khi `return_intermediates=True`, `extract_brain_mask` trả `(mask, intermediates)` và `strip_skull` trả `(stripped, mask, intermediates)`; dict có đúng 8 khoá `original`, `denoised`, `otsu`, `opened`, `lcc`, `closed_and_filled`, `brain_mask`, `stripped`, tất cả `(H, W)` uint8. Mặc định `False` giữ nguyên hợp đồng cũ (tương thích ngược).

*Tiền điều kiện:* nếu truyền `brain_mask`, hàm **không** kiểm tra lại tính nhị phân — mask có giá trị khác `{0, 255}` sẽ được `cv2.bitwise_and` hiểu theo bit.

### 4.4. Module `src/segmentation/watershed.py`

| Thành phần | Chữ ký (type hints) | Input | Output |
| :--- | :--- | :--- | :--- |
| `WatershedSegmenter.__init__` | `__init__(self, dist_thresh_ratio: float = 0.4, bg_dilate_kernel: int = 3, min_tumor_area: int = 50) -> None` | `dist_thresh_ratio` ∈ (0, 1); `bg_dilate_kernel` số lẻ ≥ 1; `min_tumor_area` ≥ 0 (0 ⇒ không lọc đảo nhỏ). | Thực thể strategy; chưa xử lý ảnh. |
| `WatershedSegmenter.segment` | `segment(self, brain_image: np.ndarray, return_intermediates: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, Dict[str, np.ndarray]]]` | `brain_image`: ảnh não **đã tách sọ** `(H, W)` uint8. | `Mask` `(H, W)` uint8 `{0, 255}`; uỷ quyền cho `segment_watershed` với tham số đã lưu. |
| `segment_watershed` | `segment_watershed(brain_image: np.ndarray, dist_thresh_ratio: float = 0.4, bg_dilate_kernel: int = 3, min_tumor_area: int = 50, return_intermediates: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, Dict[str, np.ndarray]]]` | `brain_image`: `(H, W)` uint8; pixel nền ngoài não phải bằng `0`. Ngưỡng tiền lọc cường độ dùng **phân vị 85** cố định (R4), dilation nền lặp 2 vòng (R2); hậu xử lý loại đảo `< min_tumor_area` (8-connectivity). | `Mask` `(H, W)` uint8 `{0, 255}`. Suy biến: không có pixel `> 0` hoặc `max(dist_transform) == 0` ⇒ ma trận `0`. |

*Tuỳ chọn trung gian (từ Ngày 3):* khi `return_intermediates=True`, `segment_watershed` trả `(tumor_mask, intermediates)` với đúng 9 khoá `original`, `binary_high`, `opened`, `dist_transform`, `sure_fg`, `sure_bg`, `unknown`, `markers`, `tumor_mask` — tất cả `(H, W)` uint8 (`dist_transform` được chuẩn hoá min–max về `[0, 255]`, `markers` là marker đầu vào trước `cv2.watershed`). Mặc định `False` giữ nguyên hợp đồng cũ.

*Hậu điều kiện:* `np.unique(out).issubset({0, 255})` luôn đúng; vùng u là các marker `> 1` sau `cv2.watershed` (loại nền `1` và đường phân thủy `-1`).

### 4.5. Module `src/segmentation/region_growing.py`

| Thành phần | Chữ ký (type hints) | Input | Output |
| :--- | :--- | :--- | :--- |
| `RegionGrowingSegmenter.__init__` | `__init__(self, tolerance: int = 15, min_area: int = 50, max_area: int = 25000)` | `tolerance` ≥ 0 (đơn vị mức xám); `0 < min_area ≤ max_area`. | Thực thể strategy. |
| `RegionGrowingSegmenter.segment` | `segment(self, brain_image: np.ndarray) -> np.ndarray` | `brain_image`: ảnh não đã tách sọ `(H, W)` uint8. | `Mask` `(H, W)` uint8 `{0, 255}`; uỷ quyền cho `segment_region_growing`. |
| `find_seed_point` | `find_seed_point(brain_image: np.ndarray) -> Optional[Tuple[int, int]]` | `brain_image`: `(H, W)` uint8. Hàm làm mịn Gaussian 5×5 rồi lấy cực đại toàn cục. | `(y, x)` của pixel sáng nhất; `None` nếu ảnh toàn `0`. |
| `segment_region_growing` | `segment_region_growing(brain_image: np.ndarray, tolerance: int = 15, seed_point: Optional[Tuple[int, int]] = None, min_area: int = 50, max_area: int = 25000) -> np.ndarray` | `brain_image`: `(H, W)` uint8. `seed_point`: `(hàng, cột)` trong `[0, H) × [0, W)`; `None` ⇒ tự gọi `find_seed_point`. | `Mask` `(H, W)` uint8 `{0, 255}`. Nếu `pixel_count` ngoài `[min_area, max_area]` ⇒ mặt nạ bị xoá về `0` (coi như không có u). |

*Hậu điều kiện:* vùng phát triển chỉ chứa pixel `> 0` (không vượt ra ngoài nhu mô) và mọi pixel thoả $|I(q) - I(\text{seed})| \le \text{tolerance}$.

### 4.6. Module `src/pipeline.py` (lớp điều phối)

| Thành phần | Chữ ký (type hints) | Input | Output |
| :--- | :--- | :--- | :--- |
| `BrainTumorPipeline.__init__` | `__init__(self, method: str = "watershed", params: Optional[Dict[str, Any]] = None)` | `method`: `"watershed"` hoặc `"region_growing"` (không phân biệt hoa/thường; giá trị khác rơi vào nhánh watershed). `params`: dict phẳng siêu tham số (§4.7); `None` ⇒ `{}`. | Thực thể pipeline; chưa xử lý ảnh. |
| `BrainTumorPipeline.process` | `process(self, image: np.ndarray, gt_mask: Optional[np.ndarray] = None) -> Tuple[DiagnosticResult, Dict[str, np.ndarray]]` | `image`: ảnh MRI gốc `(H, W)` uint8. `gt_mask`: mặt nạ chuyên gia `(H, W)` nhị phân, tuỳ chọn; nếu có sẽ tính Dice/IoU. | `(DiagnosticResult, intermediates)`: kết quả đo lường + dict ảnh trung gian. `dice_score`/`iou_score` chỉ được điền khi `gt_mask is not None`, ngược lại giữ `None`. |

*Ghi chú annotation:* `DiagnosticResult` được import từ `src.measurement.features`; `inspect.signature` hiển thị đầy đủ đường dẫn module (`src.measurement.features.DiagnosticResult`) nhưng là cùng một lớp.

**Hợp đồng `intermediates` (khoá cố định, không thêm/bớt):**

| Khoá | Shape / dtype | Ý nghĩa |
| :--- | :--- | :--- |
| `original` | `(H, W)` uint8 | Ảnh MRI gốc, không sửa đổi. |
| `filtered` | `(H, W)` uint8 | Kết quả Bilateral Filter (hiện chưa qua CLAHE — R1). |
| `stripped` | `(H, W)` uint8 | Nhu mô não sau tách sọ; pixel ngoài `brain_mask` bằng `0`. |
| `brain_mask` | `(H, W)` uint8 `{0, 255}` | Mặt nạ não từ `strip_skull`. |
| `tumor_mask` | `(H, W)` uint8 `{0, 255}` | Mặt nạ u từ thuật toán đã chọn. |
| `overlay` | `(H, W, 3)` uint8 BGR | Ảnh gốc + Bounding Box + đường bao u. |
| `quad` | `(2H, 2W, 3)` uint8 BGR | Lưới so sánh 2×2: Gốc • Tách sọ • Mặt nạ • Khoanh u. |

### 4.7. Ánh xạ cấu hình YAML ↔ tham số pipeline

`BrainTumorPipeline` nhận **dict phẳng**, không nhận nguyên cây YAML. Bảng dưới ghi nhận trạng thái nối dây tại Ngày 1 (đối chiếu với §3.1):

| Khoá phẳng trong `params` | Đích thực thi | Trạng thái |
| :--- | :--- | :--- |
| `dist_thresh_ratio` | `segment_watershed(dist_thresh_ratio=...)` | ✅ Đã nối |
| `intensity_tolerance` | `segment_region_growing(tolerance=...)` | ✅ Đã nối (đổi tên khoá → tham số) |
| `min_tumor_area`, `max_tumor_area` | `RegionGrowingSegmenter.min_area/max_area` | ⚠️ Chưa truyền — dùng default (trùng giá trị YAML) |
| `bg_dilate_kernel` | `segment_watershed(bg_dilate_kernel=...)` | ⚠️ Chưa truyền — default 3 |
| `kernel_size`, `morph_iterations` | `extract_brain_mask` | ⚠️ Chưa truyền — default 5 / hard-code 2 |
| `clip_limit`, `tile_grid_size` | `apply_clahe` | ⚠️ Pipeline chưa gọi CLAHE (R1) |
| `min_contour_area`, `bbox_color`, `bbox_thickness` | `extract_tumor_features` / `draw_tumor_overlay` | ⚠️ Chưa truyền — default trùng giá trị YAML |

---

## 🧪 5. Bất Biến Dữ Liệu & Truy Vết Kiểm Thử

### 5.1. Bảng bất biến (invariants) phải luôn đúng

| # | Bất biến | Phạm vi |
| :---: | :--- | :--- |
| I1 | `out.shape == image.shape` với `out` là ảnh/mặt nạ mọi tầng | `filters`, `skull_strip`, `watershed`, `region_growing`, `pipeline` |
| I2 | `out.dtype == np.uint8` | Toàn bộ chuỗi xử lý |
| I3 | `set(np.unique(mask)).issubset({0, 255})` | Mọi mặt nạ (`brain_mask`, `tumor_mask`) |
| I4 | `np.all(stripped[brain_mask == 0] == 0)` | `strip_skull` |
| I5 | `overlay.shape == (H, W, 3)`, `quad.shape == (2H, 2W, 3)` | `pipeline.process` |
| I6 | `0.0 ≤ dice, iou, sensitivity, specificity ≤ 1.0` | `evaluation.metrics` |
| I7 | `quad` chứa đúng 4 ô: `original`, `stripped`, `tumor_mask`, `overlay` | `visualization.create_comparison_quad` |

### 5.2. Quy ước xử lý đầu vào suy biến

| Tình huống | Hành vi hợp đồng |
| :--- | :--- |
| Ảnh toàn `0` | `extract_brain_mask` → mask `0`; `find_seed_point` → `None`; `segment_*` → mask `0`; `extract_tumor_features` → `tumor_detected=False`. |
| Ảnh 3 kênh BGR | Tự chuyển xám (`cv2.COLOR_BGR2GRAY`) trước khi xử lý; đầu ra là ảnh 2D. |
| `gt_mask` rỗng và dự đoán rỗng | Quy ước Dice = IoU = 1.0 (âm tính đúng). |
| `gt_mask` rỗng nhưng dự đoán có u | Dice = IoU = 0.0. |
| Không có Ground Truth | `dice_score = iou_score = None` — **không** giả định bằng 0 để tránh sai lệch thống kê. |

### 5.3. Ma trận truy vết 12 unit test ↔ hợp đồng

| # | Test | Hợp đồng được kiểm chứng |
| :---: | :--- | :--- |
| 1 | `test_measurement.py::test_circularity_perfect_circle` | Công thức $C = 4\pi A / P^2$; cận `[0, 1]`; hình tròn rời rạc cho $C \ge 0.90$ (I6). |
| 2 | `test_measurement.py::test_extract_tumor_features` | `DiagnosticResult` có `tumor_detected`, `tumor_area_px > 0`, `0 ≤ circularity ≤ 1`, `bbox` 4 phần tử. |
| 3 | `test_measurement.py::test_visualization` | `overlay` 3 kênh cùng `(H, W)`; `quad` đúng `(2H, 2W)` (I5). |
| 4 | `test_metrics.py::test_perfect_match` | $P = G \Rightarrow$ Dice = IoU = Sens = Spec = 1.0. |
| 5 | `test_metrics.py::test_zero_overlap` | Hai vùng rời nhau ⇒ Dice, IoU, Sensitivity $\approx 0$. |
| 6 | `test_metrics.py::test_empty_masks` | Quy ước mask rỗng–rỗng ⇒ Dice = IoU = 1.0 (§5.2). |
| 7 | `test_metrics.py::test_calculate_all_metrics` | Schema dict `{dice, iou, sensitivity, specificity}`, giá trị trong `[0, 1]` (I6). |
| 8 | `test_preprocessing.py::test_bilateral_filter` | Bảo toàn shape và `dtype=uint8` sau lọc (I1, I2). |
| 9 | `test_preprocessing.py::test_clahe` | Bảo toàn shape và `dtype=uint8` sau CLAHE (I1, I2). |
| 10 | `test_preprocessing.py::test_skull_stripping` | Mask nhị phân `{0, 255}` (I3); `stripped[mask == 0] == 0` (I4). |
| 11 | `test_segmentation.py::test_watershed_segmentation` | Mask nhị phân (I3); `WatershedSegmenter.segment` cho cùng hợp đồng với hàm tự do. |
| 12 | `test_segmentation.py::test_region_growing_segmentation` | Seed nằm trong miền ảnh; mask nhị phân (I3); wrapper class tương đương hàm tự do. |

**Lệnh nghiệm thu Ngày 1:**
```bash
python -c "import yaml; print(yaml.safe_load(open('configs/default_params.yaml', encoding='utf-8')))"
python -m pytest -v
# Kỳ vọng: YAML parse thành công (15 khoá) và 12/12 tests PASSED
```
> **Lưu ý Windows:** file YAML chứa tiếng Việt UTF-8. Nếu chạy `open()` không có `encoding`, Python dùng codec hệ thống (ví dụ `cp1258`) và ném `UnicodeDecodeError`. Luôn truyền `encoding='utf-8'` hoặc đặt biến môi trường `PYTHONUTF8=1`.

---

## 📌 6. Lịch Sử Phiên Bản Đặc Tả

| Phiên bản | Ngày | Nội dung thay đổi |
| :---: | :---: | :--- |
| 1.0 | 18/10/2026 | Bản đầu: kiến trúc 4 tầng, cơ sở toán học Bilateral/Otsu/Morphology/Watershed/Region Growing, bảng siêu tham số rút gọn. |
| 1.1 | 18/10/2026 | Bổ sung căn cứ DIP cho từng tham số (§3), kết quả rà soát cấu hình R1–R6 (§3.1), hợp đồng interface 5 module với type hints (§4), bảng bất biến và ma trận truy vết 12 unit test (§5). Không thay đổi chữ ký hàm nào trong `src/`. |
