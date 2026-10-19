# Phân Đoạn & Phát Hiện Khối U Não Trên Ảnh Cộng Hưởng Từ (MRI)
### Brain Tumor Segmentation and Detection in Magnetic Resonance Imaging (MRI)

> **Đồ án kết thúc học phần:** Xử lý ảnh số (Digital Image Processing)  
> **Đơn vị:** Bộ môn Khoa học Dữ liệu — Khoa Công nghệ Thông tin — Trường Đại học Công Thương TP. Hồ Chí Minh (HUIT)  
> **Năm học:** 2026–2027  
> **Repository:** [brain-tumor-mri-segmentation](https://github.com/mtzwyu/brain-tumor-mri-segmentation)

---

## 👥 Nhóm sinh viên thực hiện

| STT | Họ và Tên | Mã số sinh viên (MSSV) | Vai trò / Phân công chính |
| :---: | :--- | :---: | :--- |
| 1 | **Hà Mạnh Trường** | **2045240326** | **Trưởng nhóm**, Pipeline tiền xử lý & Tách sọ não (Skull Stripping), Thuật toán phân đoạn u não lõi (Watershed/Region Growing), Báo cáo khoa học |
| 2 | **Huỳnh Tâm Trí** | **2045240315** | **Thành viên**, Thu thập & chuẩn hóa dữ liệu MRI Ground Truth, Rút trích đặc trưng hình học khối u, Đánh giá định lượng (Dice/IoU), Demo GUI |

---

## 🎯 1. Mục tiêu và Ý nghĩa Đề tài

* **Bối cảnh y tế:** Khối u não (Brain Tumor: u tế bào đệm - Glioma, u màng não - Meningioma, u tuyến yên - Pituitary) là một trong những bệnh lý thần kinh nguy hiểm nhất. Ảnh cộng hưởng từ (MRI) là tiêu chuẩn vàng trong chẩn đoán, nhưng việc khoanh vùng thủ công tốn nhiều thời gian và phụ thuộc chủ quan vào kinh nghiệm bác sĩ.
* **Mục tiêu đầu vào:** Ảnh chụp MRI sọ não 2D lát cắt (Axial/Coronal/Sagittal) ở chuỗi xung T1-CE hoặc FLAIR (định dạng JPG, PNG).
* **Mục tiêu đầu ra:**
  1. Mặt nạ phân đoạn khối u não (Binary Segmentation Mask).
  2. Hộp giới hạn (Bounding Box) và đường bao (Contour) định vị ổ u não.
  3. Báo cáo định lượng y tế: Diện tích khối u ($S_{\text{tumor}}$), tọa độ tâm u (Centroid), độ gồ ghề bờ u (Circularity), và tỷ lệ % u/nhu mô não.
  4. Đánh giá so sánh với Ground Truth chuyên gia qua: **Dice Score, IoU, Sensitivity, Specificity**.
* **Nguyên tắc kỹ thuật cốt lõi:** Lấy kỹ thuật **Xử lý ảnh số cổ điển (Digital Image Processing - DIP)** làm trọng tâm thực nghiệm, xây dựng bước tách hộp sọ (**Skull Stripping**) bằng hình thái học và so sánh tối thiểu 2 phương án phân đoạn theo đúng đề cương Bộ môn.

---

## 🔬 2. Sơ đồ Pipeline Xử lý 7 Bước

```
[Ảnh MRI Sọ Não Gốc (T1-CE / FLAIR)]
                │
                ▼
1. 【Tiền xử lý & Cải thiện chất lượng ảnh】
   ├── Chuẩn hóa kích thước (512x512) & dải pixel [0, 255]
   ├── Khử nhiễu Rician: Lọc trung vị (Median Filter) & Lọc Bilateral bảo toàn biên u
   └── Tăng cường tương phản mô mềm não: CLAHE (kênh xám)
                │
                ▼
2. 【Tách sọ não (Skull Stripping - Kỹ thuật DIP kinh điển)】
   ├── Phân ngưỡng nhị phân loại bỏ nền ngoài sọ
   ├── Phép toán hình thái học (Morphological Opening/Closing) cắt cầu nối mô
   ├── Tìm thành phần liên thông lớn nhất (Largest Connected Component)
   └── Sinh mặt nạ nhu mô não (Brain Mask) loại bỏ hoàn toàn xương sọ và da đầu
                │
                ▼
3. 【Phân đoạn khối u lõi (Core Tumor Segmentation) — So sánh 2 phương án】
   ├── Phương án A (Baseline DIP cổ điển):
   │     Distance Transform ➔ Điểm hạt giống (Markers) ➔ Phân thủy Watershed
   │     HOẶC Phát triển vùng (Region Growing) từ điểm cực đại cường độ
   └── Phương án B (Cải tiến / Đối chứng):
         Phân cụm K-Means pixel trên không gian cường độ/kết cấu GLCM HOẶC Mạng U-Net
                │
                ▼
4. 【Định vị & Đo lường đặc trưng khối u】
   ├── Trích xuất Contour và Bounding Box màu đỏ cảnh báo quanh khối u
   ├── Tính toán diện tích khối u (S_tumor) và tỷ lệ % u / diện tích não
   └── Tính độ tròn (Circularity = 4π * Area / Perimeter^2) đánh giá độ gồ ghề bờ u
                │
                ▼
5. 【Đánh giá định lượng & Trực quan hóa】
   ├── So sánh mặt nạ dự đoán với Ground Truth: Dice (F1), IoU, Sensitivity, Specificity
   ├── Phân tích các ca u nhỏ, u bờ mờ (Failure Cases)
   └── Đo thời gian xử lý trung bình mỗi ca chụp (ms)
                │
                ▼
6. 【Chương trình ứng dụng Demo (GUI)】
   └── Giao diện web Streamlit cho phép bác sĩ nạp ảnh MRI, chọn phương pháp, xem ảnh tách sọ, mặt nạ u và tải báo cáo kết quả
```

---

## 📂 3. Cấu trúc Thư mục Dự án

```
brain-tumor-mri-segmentation/
├── .agents/                        # Bộ kỹ năng AI Agent hỗ trợ phát triển (Matt Pocock Skills)
├── docs/                           # Tài liệu đề cương, báo cáo đồ án và kết quả thực nghiệm
│   ├── BAO_CAO_DO_AN_XLAS.md       # Báo cáo toàn văn đồ án định dạng Markdown
│   ├── BAO_CAO_DO_AN_XLAS.docx     # Báo cáo chuẩn thể thức Bộ Giáo dục (Times New Roman 13pt, lề 3-3-3-2 cm)
│   ├── BENCHMARK_RESULTS.csv       # Tổng hợp định lượng 3,929 lát cắt theo lát bệnh lý & não lành
│   ├── BENCHMARK_RESULTS_FULL.csv  # Chi tiết 7,858 kết quả thực nghiệm từng lát cắt
│   ├── DATA_EXPLORATION_REPORT.md  # Báo cáo thống kê dữ liệu 110 bệnh nhân TCGA-LGG
│   └── KHUNG_NOI_DUNG_TONG_QUAT... # Khung nội dung chuẩn hóa của Bộ môn
├── data/                           # Dữ liệu ảnh MRI sọ não
│   ├── README.md                   # Mô tả cấu trúc dữ liệu và quy cách mặt nạ u
│   └── full/                       # Toàn bộ 3,929 lát cắt chuẩn TCGA-LGG
│       ├── images/                 # 3,929 ảnh MRI (.png, 256x256)
│       ├── masks/                  # 3,929 mặt nạ Ground Truth (.png, 256x256)
│       └── metadata.csv            # Metadata chi tiết 110 bệnh nhân (được track trên Git)
├── src/                            # Mã nguồn module xử lý ảnh số lõi
│   ├── preprocessing/              # Lọc nhiễu Rician, CLAHE, Tách sọ (Skull Stripping)
│   ├── segmentation/               # Watershed & Marker Distance Transform, Region Growing
│   ├── measurement/                # Đo diện tích u, độ tròn Circularity, Bounding Box
│   └── evaluation/                 # Tính Dice, IoU, Sensitivity, Specificity
├── demo/                           # Ứng dụng giao diện minh họa (Streamlit GUI tương tác)
│   ├── app.py                      # Giao diện chính phân đoạn tương tác trên kho 3,929 lát cắt
│   └── utils.py                    # Tiện ích nạp ảnh và hiển thị

├── notebooks/                      # 4 Jupyter Notebooks thực nghiệm trực quan
│   ├── 01_data_exploration.ipynb   # Khám phá và phân tích phân bố dữ liệu
│   ├── 02_preprocessing_and_skull_stripping.ipynb # Khử nhiễu & tách sọ não
│   ├── 03_segmentation_comparison.ipynb # So sánh thuật toán phân đoạn
│   └── 04_quantitative_evaluation.ipynb # Đánh giá định lượng trên toàn bộ tập dữ liệu
├── scripts/                        # Scripts tự động hóa
│   ├── download_full_dataset.py    # Tải toàn bộ 3,929 lát cắt từ Hugging Face
│   ├── run_all_experiments.py      # Benchmark đa tiến trình xử lý 3,929 lát cắt (~25s)
│   ├── export_report_docx.py       # Xuất báo cáo Word đúng chuẩn lề 3-3-3-2 cm
│   └── create_notebooks.py         # Khởi tạo tự động các notebook thực nghiệm
├── tests/                          # Bộ kiểm thử đơn vị tự động (Pytest)
├── AGENTS.md                       # Thông tin nhóm & Quy chuẩn kỹ thuật toàn cục
├── requirements.txt                # Thư viện phụ thuộc (OpenCV, NumPy, Streamlit, python-docx...)
└── README.md                       # Tài liệu tổng quan dự án
```

---

## 📊 4. Kết Quả Thực Nghiệm Benchmark Quy Mô Toàn Bộ Dữ Liệu (3,929 Lát Cắt)

Toàn bộ 3,929 lát cắt từ 110 bệnh nhân TCGA-LGG được phân tích và đánh giá định lượng độc lập giữa hai giải thuật DIP cổ điển:

| Nhóm dữ liệu kiểm thử | Phương pháp | Dice Score ($F_1$) | IoU (Jaccard) | Sensitivity | Specificity | Độ trễ (ms/ảnh) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Lát cắt có u (1,373 lát)** | **Marker-controlled Watershed** | **0.4446 ± 0.3014** | **0.3368 ± 0.2677** | **0.4436 ± 0.3170** | **0.9915 ± 0.0107** | **6.13 ± 3.32 ms** |
| | Region Growing | 0.1990 ± 0.2682 | 0.1416 ± 0.2119 | 0.2226 ± 0.3221 | 0.9851 ± 0.0432 | 12.13 ± 22.83 ms |
| **Lát não lành (2,556 lát)** | **Marker-controlled Watershed** | N/A (Không u) | N/A | N/A | **0.9904 ± 0.0100** | **6.15 ± 3.40 ms** |
| | Region Growing | N/A (Không u) | N/A | N/A | 0.9760 ± 0.0480 | 12.05 ± 21.50 ms |

> 📌 **Nhận xét chuyên môn:**
> 1. **Watershed vượt trội toàn diện:** Nhờ cơ chế gieo mầm hạt giống dựa trên biến đổi khoảng cách Euclid (Euclidean Distance Transform) trên mặt nạ tách sọ, Watershed đạt Dice 0.4446 (gấp 2.23 lần Region Growing) và thời gian thực thi ổn định chỉ ~6.13 ms/lát cắt.
> 2. **Kiểm soát dương tính giả tuyệt hảo:** Độ đặc hiệu (Specificity) trên lát não lành đạt **99.04%** (Watershed) và **97.60%** (Region Growing), khẳng định bước tách sọ não (Skull Stripping) loại bỏ triệt để tín hiệu nhiễu từ hộp sọ và màng não.

---

## 🚀 5. Hướng Dẫn Cài Đặt & Chạy Hệ Thống (Quickstart)

### Bước 1: Cài đặt môi trường
```bash
git clone https://github.com/mtzwyu/brain-tumor-mri-segmentation.git
cd brain-tumor-mri-segmentation
pip install -r requirements.txt
```

### Bước 2: Tải dữ liệu toàn bộ (3,929 lát cắt)
```bash
# Tải và giải nén tự động 3,929 lát cắt từ Hugging Face (~1-2 phút tùy mạng)
python scripts/download_full_dataset.py
```

### Bước 3: Chạy Benchmark đa tiến trình toàn bộ 3,929 lát cắt
```bash
# Chạy đánh giá đa luồng tốc độ cao (~25 giây hoàn thành toàn bộ 3,929 ảnh)
python scripts/run_all_experiments.py
```

### Bước 4: Khởi chạy Giao diện Tương tác Web (Streamlit Demo)
```bash
streamlit run demo/app.py
```

### Bước 5: Chạy Kiểm thử Đơn vị Tự động (Unit Tests)
```bash
pytest -v
```

---

## 📋 6. Kế Hoạch Triển Khai Cấp Tốc 7 Ngày & Khung Đánh Giá Đồ Án Chuẩn HUIT

### 6.1. Khung Tiêu Chí Đánh Giá (Rubric 5 Tiêu Chí - Thang Điểm 10)
> Theo *Kế hoạch thực hiện Đồ án Xử lý ảnh số năm học 2026–2027* của Khoa CNTT — HUIT, điểm đồ án chiếm **100% điểm thi kết thúc học phần** (tương đương **70% tổng điểm học phần**):

| STT | Tiêu chí đánh giá | Chuẩn đầu ra (PLO/CLO) | Trọng số | Điểm tối đa |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Phân tích và lựa chọn đúng phương pháp | PLO2 / CLO1 | 15% | 1.5 điểm |
| 2 | **Áp dụng được các phương pháp xử lý (Trọng tâm)** | PLO2 / CLO2 | **50%** | **5.0 điểm** |
| 3 | Đọc tài liệu, nghiên cứu giải quyết bài toán | PLO4 / CLO3 | 10% | 1.0 điểm |
| 4 | Trình bày báo cáo | PLO7 / CLO5 | 15% | 1.5 điểm |
| 5 | Phân công và phối hợp làm việc nhóm | PLO6 / CLO4 | 10% | 1.0 điểm |
| **TỔNG** | **ĐIỂM ĐÁNH GIÁ CUỐI KỲ** | **ĐẠT CHUẨN ĐẦU RA** | **100%** | **10.0 điểm** |

### 6.2. Lộ Trình Sprint Cấp Tốc 7 Ngày Triển Khai Chi Tiết
* **Ngày 1 (Khởi động, Dữ liệu & Đặc tả toán học):** Phân công vai trò 50%-50%, chuẩn hóa toàn bộ 3,929 lát cắt dữ liệu TCGA-LGG, chạy Notebook 01 EDA và soạn thảo đặc tả kỹ thuật `docs/SPEC_PIPELINE_MRI.md`.

* **Ngày 2 (Tiền xử lý, Tách sọ não & Bộ đo y sinh):** Hiện thực hóa quy trình 6 bước Tách sọ não (*Skull Stripping*) loại bỏ xương sọ, lọc Bilateral + CLAHE, hoàn thiện Notebook 02 và cài đặt module `src/evaluation/metrics.py` (Dice, IoU, Sensitivity, Specificity).
* **Ngày 3 (Phân đoạn Baseline Watershed & Đo đặc trưng hình học):** Hiện thực hóa Marker-controlled Watershed với biến đổi khoảng cách EDT, cài đặt module `src/measurement/features.py` (Diện tích, Tỷ lệ u/não, Circularity) và trực quan hóa Bounding Box cảnh báo đỏ.
* **Ngày 4 (Phân đoạn Đối chứng Region Growing & Ghép nối Pipeline):** Hiện thực hóa Seeded Region Growing (tự tìm seed cực đại cường độ, lan truyền 8 láng giềng BFS), hoàn thiện Notebook 03 và tích hợp lớp điều phối `BrainTumorPipeline` trong `src/pipeline.py`.
* **Ngày 5 (Benchmark 3,929 lát cắt & Ứng dụng Web Demo):** Chạy thực nghiệm định lượng đa tiến trình trên toàn bộ 3,929 lát cắt, phân tích chuyên sâu các ca thất bại (*Failure Cases*), hoàn thiện Notebook 04 và hoàn thành giao diện Web Streamlit GUI (`demo/app.py`).
* **Ngày 6 (Biên soạn Báo cáo Đồ án 12 Mục):** Soạn thảo 4 chương kỹ thuật và 6 chương tổng quan, ghép nối hoàn chỉnh Báo cáo toàn văn `docs/BAO_CAO_DO_AN_XLAS.md` và xuất file Word `docs/BAO_CAO_DO_AN_XLAS.docx` chuẩn thể thức HUIT.
* **Ngày 7 (Slide thuyết trình, Video Demo, Test 12/12 & Đóng gói):** Rà soát mã nguồn `src/` (12/12 unit tests PASSED), thiết kế bộ Slide 20 trang (`docs/SLIDE_THUYET_TRINH_OUTLINE.md`), quay Video demo 3 phút và đóng gói hồ sơ nộp đồ án.

### 6.3. Chi Tiết Nhiệm Vụ Từng Sinh Viên
* [Kế hoạch nhiệm vụ cấp tốc 7 ngày của Hà Mạnh Trường (Nhóm trưởng)](docs/NHIEM_VU_HA_MANH_TRUONG.md)
* [Kế hoạch nhiệm vụ cấp tốc 7 ngày của Huỳnh Tâm Trí (Thành viên)](docs/NHIEM_VU_HUYNH_TAM_TRI.md)
* [Báo cáo toàn văn đồ án 12 mục (Markdown)](docs/BAO_CAO_DO_AN_XLAS.md)
* [Báo cáo đồ án định dạng Microsoft Word chuẩn HUIT](docs/BAO_CAO_DO_AN_XLAS.docx)

