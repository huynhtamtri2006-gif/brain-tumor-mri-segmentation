# Phân Đoạn & Phát Hiện Tổn Thương Trên Ảnh Y Tế
### Medical Image Lesion Segmentation and Detection

> **Đồ án kết thúc học phần:** Xử lý ảnh số (Digital Image Processing)  
> **Đơn vị:** Bộ môn Khoa học Dữ liệu — Khoa Công nghệ Thông tin — Trường Đại học Công Thương TP. Hồ Chí Minh (HUIT)  
> **Năm học:** 2026–2027  

---

## 👥 Thành viên nhóm thực hiện

| STT | Họ và Tên | Mã số sinh viên (MSSV) | Vai trò / Phân công chính |
| :---: | :--- | :---: | :--- |
| 1 | **Hà Mạnh Trường** | **2045240326** | Trưởng nhóm, Thiết kế pipeline tiền xử lý DIP, Thuật toán phân đoạn lõi (Otsu/Watershed), Báo cáo khoa học |
| 2 | **Huỳnh Tâm Trí** | **2045240315** | Chuẩn bị dữ liệu & gán nhãn, Rút trích đặc trưng hình học/kết cấu, Đánh giá định lượng (Dice/IoU), Xây dựng ứng dụng Demo |

---

## 🎯 1. Mục tiêu và Phạm vi Đề tài

* **Bối cảnh:** Ảnh y tế (da liễu, X-quang, CT/MRI) thường có độ tương phản thấp, ranh giới tổn thương mờ và có nhiều nhiễu do thiết bị thu nhận. Việc tự động phát hiện và phân đoạn tổn thương giúp hỗ trợ các bác sĩ chẩn đoán nhanh, khách quan và chính xác hơn.
* **Mục tiêu đầu vào:** Ảnh y tế kỹ thuật số chứa vùng nghi ngờ tổn thương (định dạng JPG, PNG, DICOM).
* **Mục tiêu đầu ra:**
  1. Mặt nạ phân đoạn tổn thương (Binary Segmentation Mask).
  2. Bounding Box và đường bao (Contour / Convex Hull) khoanh vùng chính xác ổ bệnh.
  3. Báo cáo định lượng: Diện tích tổn thương ($S_{\text{lesion}}$), tỷ lệ tổn thương so với vùng cơ quan ($P\%$), chỉ số độ tương đồng **Dice Score, IoU, Sensitivity, Specificity**.
* **Nguyên tắc kỹ thuật cốt lõi:** Lấy kỹ thuật **Xử lý ảnh số cổ điển (Digital Image Processing - DIP)** làm trọng tâm thực nghiệm, so sánh tối thiểu 2 phương án xử lý theo đúng yêu cầu học phần của Bộ môn.

---

## 🔬 2. Sơ đồ Pipeline Xử lý 7 Bước

```
[Ảnh Y Tế Đầu Vào]
        │
        ▼
1. 【Tiền xử lý & Cải thiện chất lượng ảnh】
   ├── Chuẩn hóa kích thước (512x512) & dải pixel [0, 1]
   ├── Lọc nhiễu bảo toàn đường biên: Bilateral Filter / Median Filter
   ├── Nâng cao tương phản cục bộ: CLAHE (Contrast Limited Adaptive Histogram Equalization)
   └── (Ảnh da liễu) Tẩy lông/vết mờ bằng Black-hat transform + Inpainting
        │
        ▼
2. 【Phân đoạn tổn thương (Segmentation) — Thực nghiệm đối chứng】
   ├── Phương án A (Baseline DIP): Multi-Otsu / Adaptive Thresholding ➔ Morphological Opening/Closing ➔ Distance Transform + Watershed
   └── Phương án B (Advanced/Comparison): Phân cụm K-Means pixel trên không gian Lab + Texture GLCM/LBP HOẶC U-Net segmentation
        │
        ▼
3. 【Phát hiện & Định vị ổ tổn thương】
   ├── Connected Components Analysis & Trích xuất Contours
   ├── Lọc nhiễu theo diện tích tối thiểu (Area thresholding)
   └── Vẽ Bounding Box & Convex Hull bao quanh tổn thương
        │
        ▼
4. 【Đo lường & Đánh giá định lượng】
   ├── Tính toán diện tích tổn thương và tỷ lệ % tổn thương / cơ quan
   ├── Đo đạc so sánh với Ground Truth: Dice Coefficient (F1), IoU (Jaccard), Sensitivity (Recall), Specificity
   └── Đo thời gian xử lý trung bình mỗi ca chụp (ms)
        │
        ▼
5. 【Chương trình ứng dụng Demo (GUI)】
   └── Giao diện web Streamlit cho phép bác sĩ nạp ảnh, xem ảnh trung gian, chọn phương pháp và xuất báo cáo
```

