# KHUNG NỘI DUNG TỔNG QUÁT & QUY TRÌNH THỰC HIỆN ĐỒ ÁN XỬ LÝ ẢNH SỐ
**Trường Đại học Công Thương TP. Hồ Chí Minh (HUIT) — Khoa CNTT — Bộ môn KHDL**  
*(Mô hình chuẩn hóa áp dụng cho mọi đề tài trong danh sách gợi ý và đề tài tự đề xuất 2026–2027)*

---

## 📌 I. Tổng quan & Quy tắc vàng của Học phần

Đồ án kết thúc học phần Xử lý ảnh số chiếm **100% điểm thi cuối kỳ (tương đương 70% tổng điểm học phần)**.

> ⚠️ **Quy tắc vàng của môn Xử lý ảnh số (Tránh bẫy Deep Learning):**
> 1. **Bản chất môn học:** Đồ án phải lấy **kỹ thuật Xử lý ảnh số truyền thống (DIP)** làm nền tảng cốt lõi: tiền xử lý, không gian màu, lọc nhiễu, cân bằng sáng/tương phản, hình thái học (morphology), phân đoạn (segmentation) và trích xuất đặc trưng hình học/màu sắc/kết cấu.
> 2. **Học máy & Học sâu:** Chỉ đóng vai trò hỗ trợ phân loại hoặc so sánh đối chứng. Tuyệt đối không nạp ảnh thô vào mạng Deep Learning (U-Net, YOLO, ResNet...) mà bỏ qua các công đoạn xử lý ảnh số.
> 3. **Thực nghiệm so sánh bắt buộc:** Bắt buộc cài đặt và **so sánh tối thiểu 02 phương án/cấu hình xử lý** (ví dụ: Baseline xử lý ảnh cổ điển vs. Phương án cải tiến).
> 4. **Trọng số điểm:** Phần cài đặt và áp dụng phương pháp xử lý chiếm **50% điểm đồ án**.

---

## 🚀 II. Khung quy trình 7 bước chuẩn mực cho mọi đề tài

Dựa trên phân tích 30 đề tài gợi ý từ Bộ môn, mọi đồ án đều tuân thủ chặt chẽ 7 bước logic:

### 🔹 Bước 1: Thu thập & Chuẩn bị tập dữ liệu (Data Preparation)
* **Quy mô dữ liệu:** Chuẩn bị từ 40–100 ảnh (đối với ảnh tự chụp/thu thập) hoặc 100–500+ ảnh (đối với bộ dữ liệu benchmark công khai).
* **Điều kiện thu nhận:** Đa dạng hóa góc chụp, cường độ sáng, mức độ phức tạp của nền để kiểm tra tính bền vững của thuật toán.
* **Gán nhãn & Ground Truth:** Thiết lập nhãn lớp (class label), bounding box tọa độ hoặc mặt nạ phân đoạn chuẩn (ground-truth binary mask) phục vụ đánh giá định lượng.
* **Tổ chức thư mục:** Phân tách rõ ràng `data/raw/` (ảnh gốc), `data/processed/` (ảnh sau tiền xử lý) và `data/masks/` hoặc `data/labels/`.

### 🔹 Bước 2: Tiền xử lý & Cải thiện chất lượng ảnh (Image Preprocessing & Enhancement)
* **Chuẩn hóa hình học & biểu diễn:** Đọc ảnh qua OpenCV, chuẩn hóa kích thước (resize bảo toàn tỷ lệ), chuẩn hóa khoảng giá trị pixel về $[0, 1]$ hoặc $[0, 255]$.
* **Chuyển đổi không gian màu:** Lựa chọn không gian màu phù hợp: Grayscale (cho ảnh cấu trúc), HSV/HLS (cho phân vùng màu sắc độc lập độ sáng), CIE Lab/YCrCb (cho trích xuất da/vật thể y tế).
* **Khử nhiễu bảo toàn biên:** Áp dụng Gaussian Filter (nhiễu Gauss), Median Filter (nhiễu muối tiêu), hoặc Bilateral Filter (khử nhiễu nhưng giữ sắc nét đường biên đối tượng).
* **Tăng cường độ tương phản:** Khảo sát lược đồ xám (histogram) và áp dụng Gamma Correction, Cân bằng Histogram (HE), hoặc Cân bằng Histogram thích nghi giới hạn độ tương phản (**CLAHE**).
* **Xác định vùng quan tâm (ROI):** Cắt lọc vùng chứa đối tượng chính, loại bỏ phần viền/nhiễu nền không mong muốn.

