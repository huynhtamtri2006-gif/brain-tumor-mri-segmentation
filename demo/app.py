"""Ứng dụng Web Demo Streamlit: Phân đoạn và phát hiện khối u não trên ảnh MRI.

Học phần: Xử lý ảnh số (2026-2027) - Bộ môn Khoa học Dữ liệu - Khoa CNTT - HUIT.
Nhóm sinh viên: Hà Mạnh Trường (2045240326) & Huỳnh Tâm Trí (2045240315).
"""

import os
import sys
import numpy as np
import cv2
import streamlit as st

# Thêm đường dẫn gốc vào sys.path để import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline import BrainTumorPipeline
from demo.utils import list_sample_cases, load_image_and_mask

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Phân Đoạn U Não MRI — HUIT DIP Project",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện y khoa hiện đại
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.05rem; color: #4B5563; margin-bottom: 1.5rem; }
    .metric-card { background-color: #F3F4F6; border-radius: 8px; padding: 12px; border-left: 4px solid #3B82F6; }
</style>
""", unsafe_allow_html=True)

# 1. SIDEBAR
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Logo_HUIT.png/220px-Logo_HUIT.png", width=120)
    st.title("⚙️ Cấu Hình Hệ Thống")
    st.markdown("**Đồ án Xử lý ảnh số (2026–2027)**")
    st.markdown("👨‍🎓 **Hà Mạnh Trường** - `2045240326`  \n👨‍🎓 **Huỳnh Tâm Trí** - `2045240315`")
    st.divider()

    st.subheader("1. Nạp Dữ Liệu Ảnh MRI")
    data_options = [
        "Chọn từ kho 3,929 lát cắt chuẩn TCGA-LGG (data/full)",
        "Tải ảnh từ máy tính (.png, .jpg)"
    ]
    data_mode = st.radio("Nguồn ảnh đầu vào:", data_options)

    input_img = None
    input_gt_mask = None

    if "3,929" in data_mode:
        full_files = list_sample_cases("data/full/images")
        if full_files:
            # Cho phép tìm kiếm/lọc nhanh
            search_patient = st.text_input("Lọc theo mã bệnh nhân (ví dụ: TCGA_CS_4941):", "")
            if search_patient:
                filtered_files = [f for f in full_files if search_patient.upper() in f.upper()]
            else:
                filtered_files = full_files[:100] # hiển thị 100 lát đầu để mượt giao diện
            
            selected_file = st.selectbox(f"Chọn lát cắt MRI ({len(filtered_files)}/{len(full_files)} khả dụng):", filtered_files)
            if selected_file:
                sample_id = selected_file.replace(".png", "")
                input_img, input_gt_mask = load_image_and_mask(sample_id, base_dir="data/full")
        else:
            st.warning("Chưa có ảnh trong data/full/images")

    else:
        uploaded_file = st.file_uploader("Tải lên ảnh MRI xám:", type=["png", "jpg", "jpeg", "tif"])
        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            input_img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

    st.divider()
    st.subheader("2. Thuật Toán Phân Đoạn (DIP)")
    method_option = st.selectbox(
        "Lựa chọn phương pháp:",
        ["Phương án A: Marker-controlled Watershed (Baseline)", "Phương án B: Seeded Region Growing (Đối chứng)"]
    )
    method_key = "watershed" if "Watershed" in method_option else "region_growing"

    with st.expander("Tùy chỉnh siêu tham số"):
        if method_key == "watershed":
            dist_ratio = st.slider("Ngưỡng khoảng cách cực đại (Dist Ratio):", 0.1, 0.9, 0.4, 0.05)
            pipeline_params = {"dist_thresh_ratio": dist_ratio}
        else:
            tol = st.slider("Dung sai độ sáng (Intensity Tolerance):", 5, 40, 15, 1)
            pipeline_params = {"intensity_tolerance": tol}

# 2. KHU VỰC HIỂN THỊ CHÍNH (MAIN AREA)
st.markdown('<div class="main-header">🧠 HỆ THỐNG PHÂN ĐOẠN & PHÁT HIỆN KHỐI U NÃO MRI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Trường ĐH Công Thương TP.HCM — Bộ môn Khoa học Dữ liệu — Học phần Xử lý ảnh số</div>', unsafe_allow_html=True)

if input_img is None:
    st.info("👈 Vui lòng chọn hoặc tải ảnh MRI ở thanh điều khiển bên trái để bắt đầu phân đoạn.")
else:
    # Nút thực thi chẩn đoán
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        run_button = st.button("🚀 TIẾN HÀNH PHÂN ĐOẠN", type="primary", use_container_width=True)

    if run_button or True: # Tự động chạy khi có ảnh
        pipeline = BrainTumorPipeline(method=method_key, params=pipeline_params)
        diag_res, inters = pipeline.process(input_img, gt_mask=input_gt_mask)

        # Hàng 1: Thẻ chỉ số chẩn đoán (Dashboard KPI Cards)
        st.subheader("📊 Kết Quả Chẩn Đoán & Định Lượng")
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        with kpi1:
            st.metric("Phát hiện khối u", "CÓ U" if diag_res.tumor_detected else "BÌNH THƯỜNG",
                      delta="Cảnh báo" if diag_res.tumor_detected else None, delta_color="inverse")
        with kpi2:
            st.metric("Diện tích khối u", f"{diag_res.tumor_area_px:,} px")
        with kpi3:
            st.metric("Tỷ lệ % u / não", f"{diag_res.tumor_ratio_percent:.2f} %")
        with kpi4:
            st.metric("Độ tròn (Circularity)", f"{diag_res.circularity:.3f}")
        with kpi5:
            if diag_res.dice_score is not None:
                st.metric("Chỉ số Dice (F1)", f"{diag_res.dice_score:.4f}", help="So với Ground Truth chuyên gia")
            else:
                st.metric("Chỉ số Dice", "N/A (Ảnh tự do)")

        st.divider()

        # Hàng 2: Trực quan hóa 4 bước trung gian DIP
        st.subheader("🔬 Trực Quan Hóa Quy Trình Xử Lý Ảnh Số (DIP Steps)")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.caption("1. Ảnh MRI Sọ Não Gốc")
            st.image(inters["original"], use_container_width=True, clamp=True)
        with c2:
            st.caption("2. Tách Sọ (Skull Stripped)")
            st.image(inters["stripped"], use_container_width=True, clamp=True)
        with c3:
            st.caption(f"3. Mặt Nạ U ({method_key.title()})")
            st.image(inters["tumor_mask"], use_container_width=True, clamp=True)
        with c4:
            st.caption("4. Định Vị (Bounding Box Đỏ)")
            st.image(inters["overlay"], use_container_width=True, channels="BGR")

        # So sánh Ground Truth nếu có
        if input_gt_mask is not None:
            with st.expander("🔍 So sánh trực tiếp Mặt nạ Dự đoán với Ground Truth Bác sĩ"):
                gt_c1, gt_c2 = st.columns(2)
                with gt_c1:
                    st.caption("Mặt Nạ Ground Truth Chuyên Gia")
                    st.image(input_gt_mask, use_container_width=True)
                with gt_c2:
                    st.caption("Mặt Nạ Dự Đoán Của Thuật Toán")
                    st.image(inters["tumor_mask"], use_container_width=True)
