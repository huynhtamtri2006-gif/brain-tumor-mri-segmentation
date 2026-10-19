# Brain Tumor MRI Segmentation & Quantitative Analysis Pipeline

### Hệ thống Phân đoạn và Phân tích Định lượng Khối u Não trên Ảnh Cộng hưởng từ (MRI) bằng Kỹ thuật Xử lý Ảnh số Cổ điển (DIP)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests: Passing](https://img.shields.io/badge/Tests-16%20Passed-brightgreen.svg)](tests/)
[![Framework: OpenCV](https://img.shields.io/badge/Computer%20Vision-OpenCV-orange.svg)](https://opencv.org/)
[![GUI: Streamlit](https://img.shields.io/badge/Web%20GUI-Streamlit-red.svg)](https://streamlit.io/)
[![Dataset: TCGA-LGG](https://img.shields.io/badge/Dataset-TCGA--LGG%20(3%2C929%20slices)-blueviolet.svg)](https://wiki.cancerimagingarchive.net/display/Public/TCGA-LGG)

---

## 1. Tổng quan Dự án (Project Overview)

Chẩn đoán và khoanh vùng khối u não (Brain Tumor: U tế bào đệm - Glioma, U màng não - Meningioma, U tuyến yên - Pituitary) từ ảnh chụp cộng hưởng từ (MRI) là bài toán then chốt trong hỗ trợ điều trị y khoa thần kinh. Thông thường, việc xác định đường biên u bằng tay đòi hỏi nhiều thời gian và phụ thuộc lớn vào đánh giá chủ quan của bác sĩ chuyên khoa.

Dự án này phát triển một hệ thống mã nguồn mở hoàn chỉnh nhằm **tự động tách sọ não, phân đoạn khối u và trích xuất các thông số hình học lâm sàng** trên chuỗi xung MRI FLAIR (Fluid-Attenuated Inversion Recovery). Thay vì sử dụng các mạng nơ-ron tích chập sâu (Deep Learning) cồng kềnh đòi hỏi năng lực phần cứng GPU đắt đỏ và thiếu tính minh bạch (black-box), hệ thống ứng dụng toàn diện các giải thuật **Xử lý Ảnh số Cổ điển (Classical Digital Image Processing - DIP)** kết hợp hình thái học toán học và phân thủy có hạt giống kiểm soát.

### Ưu điểm kỹ thuật cốt lõi:
- **Tốc độ thời gian thực (Real-time Latency):** Thời gian xử lý trung bình chỉ **~6.13 ms / lát cắt**, hoàn toàn khả thi để nhúng vào các trạm làm việc lâm sàng tiêu chuẩn hoặc thiết bị y tế biên (Edge Computing) không có GPU rời.
- **Tính minh bạch toán học (Explainability):** Mọi công đoạn từ lọc nhiễu, tăng độ tương phản, tách màng não đến phát triển vùng đều được giải thích rõ ràng dựa trên lý thuyết giải tích không gian ảnh và hình thái học toán học.
- **Khả năng kiểm soát dương tính giả cao:** Đạt độ đặc hiệu (Specificity) **99.04%** trên lát cắt não lành, loại bỏ triệt để các phản xạ giả tạo từ xương sọ và mô mềm da đầu.

---

## 2. Tính năng Nổi bật (Key Features)

- **Quy trình Tách sọ Não 6 Bước (6-Stage Skull Stripping Pipeline):**
  - Tích hợp bộ lọc Bilateral Filter bảo toàn đường biên mô mềm kết hợp cân bằng biểu đồ mức xám thích ứng cục bộ (CLAHE).
  - Phân ngưỡng Otsu toàn cục kết hợp đóng/mở hình thái học (Morphological Opening & Closing) cắt đứt cầu nối mô.
  - Phép lọc thành phần liên thông lớn nhất (Largest Connected Component - LCC) bóc tách chính xác toàn bộ hộp sọ và màng não.
- **Động cơ Phân đoạn Đối chứng (Dual-Method Segmentation Engine):**
  - **Marker-controlled Watershed:** Ứng dụng biến đổi khoảng cách Euclid (Euclidean Distance Transform - EDT), tự động sinh mầm hạt giống cực đại cục bộ, ngăn chặn hoàn toàn hiện tượng quá phân đoạn (over-segmentation).
  - **Seeded Region Growing:** Tự động phát hiện hạt giống cường độ cực đại trong nhu mô não đã bóc sọ, lan truyền vùng theo kết nối 8 láng giềng dựa trên ngưỡng dung sai cường độ động.
- **Đo lường & Trích xuất Đặc trưng Hình học Y sinh (Clinical Geometric Metrics):**
  - Tự động trích xuất diện tích khối u ($S_{\text{tumor}}$ theo pixel và mm²), diện tích não ($S_{\text{brain}}$).
  - Tính toán tỷ lệ phần trăm u chiếm dụng thể tích não (Tumor-to-Brain Ratio).
  - Đánh giá độ gồ ghề của bờ viền u qua chỉ số hình học Circularity Index ($C = \frac{4\pi \cdot \text{Area}}{\text{Perimeter}^2}$) và bao lồi (Convex Hull).
- **Trực quan hóa & Cảnh báo Chẩn đoán (Diagnostic Visualization):**
  - Đóng khung Bounding Box cảnh báo màu đỏ xung quanh tổn thương.
  - Lớp phủ màu bán trong suốt (Alpha Blended Overlay) giúp bác sĩ đối chiếu trực tiếp vị trí u trên ảnh gốc.
- **Hệ thống Đánh giá Định lượng Y sinh Chuẩn mực (Medical Evaluation Framework):**
  - Cung cấp module kiểm chuẩn toàn diện: Dice Similarity Coefficient ($F_1$), IoU (Jaccard Index), Độ nhạy (Sensitivity/Recall), Độ đặc hiệu (Specificity), Độ chính xác (Accuracy).
- **Ứng dụng Web Tương tác (Streamlit Interactive Web App):**
  - Giao diện thân thiện cho phép tải ảnh MRI bất kỳ hoặc duyệt nhanh kho dữ liệu 3.929 lát cắt, điều chỉnh tham số tương tác và xem toàn bộ các bước xử lý trung gian.

---

## 3. Kiến trúc Pipeline Xử lý (Architecture Pipeline)

```
[Ảnh MRI Sọ Não Gốc (FLAIR / T1-CE)]
               │
               ▼
1. 【TIỀN XỬ LÝ (PREPROCESSING)】
   ├── Chuẩn hóa kích thước không gian (256x256) & dải giá trị [0, 255]
   ├── Lọc song phương Bilateral Filter khử nhiễu Rician và bảo toàn biên u
   └── Tăng cường tương phản cục bộ bằng CLAHE (Clip Limit = 2.0, Grid = 8x8)
               │
               ▼
2. 【TÁCH SỌ NÃO (SKULL STRIPPING)】
   ├── Phân ngưỡng Otsu tìm vùng mô tiềm năng
   ├── Phép mở hình thái học (Opening 5x5) loại bỏ cầu nối xương sọ
   ├── Trích xuất thành phần liên thông lớn nhất (Largest Connected Component)
   ├── Phép đóng hình thái học (Closing) lấp đầy khoang nội sọ
   └── Nhân chập mặt nạ sinh ảnh não đã bóc sọ (Stripped Brain)
               │
               ▼
3. 【PHÂN ĐOẠN Ổ U (CORE TUMOR SEGMENTATION)】
   ├── Tuyến A: Marker-controlled Watershed (Biến đổi khoảng cách EDT + Hạt giống)
   └── Tuyến B: Seeded Region Growing (Lan truyền 8 láng giềng từ cực đại cường độ)
               │
               ▼
4. 【TRÍCH XUẤT ĐẶC TRƯNG & TRỰC QUAN HÓA】
   ├── Định vị đường bao Contour, tính Bounding Box màu đỏ cảnh báo
   ├── Đo lường hình học: Diện tích u, Tỷ lệ u/não (%), Độ tròn Circularity
   └── Lớp phủ Overlay màu RGBA trên nền ảnh sọ não
               │
               ▼
5. 【ĐÁNH GIÁ ĐỊNH LƯỢNG LÂM SÀNG】
   └── So sánh định lượng với Ground Truth: Dice, IoU, Sensitivity, Specificity
```

---

## 4. Tập dữ liệu Thực nghiệm (Dataset)

Dự án sử dụng bộ dữ liệu chuẩn y sinh quốc tế **TCGA-LGG (The Cancer Genome Atlas Low-Grade Glioma)** được công bố bởi Buda et al. (2019):
- **Quy mô:** Bao gồm **3.929 lát cắt MRI** (kích thước 256x256 pixel) thu thập từ **110 bệnh nhân** mắc u tế bào đệm cấp độ thấp.
- **Phân loại lát cắt:**
  - **1.373 lát cắt bệnh lý** có chứa khối u não (đi kèm mặt nạ Ground Truth do chuyên gia X-quang thần kinh khoanh vùng).
  - **2.556 lát cắt nhu mô não lành** không chứa tổn thương (dùng để kiểm thử tỷ lệ dương tính giả).
- **Metadata đi kèm:** File `data/full/metadata.csv` lưu trữ thông tin định danh bệnh nhân, mã lát cắt, tình trạng có/không có u và diện tích u Ground Truth.

### Tải nhanh bộ dữ liệu:
Hệ thống cung cấp sẵn script tải và giải nén tự động 1 lệnh từ kho lưu trữ Hugging Face:
```bash
python scripts/download_full_dataset.py
```

---

## 5. Kết quả Thực nghiệm Định lượng (Benchmark Results)

Toàn bộ **3.929 lát cắt** được xử lý và đánh giá tự động đa tiến trình, so sánh giữa giải thuật **Marker-controlled Watershed** và **Seeded Region Growing**:

| Tập dữ liệu kiểm thử | Phương pháp | Dice Score ($F_1$) | IoU (Jaccard) | Độ nhạy (Sensitivity) | Độ đặc hiệu (Specificity) | Tốc độ xử lý (ms/ảnh) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Lát có u (1.373 lát)** | **Marker Watershed** | **0.4446 ± 0.3014** | **0.3368 ± 0.2677** | **0.4436 ± 0.3170** | **0.9915 ± 0.0107** | **6.13 ± 3.32 ms** |
| | Region Growing | 0.1990 ± 0.2682 | 0.1416 ± 0.2119 | 0.2226 ± 0.3221 | 0.9851 ± 0.0432 | 12.13 ± 22.83 ms |
| **Lát não lành (2.556 lát)** | **Marker Watershed** | N/A (Không u) | N/A | N/A | **0.9904 ± 0.0100** | **6.15 ± 3.40 ms** |
| | Region Growing | N/A (Không u) | N/A | N/A | 0.9760 ± 0.0480 | 12.05 ± 21.50 ms |

### Nhận xét thực nghiệm chuyên sâu:
1. **Watershed vượt trội về độ chính xác và tính ổn định:** Nhờ cơ chế gieo mầm dựa trên khoảng cách Euclidean Distance Transform, Marker Watershed đạt điểm Dice gấp **2.23 lần** so với Region Growing, đồng thời tốc độ thực thi nhanh hơn gấp 2 lần (~6.13 ms so với ~12.13 ms).
2. **Khả năng triệt tiêu dương tính giả xuất sắc:** Cả hai phương pháp đều đạt độ đặc hiệu trên **97.6% - 99.0%** trên toàn bộ 2.556 lát cắt não lành, minh chứng tính hiệu quả vượt bậc của bước tách sọ não (Skull Stripping) trong việc ngăn chặn bắt nhầm tín hiệu xương sọ.
3. **Phân tích các ca thách thức (Failure Cases):** Khối u có độ tương phản thấp hoặc nằm sát biên não thất có thể dẫn đến hiện tượng rò rỉ đường biên (leakage) ở Region Growing. Watershed xử lý tốt hơn nhưng vẫn gặp thách thức với các ổ u kích thước cực nhỏ (< 50 pixel).

---

## 6. Hướng dẫn Cài đặt & Khởi chạy (Quickstart)

### 6.1. Yêu cầu Hệ thống
- Hệ điều hành: Windows 10/11, macOS, hoặc Linux.
- Python: Phiên bản **3.10** trở lên.
- RAM: Tối thiểu 4 GB (Khuyến nghị 8 GB để benchmark đa tiến trình tốc độ cao).

### 6.2. Cài đặt Môi trường
```bash
# 1. Clone repository về máy
git clone https://github.com/mtzwyu/brain-tumor-mri-segmentation.git
cd brain-tumor-mri-segmentation

# 2. Tạo môi trường ảo (khuyến nghị)
python -m venv venv
# Trên Windows:
.\venv\Scripts\activate
# Trên Linux/macOS:
source venv/bin/activate

# 3. Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt
```

### 6.3. Tải Dữ liệu Đầy đủ
```bash
python scripts/download_full_dataset.py
```

### 6.4. Khởi chạy Ứng dụng Web Demo (Streamlit)
```bash
streamlit run demo/app.py
```
Ứng dụng sẽ tự động mở tại địa chỉ `http://localhost:8501`. Bạn có thể:
- Chọn lát cắt ngẫu nhiên hoặc chỉ định từ kho 3.929 ảnh TCGA-LGG.
- Tải lên ảnh MRI tùy ý (JPG, PNG).
- Chuyển đổi giữa 2 thuật toán Watershed và Region Growing.
- Xem chi tiết 8 bước ảnh trung gian của quá trình tách sọ và phân đoạn.
- Đọc bảng thông số định lượng và tải báo cáo chẩn đoán.

### 6.5. Chạy Đánh giá Toàn bộ Tập Dữ liệu (Benchmark CLI)
```bash
python scripts/run_all_experiments.py
```
Script sử dụng kỹ thuật xử lý đa tiến trình (`multiprocessing`), hoàn thành quét và đánh giá toàn bộ 3.929 lát cắt chỉ trong vòng **~20 - 25 giây**, tự động xuất bảng số liệu ra thư mục `docs/BENCHMARK_RESULTS.csv`.

### 6.6. Chạy Bộ Kiểm thử Tự động (Unit Tests)
```bash
pytest -v
```
Kiểm thử toàn diện 16 bài test bao quát các trường hợp biên: ma trận rỗng, mặt nạ hoàn hảo, mặt nạ lệch hoàn toàn, phép tính y sinh phân đoạn và kiểm định bất biến DIP.

---

## 7. Cấu trúc Thư mục Dự án (Repository Structure)

```
brain-tumor-mri-segmentation/
├── configs/                        # Cấu hình tham số hệ thống
│   └── default_params.yaml         # Siêu tham số lọc nhiễu, tách sọ và phân đoạn
├── data/                           # Dữ liệu ảnh MRI
│   ├── README.md                   # Mô tả quy cách cấu trúc ảnh và nhãn
│   └── full/                       # Toàn bộ 3.929 lát cắt chuẩn TCGA-LGG
│       ├── images/                 # Ảnh MRI chuỗi xung FLAIR (256x256, PNG)
│       ├── masks/                  # Mặt nạ Ground Truth (256x256, PNG nhị phân)
│       └── metadata.csv            # Bảng thông tin 110 bệnh nhân và 3.929 lát cắt
├── demo/                           # Giao diện Web tương tác Streamlit
│   ├── app.py                      # Mã nguồn chính giao diện chẩn đoán trực quan
│   └── utils.py                    # Tiện ích nạp ảnh, tạo ảnh trung gian và xuất file
├── docs/                           # Tài liệu kỹ thuật và kết quả thực nghiệm
│   ├── BENCHMARK_RESULTS.csv       # Tổng hợp định lượng theo lát u và não lành
│   ├── BENCHMARK_RESULTS_FULL.csv  # Chi tiết 7.858 kết quả đo đạc từng ảnh
│   ├── DATA_EXPLORATION_REPORT.md  # Báo cáo thống kê phân bố dữ liệu TCGA-LGG
│   └── SPEC_PIPELINE_MRI.md        # Đặc tả toán học và giao diện lập trình
├── notebooks/                      # Jupyter Notebooks thực nghiệm trực quan
│   ├── 01_data_exploration.ipynb   # Thống kê, phân tích phân bố dữ liệu
│   ├── 02_preprocessing_and_skull_stripping.ipynb # Khử nhiễu và tách sọ não 6 bước
│   ├── 03_segmentation_comparison.ipynb # So sánh Watershed vs. Region Growing
│   └── 04_quantitative_evaluation.ipynb # Đánh giá định lượng toàn diện
├── reports/                        # Báo cáo đồ thị và hình ảnh xuất bản
│   └── figures/                    # Biểu đồ phân tích và hình minh họa quy trình
├── scripts/                        # Scripts tự động hóa
│   ├── download_full_dataset.py    # Tải 3.929 ảnh TCGA-LGG từ Hugging Face
│   ├── run_all_experiments.py      # Benchmark đa tiến trình 3.929 lát cắt
│   └── verify_day2_contract.py     # Kiểm chuẩn tự động hợp đồng kỹ thuật DIP
├── src/                            # Mã nguồn module xử lý ảnh số lõi
│   ├── __init__.py
│   ├── pipeline.py                 # Bộ điều phối toàn trình BrainTumorPipeline
│   ├── preprocessing/              # Tiền xử lý & Tách sọ
│   │   ├── filters.py              # Lọc Bilateral và cân bằng CLAHE
│   │   └── skull_strip.py          # Bóc sọ 6 bước dựa trên hình thái học
│   ├── segmentation/               # Giải thuật phân đoạn u
│   │   ├── watershed.py            # Marker-controlled Watershed
│   │   └── region_growing.py       # Seeded Region Growing
│   ├── measurement/                # Đo lường đặc trưng hình học
│   │   └── features.py             # Diện tích, Circularity, Bounding Box
│   └── evaluation/                 # Đo lường chỉ số đánh giá y sinh
│       └── metrics.py              # Dice, IoU, Sensitivity, Specificity
├── tests/                          # Bộ kiểm thử tự động
│   ├── test_metrics.py             # Kiểm thử độ chính xác các hàm đánh giá
│   ├── test_preprocessing.py       # Kiểm thử lọc nhiễu và bóc sọ
│   └── test_segmentation.py        # Kiểm thử giải thuật phân đoạn
├── .gitignore                      # Loại trừ dữ liệu nặng và cache môi trường
├── requirements.txt                # Danh sách thư viện phụ thuộc
└── README.md                       # Tài liệu tổng quan dự án
```

---

## 8. Chi tiết Kỹ thuật Các Module (Technical Methodologies)

### 8.1. Tiền xử lý & Tách sọ Não (Skull Stripping)
- **Bilateral Filter:** Bảo toàn độ sắc nét của đường biên khối u bằng cách kết hợp hàm Gauss theo khoảng cách không gian ($\sigma_{\text{space}} = 75$) và hàm Gauss theo độ chênh lệch cường độ pixel ($\sigma_{\text{color}} = 75$).
- **CLAHE:** Cân bằng biểu đồ mức xám cục bộ với ngưỡng cắt Clip Limit = 2.0 trên các ô lưới 8x8 pixel, làm nổi bật viền tương phản giữa mô u và nhu mô não xung quanh mà không gây khuếch đại nhiễu hạt.
- **Bóc tách sọ não:** Loại bỏ hoàn toàn tín hiệu xương sọ bằng phân ngưỡng Otsu tự động, toán tử mở (Opening) với phần tử cấu trúc hình elip $5 \times 5$, giữ lại thành phần liên thông lớn nhất (LCC) đại diện cho khối nhu mô não, và toán tử đóng (Closing) lấp đầy các rãnh não.

### 8.2. Marker-controlled Watershed Segmentation
- Sử dụng phép biến đổi khoảng cách Euclidean Distance Transform (EDT) trên mặt nạ nhị phân ngưỡng cao của mô u.
- Điểm cực đại khoảng cách cục bộ được gán nhãn làm mầm hạt giống (Markers).
- Thuật toán phân thủy mô phỏng quá trình dâng nước trên bề mặt gradient mức xám, ngăn chặn hiệu quả hiện tượng quá phân đoạn (over-segmentation) thường gặp ở giải thuật Watershed cổ điển.

### 8.3. Seeded Region Growing
- Tự động dò tìm pixel có cường độ sáng cực đại trong nhu mô não đã bóc sọ để làm điểm hạt giống ban đầu $(x_0, y_0)$.
- Lan truyền theo cơ chế hàng đợi (Breadth-First Search - BFS) xét kết nối 8 láng giềng.
- Điều kiện dừng và kết nạp pixel dựa trên ngưỡng chênh lệch cường độ so với hạt giống: $|I(x, y) - I(x_0, y_0)| \le T$, kết hợp loại bỏ các cụm điểm rời rạc bằng lọc diện tích tối thiểu.

---

## 9. Đóng góp & Phát triển (Contributing)

Mọi đóng góp nhằm nâng cao độ chính xác và mở rộng tính năng của dự án đều được hoan nghênh:
1. Fork repository và tạo nhánh mới: `git checkout -b feature/tinh-nang-moi`.
2. Tuân thủ chuẩn lập trình sạch (Clean Code), viết chú thích và docstring đầy đủ.
3. Đảm bảo toàn bộ kiểm thử đơn vị đều vượt qua: `pytest`.
4. Gửi Pull Request mô tả chi tiết các cải tiến kỹ thuật.

---

## 10. Tác giả & Trích dẫn (Authors & Citation)

### Nhóm Tác giả Phát triển:
- **Hà Mạnh Trường** - Pipeline Tiền xử lý & Tách sọ (Skull Stripping), Giải thuật Phân đoạn Lõi u (Watershed & Region Growing).
- **Huỳnh Tâm Trí** - Chuẩn hóa Dữ liệu Y sinh TCGA-LGG, Đo lường Đặc trưng Hình học, Khung Đánh giá Định lượng & Giao diện Streamlit.

### Trích dẫn Nguồn Dữ liệu (Citation):
Nếu bạn sử dụng bộ dữ liệu hoặc mã nguồn của dự án này trong các nghiên cứu khoa học, vui lòng trích dẫn công trình gốc:
```bibtex
@article{buda2019association,
  title={Association of genomic subtypes of lower-grade gliomas with shape features automatically extracted by a deep learning algorithm},
  author={Buda, Mateusz and Saha, Ashirbani and Mazurowski, Maciej A},
  journal={Computers in Biology and Medicine},
  volume={109},
  pages={218--225},
  year={2019},
  publisher={Elsevier}
}
```

---

## 11. Giấy phép Bản quyền (License)

Dự án được phân phối dưới giấy phép **MIT License**. Xem chi tiết tại tệp [LICENSE](LICENSE).