### 🔹 Bước 3: Phân đoạn & Tách đối tượng cốt lõi (Core Segmentation / ROI Extraction)
* **Nhị phân hóa & Phân ngưỡng:**
  * Phân ngưỡng toàn cục tự động Otsu (*Otsu Thresholding*) hoặc đa ngưỡng (*Multi-Otsu*).
  * Phân ngưỡng thích nghi cục bộ (*Adaptive Thresholding*) khi điều kiện chiếu sáng không đều.
  * Phân ngưỡng theo dải màu sắc (Color Thresholding trên kênh H, S trong HSV hoặc L, a, b).
* **Xử lý hình thái học (Morphological Operations):**
  * Phép mở (*Opening* = Co rồi Giãn) để xóa bỏ các đốm nhiễu nhỏ, chân rết.
  * Phép đóng (*Closing* = Giãn rồi Co) để lấp đầy các lỗ khuyết bên trong đối tượng, nối liền đường nét đứt gãy.
  * Phép toán Top-hat / Black-hat để làm nổi bật chi tiết nhỏ sáng hơn hoặc tối hơn nền xung quanh.
* **Thuật toán phân đoạn nâng cao:** Áp dụng Watershed (kết hợp Distance Transform để tách vật thể dính nhau), Region Growing (phát triển vùng từ hạt giống), Active Contour / GrabCut hoặc K-Means Clustering trên không gian đặc trưng pixel.

### 🔹 Bước 4: Rút trích đặc trưng & Đo lường / Nhận dạng (Feature Extraction & Measurement)
* **Trích xuất đường bao (Contours) & Thành phần liên thông:** Sử dụng `cv2.findContours` hoặc `cv2.connectedComponentsWithStats` để lập chỉ mục từng đối tượng riêng biệt.
* **Đặc trưng hình học & Kích thước:** Tính diện tích (*Area*), chu vi (*Perimeter*), độ tròn (*Circularity* = $4\pi \times \text{Area} / \text{Perimeter}^2$), độ thuôn dài (*Aspect Ratio*), mức độ đặc (*Solidity*), tâm hình học (*Centroid*).
* **Đặc trưng kết cấu (Texture) & Màu sắc:** Vector đặc trưng Color Histogram, Ma trận đồng xuất mức xám GLCM (Haralick features: Contrast, Homogeneity, Energy, Correlation), Local Binary Patterns (*LBP*), hoặc Histogram of Oriented Gradients (*HOG*).
* **Quyết định & Đo lường:** Thiết lập bộ luật ngưỡng (Rule-based), ma trận khoảng cách so khớp, hoặc huấn luyện bộ phân loại cơ bản (KNN, SVM, Random Forest). Tính toán các chỉ số đầu ra: số lượng đếm, vị trí tọa độ, tỷ lệ diện tích bất thường (%).

### 🔹 Bước 5: Xây dựng Baseline & Thực nghiệm so sánh (Comparative Experiments)
* **Phương án 1 (Baseline):** Cấu hình giải pháp xử lý ảnh số cơ sở (ví dụ: Otsu truyền thống + Opening/Closing thông thường).
* **Phương án 2 (Phương án cải tiến / Đối chứng):** Giải pháp nâng cao (ví dụ: Tiền xử lý bằng CLAHE + Lọc Bilateral + Watershed/Region Growing; hoặc trích đặc trưng kết cấu GLCM/LBP kết hợp SVM; hoặc so sánh với mô hình học máy).
* **Khảo sát siêu tham số:** Thực nghiệm thay đổi kích thước kernel lọc ($3 \times 3$, $5 \times 5$, $7 \times 7$), tham số clip limit của CLAHE, ngưỡng nhị phân để tìm ra cấu hình tối ưu.