---

## 📂 3. Cấu trúc thư mục dự án

```
medical-image-lesion-segmentation/
├── .agents/                        # Bộ kỹ năng AI Agent hỗ trợ phát triển (Matt Pocock Skills)
├── docs/                           # Tài liệu đề cương, danh mục đề tài và hướng dẫn học phần
│   ├── 7. DANH_SACH_DE_TAI...pdf   # Danh mục đề tài gợi ý của Bộ môn
│   ├── 9. Ke_hoach_thuc_ĐA...pdf   # Kế hoạch thực hiện 15 tuần của Bộ môn
│   ├── KHUNG_NOI_DUNG_TONG_QUAT... # Khung nội dung chuẩn hóa cho mọi đề tài (PDF + MD)
│   └── agents/                     # Cấu hình issue tracker, triage labels, domain docs
├── data/                           # Dữ liệu ảnh y tế (tạo khi thực nghiệm)
│   ├── raw/                        # Ảnh y tế gốc
│   ├── processed/                  # Ảnh sau tiền xử lý (CLAHE, Bilateral)
│   └── masks/                      # Mặt nạ ground truth chuyên gia
├── src/                            # Mã nguồn chính của pipeline xử lý ảnh số
│   ├── preprocessing/              # Các mô-đun lọc nhiễu, CLAHE, cân bằng sáng
│   ├── segmentation/               # Các giải pháp phân đoạn (Otsu, Watershed, K-Means)
│   ├── measurement/                # Đo lường diện tích, bounding box, tính toán chỉ số
│   └── evaluation/                 # Tính Dice, IoU, Sensitivity, Confusion Matrix
├── demo/                           # Mã nguồn ứng dụng giao diện minh họa (Streamlit GUI)
├── scripts/                        # Các script tự động hóa tài liệu và thử nghiệm
├── AGENTS.md                       # Quy chuẩn kỹ thuật toàn cục và thông tin nhóm
├── requirements.txt                # Danh sách thư viện phụ thuộc (OpenCV, NumPy, Streamlit...)
└── README.md                       # Tài liệu giới thiệu dự án
```

---

## 🛠️ 4. Cài đặt và Chạy thử nghiệm

### Yêu cầu môi trường
* Python 3.10+
* OpenCV (`opencv-python >= 4.8.0`)
* NumPy, SciPy, Scikit-image, Scikit-learn, Matplotlib
* Streamlit (cho giao diện Demo)

### Cài đặt
```bash
# Clone repository
git clone https://github.com/mtzwyu/medical-image-lesion-segmentation.git
cd medical-image-lesion-segmentation

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

---

## 📋 5. Kế hoạch nộp sản phẩm theo quy định Khoa CNTT

* **Báo cáo đồ án:** Soạn thảo theo chuẩn 10 mục của Khoa CNTT (Word và PDF).
* **Mã nguồn:** Toàn bộ pipeline xử lý ảnh số sạch, có chú thích chi tiết, kèm demo tương tác.
* **Tập dữ liệu:** Bộ dữ liệu kiểm thử kèm ground truth mask.
* **Slide thuyết trình:** Tóm tắt bối cảnh, phương pháp, kết quả định lượng và kết luận.