### 🔹 Bước 6: Đánh giá định lượng & Phân tích trường hợp thất bại (Evaluation & Error Analysis)
* **Bộ chỉ số đánh giá theo từng dạng bài toán:**
  * *Bài toán phân đoạn (Segmentation):* Chỉ số tương đồng Dice (*Dice Similarity Coefficient / F1*), chỉ số Jaccard (*IoU*), Độ nhạy (*Sensitivity/Recall*), Độ đặc hiệu (*Specificity*).
  * *Bài toán đếm & đo lường:* Sai số tuyệt đối trung bình (*MAE*), Sai số tương đối (*Mean Percentage Error*).
  * *Bài toán phân loại/nhận dạng:* Độ chính xác (*Accuracy*), Ma trận nhầm lẫn (*Confusion Matrix*), F1-score.
  * *Bài toán nâng cao chất lượng ảnh:* *PSNR* (dB), *SSIM* (0 đến 1), *Entropy* thông tin.
  * *Hiệu năng tính toán:* Thời gian xử lý trung bình mỗi khung hình/ảnh (ms hoặc FPS).
* **Phân tích định tính trực quan:** Trình bày bảng so sánh song song: [Ảnh gốc] $\rightarrow$ [Ảnh sau tiền xử lý] $\rightarrow$ [Mặt nạ phân đoạn / Bounding Box] $\rightarrow$ [Ảnh Ground Truth].
* **Phân tích trường hợp thất bại (Failure Cases):** Nhận diện và giải thích nguyên nhân thuật toán bị lỗi (độ tương phản quá thấp, biên mờ, vật thể bị che khuất, nhiễu nền quá mạnh).

### 🔹 Bước 7: Xây dựng chương trình minh họa & Đóng gói (Demo & Packaging)
* **Giao diện tương tác (GUI):** Xây dựng giao diện demo hoàn chỉnh bằng *Streamlit*, *Gradio*, hoặc *OpenCV GUI/Tkinter*.
* **Chức năng giao diện:** Cho phép người dùng tải ảnh từ máy tính (hoặc webcam), chọn cấu hình/thuật toán xử lý, điều chỉnh thanh trượt tham số (threshold, kernel size), xem các ảnh kết quả trung gian và lưu ảnh kết quả kèm báo cáo chỉ số ra file.
* **Tính tái lập (Reproducibility):** Đóng gói mã nguồn sạch, có file cấu hình môi trường (`requirements.txt`), hướng dẫn cài đặt và chạy thử rõ ràng trong `README.md`.

---

## 📊 III. Bảng ánh xạ kỹ thuật cho 5 nhóm đề tài lớn

| Nhóm Đề Tài | Tiền Xử Lý & Nâng Cao | Thuật Toán Phân Đoạn / Xử Lý Lõi | Chỉ Số Đánh Giá |
| :--- | :--- | :--- | :--- |
| **1. Cải thiện & Nâng cao ảnh**<br>*(Đề tài 1, 2, 3, 4, 5, 28)* | Cân bằng sáng, Gamma, CLAHE, Homomorphic filter, Lọc FFT 2D | Phân tích tần số, Biến đổi Fourier/DCT, Notch filter khử sọc | PSNR, SSIM, Entropy, Tương phản (Contrast), Thời gian xử lý |
| **2. Nhị phân hóa & Quét tài liệu**<br>*(Đề tài 6, 14, 20, 21, 22)* | Grayscale, Khử bóng mờ, Lọc trung vị, Perspective transform | Otsu, Adaptive thresholding, Morphology nối nét, Tìm biên tài liệu | Tỷ lệ pixel nền/chữ, Độ tương phản ký tự, Tỷ lệ nhận diện góc |
| **3. Đếm & Đo lường vật thể**<br>*(Đề tài 7, 8, 9, 12, 13, 16, 17)* | Lọc Gaussian/Median, Tách nền, Chuẩn hóa kích thước | Thresholding + Distance Transform + Watershed, Connected components | Độ chính xác số lượng đếm (Accuracy), Sai số MAE, Tỷ lệ Pass/Fail |
| **4. Phân đoạn tổn thương/bệnh**<br>*(Đề tài 10, 23, 27 và **Ảnh y tế**)* | Cân bằng CLAHE, Lọc Bilateral giữ biên, Chuyển đổi HSV/Lab, Khử nhiễu nền | Phân đoạn Otsu/Multi-Otsu, Watershed, Region Growing, Phân cụm K-Means pixel, Lọc diện tích | **Dice Score**, **IoU**, Sensitivity, Specificity, Tỷ lệ % diện tích tổn thương |
| **5. So khớp & Phân loại cổ điển**<br>*(Đề tài 15, 18, 19, 24, 25, 26, 29, 30)* | Canny edge detection, Cắt vùng ROI hình thang, Chuẩn hóa vector | Hough Transform (Line/Circle), Trích đặc trưng SIFT/ORB, HOG/LBP + KNN/SVM | Top-1/Top-K Accuracy, Precision, Recall, F1, Confusion Matrix |

---

## 🏥 IV. Ánh xạ chi tiết vào đề tài: "Phân đoạn và phát hiện tổn thương trên ảnh y tế"

| Hạng mục | Triển khai kỹ thuật cụ thể |
| :--- | :--- |
| **Tập Dữ Liệu** | Sử dụng bộ dữ liệu y tế chuẩn có ground-truth mask: ISIC 2018 (tổn thương ung thư da), COVID-QU-Ex (tổn thương viêm phổi trên X-quang), hoặc Figshare MRI (khối u não). Gồm ảnh gốc và mask nhị phân tổn thương do chuyên gia y tế đánh dấu. |
| **Tiền Xử Lý** | 1. Chuẩn hóa kích thước $512 \times 512$, chuẩn hóa dải pixel.<br>2. Áp dụng **Bilateral Filter** để lọc nhiễu hạt y tế nhưng bảo toàn sắc nét ranh giới mô bệnh và mô lành.<br>3. Áp dụng **CLAHE** để làm nổi bật các tổn thương có độ tương phản thấp.<br>4. (Với ảnh da liễu) Áp dụng biến đổi Black-hat và Inpainting để xóa các vết lông/tóc che khuất. |
| **Phân Đoạn Lõi (Baseline)** | - Chuyển sang không gian màu thích hợp (kênh L trong Lab hoặc ảnh xám CLAHE).<br>- Nhị phân hóa bằng **Multi-Otsu** hoặc **Adaptive Thresholding**.<br>- Hậu xử lý bằng **Morphological Opening** (kernel $5 \times 5$) để loại bỏ đốm nhiễu, tiếp theo là **Morphological Closing** để lấp đầy vùng lõi tổn thương.<br>- Áp dụng **Distance Transform + Watershed** để tách các cụm tổn thương nằm sát nhau. |
| **Phương Án Cải Tiến** | - **Phương án so sánh:** Sử dụng ảnh đã qua tiền xử lý DIP đưa vào thuật toán phân cụm **K-Means Clustering** trên không gian màu kết hợp đặc trưng kết cấu GLCM/LBP; hoặc mô hình phân đoạn mạng nơ-ron **U-Net** được huấn luyện trên ảnh đã tăng cường chất lượng. |
| **Phát Hiện & Đo Lường** | - Rút trích Contours, lọc bỏ các vùng nhỏ ($\text{Area} < \text{min\_thresh}$).<br>- Vẽ **Bounding Box** (hình chữ nhật bao quanh) và **Convex Hull** bao quanh từng ổ tổn thương.<br>- Tính toán diện tích pixel tổn thương ($S_{\text{lesion}}$) và tỷ lệ phần trăm tổn thương so với toàn bộ cơ quan: $P = (S_{\text{lesion}} / S_{\text{organ}}) \times 100\%$. |
| **Đánh Giá Định Lượng** | So sánh mặt nạ dự đoán ($P$) với mặt nạ chuyên gia ($G$) qua các chỉ số:<br>- $\text{Dice} = \frac{2 |P \cap G|}{|P| + |G|}$ và $\text{IoU} = \frac{|P \cap G|}{|P \cup G|}$<br>- $\text{Sensitivity} = \frac{\text{TP}}{\text{TP} + \text{FN}}$ (tỷ lệ phát hiện đúng vùng bệnh, cực kỳ quan trọng trong y tế)<br>- Đo thời gian xử lý trung bình trên mỗi ca chụp. |
| **Chương Trình Demo** | Giao diện web Streamlit: Bác sĩ/Người dùng nạp ảnh y tế $\rightarrow$ Chọn phương pháp (Baseline DIP vs Cải tiến) $\rightarrow$ Hiển thị trực quan: Ảnh gốc, Ảnh CLAHE, Mặt nạ tổn thương, Bounding Box màu cảnh báo, Bảng chỉ số Dice/IoU và diện tích tổn thương. |

---

## 📑 V. Cấu trúc Báo cáo đồ án chuẩn 10 mục (Khoa CNTT - HUIT)

1. **Trang bìa:** Tên trường, khoa, bộ môn, tên đề tài, thông tin giảng viên hướng dẫn, danh sách thành viên nhóm (kèm tỷ lệ phần trăm % đóng góp).
2. **Mục lục:** Mục lục tự động, danh mục bảng biểu, danh mục hình ảnh, danh mục từ viết tắt.
3. **Mục 1: Giới thiệu đề tài:** Bối cảnh thực tế, tầm quan trọng của bài toán, mục tiêu cụ thể (đầu vào, đầu ra mong đợi), phạm vi và giới hạn của đề tài.
4. **Mục 2: Cơ sở lý thuyết:** Trình bày nguyên lý toán học và cơ chế hoạt động của các thuật toán sử dụng (bộ lọc, biến đổi hình thái, CLAHE, Otsu, Watershed, độ đo Dice/IoU). Có hình vẽ minh họa thuật toán.
5. **Mục 3: Mô tả tập dữ liệu:** Nguồn gốc bộ dữ liệu, số lượng ảnh, độ phân giải, phân bố các lớp, điều kiện thu nhận và phương pháp gán nhãn ground truth.
6. **Mục 4: Tiền xử lý ảnh:** Mô tả chi tiết từng bước tiền xử lý, bảng tham số đã chọn, hình ảnh minh họa so sánh trước và sau khi tiền xử lý.
7. **Mục 5: Phương pháp và quy trình thực nghiệm:** Sơ đồ khối pipeline hoàn chỉnh từ ảnh đầu vào đến kết quả cuối cùng. Mô tả chi tiết thuật toán Baseline và phương án cải tiến/so sánh.
8. **Mục 6: Kết quả và đánh giá:** Trình bày bảng số liệu định lượng (Dice, IoU, Accuracy, thời gian...), biểu đồ so sánh giữa các phương án; minh họa các ca nhận dạng tốt và các ca thất bại (kèm phân tích nguyên nhân).
9. **Mục 7: Chương trình minh họa (Demo):** Mô tả cấu trúc mã nguồn, hướng dẫn cài đặt và sử dụng, hình chụp giao diện hoạt động thực tế trên các ca thử nghiệm khác nhau.
10. **Mục 8: Kết luận và hướng phát triển:** Tóm tắt những kết quả đã đạt được, tự đánh giá ưu điểm và hạn chế của hệ thống, đề xuất các hướng mở rộng trong tương lai.
11. **Tài liệu tham khảo:** Trích dẫn chuẩn học thuật (IEEE hoặc APA) các bài báo khoa học, giáo trình môn học và tài liệu OpenCV/thư viện liên quan.

---

## 🏆 VI. Trọng số đánh giá đồ án (Rubric Bộ môn KHDL)

| Tiêu Chí Đánh Giá | Trọng Số | Yêu Cầu Cốt Lõi Cần Đạt |
| :--- | :---: | :--- |
| **Cài đặt & Áp dụng phương pháp xử lý** | **50%** | Xây dựng pipeline chạy ổn định; áp dụng đúng và sáng tạo các kỹ thuật xử lý ảnh; có kết quả thực nghiệm trực quan và bảng số liệu định lượng rõ ràng. |
| **Phân tích & Lựa chọn phương pháp** | **15%** | Giải thích rõ lý do lựa chọn thuật toán; so sánh tối thiểu 2 phương án/cấu hình; hiểu sâu bản chất tham số và ưu nhược điểm của từng phương pháp. |
| **Trình bày báo cáo khoa học** | **15%** | Báo cáo đúng cấu trúc 10 mục; hình vẽ, bảng biểu chuẩn mực có chú thích rõ ràng; không mắc lỗi chính tả; văn phong mạch lạc, khách quan. |
| **Tự học & Nghiên cứu mở rộng** | **10%** | Khả năng tự tìm hiểu tài liệu chuyên ngành, thư viện OpenCV, bộ dữ liệu thực tế và giải quyết các vấn đề kỹ thuật phát sinh. |
| **Phân công & Phối hợp làm việc nhóm** | **10%** | Phân chia công việc công bằng, minh bạch; mỗi thành viên nắm vững phần việc của mình và hiểu toàn bộ quy trình chung của nhóm. |
