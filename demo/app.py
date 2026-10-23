"""Web demo Streamlit chẩn đoán u não MRI - Giao diện NeuroScan PACS Workstation.
Khoa Công nghệ Thông tin - Bộ môn Khoa học Dữ liệu - Đại học Công Thương TP.HCM (HUIT).
Giao diện chuẩn hóa y tế tiếng Việt đầy đủ, hỗ trợ chuyển đổi giữa Chế độ Sáng (mặc định) và Chế độ Tối.
"""

from __future__ import annotations

import csv
import io
import os
import sys
import time

import cv2
import numpy as np
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from demo.utils import (
    PRESET_CASES,
    generate_error_map,
    list_sample_cases,
    load_image_and_mask,
)
from src.pipeline import BrainTumorPipeline


# =============================================================================
# 1. CẤU HÌNH TRANG VÀ QUẢN LÝ CHẾ ĐỘ GIAO DIỆN (THEME)
# =============================================================================

st.set_page_config(
    page_title="NeuroScan Pro - Phân Đoạn U Não MRI | HUIT",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Nhận diện chế độ giao diện từ session_state (mặc định Sáng theo yêu cầu)
if "theme_mode_selector" not in st.session_state:
    st.session_state["theme_mode_selector"] = "Chế độ Sáng (Clinical Light)"

is_light = "Sáng" in st.session_state["theme_mode_selector"]

# Khởi tạo bảng biến CSS thích ứng cho 2 chế độ Sáng và Tối
if is_light:
    theme_vars = """
        --bg-main: #f8fafc;
        --bg-card: #ffffff;
        --bg-card-hover: #f1f5f9;
        --bg-sidebar: #f8fafc;
        --border-color: #e2e8f0;
        --border-subtle: #cbd5e1;
        --text-primary: #0f172a;
        --text-secondary: #334155;
        --text-muted: #64748b;
        --accent-blue: #0284c7;
        --accent-cyan: #0891b2;
        --accent-green: #059669;
        --accent-red: #dc2626;
        --accent-amber: #d97706;
        --pacs-header-bg: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
        --pacs-header-border: #bae6fd;
        --pacs-header-shadow: 0 4px 20px -2px rgba(14, 165, 233, 0.12), 0 2px 6px -1px rgba(0, 0, 0, 0.05);
        --pacs-title-color: #0f172a;
        --pacs-pill-bg: #e0f2fe;
        --pacs-pill-border: #bae6fd;
        --pacs-pill-text: #0369a1;
        --pacs-pill-bold: #0284c7;
        --stat-box-bg: #f8fafc;
        --stat-box-border: #e2e8f0;
        --stat-box-text: #1e293b;
        --input-bg: #ffffff;
        --input-border: #cbd5e1;
        --input-text: #0f172a;
    """
else:
    theme_vars = """
        --bg-main: #0b0f19;
        --bg-card: #111827;
        --bg-card-hover: #1e293b;
        --bg-sidebar: #0d1322;
        --border-color: #1f293d;
        --border-subtle: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-blue: #0284c7;
        --accent-cyan: #06b6d4;
        --accent-green: #10b981;
        --accent-red: #ef4444;
        --accent-amber: #f59e0b;
        --pacs-header-bg: linear-gradient(135deg, rgba(17, 24, 39, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        --pacs-header-border: #1e293b;
        --pacs-header-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(14, 165, 233, 0.08);
        --pacs-title-color: #ffffff;
        --pacs-pill-bg: rgba(30, 41, 59, 0.7);
        --pacs-pill-border: #334155;
        --pacs-pill-text: #cbd5e1;
        --pacs-pill-bold: #38bdf8;
        --stat-box-bg: #111827;
        --stat-box-border: #1e293b;
        --stat-box-text: #cbd5e1;
        --input-bg: #111827;
        --input-border: #1f293d;
        --input-text: #f8fafc;
    """

st.markdown(
    f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

      :root {{
        {theme_vars}
      }}

      html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      }}

      .stApp {{
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
      }}

      .block-container {{
        max-width: 1520px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
      }}

      /* Sidebar Styling */
      [data-testid="stSidebar"] {{
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-color) !important;
      }}
      [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
      [data-testid="stSidebar"] span,
      [data-testid="stSidebar"] label {{
        color: var(--text-primary) !important;
      }}
      [data-testid="stSidebar"] .stCaption,
      [data-testid="stSidebar"] small {{
        color: var(--text-muted) !important;
      }}

      /* Radio Buttons & Labels */
      [data-testid="stRadio"] label {{
        color: var(--text-primary) !important;
      }}
      [data-testid="stRadio"] div[role="radiogroup"] span {{
        color: var(--text-primary) !important;
      }}

      /* Inputs & Dropdowns */
      [data-testid="stTextInput"] input {{
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 8px !important;
      }}
      [data-testid="stSelectbox"] > div > div {{
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 8px !important;
      }}
      [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {{
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
      }}
      [data-baseweb="menu"] li {{
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
      }}
      [data-baseweb="menu"] li:hover {{
        background-color: var(--bg-card-hover) !important;
      }}

      /* Expander */
      [data-testid="stExpander"] {{
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
      }}
      [data-testid="stExpander"] summary {{
        color: var(--text-primary) !important;
      }}
      [data-testid="stExpander"] details {{
        background-color: var(--bg-card) !important;
        border-color: var(--border-color) !important;
      }}

      /* Secondary Buttons (như các Preset) */
      div[data-testid="stButton"] button[kind="secondary"] {{
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
      }}
      div[data-testid="stButton"] button[kind="secondary"]:hover {{
        border-color: #0284c7 !important;
        color: #0284c7 !important;
      }}

      /* Top Header Hub */
      .pacs-header {{
        background: var(--pacs-header-bg);
        border: 1px solid var(--pacs-header-border);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--pacs-header-shadow);
      }}
      .pacs-badge {{
        display: inline-flex;
        align-items: center;
        background: rgba(14, 165, 233, 0.12);
        color: #0284c7;
        border: 1px solid rgba(14, 165, 233, 0.28);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
      }}
      .pacs-title {{
        color: var(--pacs-title-color);
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
      }}
      .pacs-subtitle {{
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin-top: 0.4rem;
        margin-bottom: 0;
      }}
      .pacs-status-bar {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 1rem;
        padding-top: 0.8rem;
        border-top: 1px solid var(--border-color);
      }}
      .pacs-pill {{
        background: var(--pacs-pill-bg);
        border: 1px solid var(--pacs-pill-border);
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.78rem;
        color: var(--pacs-pill-text);
        font-family: 'JetBrains Mono', monospace;
      }}
      .pacs-pill b {{
        color: var(--pacs-pill-bold);
      }}

      /* Header Sections & Titles */
      .section-heading {{
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.8rem;
      }}
      .preset-bar-title {{
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
      }}

      /* KPI Cards */
      .kpi-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 14px;
        margin-bottom: 1.5rem;
      }}
      .kpi-card {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 1.1rem 1.25rem;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
      }}
      .kpi-card:hover {{
        transform: translateY(-2px);
        border-color: #0284c7;
        box-shadow: 0 6px 16px rgba(14, 165, 233, 0.15);
      }}
      .kpi-card.alert-danger {{
        border-left: 4px solid var(--accent-red);
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, var(--bg-card) 100%);
      }}
      .kpi-card.alert-success {{
        border-left: 4px solid var(--accent-green);
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, var(--bg-card) 100%);
      }}
      .kpi-card.card-blue {{
        border-left: 4px solid #0ea5e9;
      }}
      .kpi-card.card-amber {{
        border-left: 4px solid #f59e0b;
      }}
      .kpi-card.card-purple {{
        border-left: 4px solid #8b5cf6;
      }}
      .kpi-label {{
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-muted);
        margin-bottom: 0.4rem;
      }}
      .kpi-val {{
        font-size: 1.65rem;
        font-weight: 750;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.2;
      }}
      .kpi-sub {{
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-top: 0.35rem;
      }}

      /* Frame ảnh chuyên dụng */
      .img-card {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
      }}
      .img-card-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid var(--border-color);
      }}
      .img-card-title {{
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--text-primary);
      }}
      .img-card-tag {{
        font-size: 0.7rem;
        padding: 2px 7px;
        border-radius: 4px;
        background: var(--stat-box-bg);
        color: var(--text-secondary);
        border: 1px solid var(--border-color);
        font-family: 'JetBrains Mono', monospace;
      }}

      /* Hộp thông số thống kê đối chứng */
      .stat-box {{
        background: var(--stat-box-bg);
        border: 1px solid var(--stat-box-border);
        border-radius: 8px;
        padding: 0.85rem;
        margin-top: 0.5rem;
        font-size: 0.85rem;
        color: var(--stat-box-text);
        line-height: 1.6;
      }}

      /* Hộp phân tích bản đồ sai số */
      .error-breakdown-box {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
      }}

      /* Tùy chỉnh Tabs */
      div[data-testid="stTabs"] button {{
        font-size: 0.92rem;
        font-weight: 600;
        color: var(--text-secondary);
        padding: 0.6rem 1.2rem;
      }}
      div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: #0284c7 !important;
        border-bottom-color: #0284c7 !important;
      }}

      /* Download Button */
      div[data-testid="stDownloadButton"] button {{
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25) !important;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)


def decode_upload(uploaded_file: object) -> np.ndarray | None:
    """Đọc ảnh tải lên thành ảnh xám OpenCV."""
    if uploaded_file is None:
        return None
    raw = np.frombuffer(uploaded_file.getvalue(), dtype=np.uint8)
    return cv2.imdecode(raw, cv2.IMREAD_GRAYSCALE)


# =============================================================================
# 2. KHỞI TẠO STATE VÀ QUẢN LÝ DỮ LIỆU
# =============================================================================

if "current_sample_id" not in st.session_state:
    st.session_state["current_sample_id"] = PRESET_CASES[0]["id"]

image_dir = os.path.join(PROJECT_ROOT, "data", "full", "images")
all_files = list_sample_cases(image_dir)


# =============================================================================
# 3. TOP BANNER / HEADER TRẠM CHẨN ĐOÁN
# =============================================================================

st.markdown(
    """
    <div class="pacs-header">
      <div class="pacs-badge">
        HUIT DATA SCIENCE LAB · DIGITAL IMAGE PROCESSING
      </div>
      <h1 class="pacs-title">
        NEUROSCAN PACS WORKSTATION
      </h1>
      <p class="pacs-subtitle">
        Hệ thống phân đoạn tự động và định lượng hình học khối u não trên ảnh cộng hưởng từ MRI chuẩn hóa quốc tế TCGA-LGG.
      </p>
      <div class="pacs-status-bar">
        <div class="pacs-pill">Kho dữ liệu: <b>3,929 lát cắt chuẩn</b></div>
        <div class="pacs-pill">Quy mô: <b>110 bệnh nhân</b></div>
        <div class="pacs-pill">Bộ giải thuật: <b>Watershed EDT vs Region Growing</b></div>
        <div class="pacs-pill">Độ đặc hiệu não lành: <b>99.04%</b></div>
        <div class="pacs-pill">Độ trễ xử lý: <b>~6.13 ms / lát</b></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 4. THANH TRẢI NGHIỆM NHANH 4 CA LÂM SÀNG TIÊU BIỂU (CURATED PRESETS)
# =============================================================================

st.markdown(
    "<div class='preset-bar-title'>Danh Mục Ca Lâm Sàng Tiêu Biểu (Phân Tích Nhanh):</div>",
    unsafe_allow_html=True,
)

preset_cols = st.columns(4)
for idx, (col, preset) in enumerate(zip(preset_cols, PRESET_CASES)):
    with col:
        is_active = st.session_state.get("current_sample_id") == preset["id"]
        btn_label = f"{preset['title']} [{preset['badge']}]"
        btn_type = "primary" if is_active else "secondary"
        if st.button(btn_label, key=f"btn_preset_{idx}", type=btn_type, use_container_width=True):
            st.session_state["current_sample_id"] = preset["id"]
            st.rerun()


# =============================================================================
# 5. SIDEBAR: BẢNG ĐIỀU KHIỂN THAM SỐ VÀ DỮ LIỆU
# =============================================================================

with st.sidebar:
    # 5.1. BỘ CHỌN CHẾ ĐỘ GIAO DIỆN SÁNG / TỐI
    st.markdown("### Giao Diện Hiển Thị")
    st.radio(
        "Chế độ màu",
        ("Chế độ Sáng (Clinical Light)", "Chế độ Tối (Clinical Dark)"),
        key="theme_mode_selector",
        label_visibility="collapsed",
        horizontal=True,
    )

    st.markdown("---")
    st.markdown("### Bảng Điều Khiển")
    st.caption("Cấu hình nguồn ảnh, giải thuật và các siêu tham số xử lý.")

    source_mode = st.radio(
        "Nguồn ảnh đầu vào",
        ("Kho chuẩn TCGA-LGG (3,929 lát)", "Tải ảnh từ máy tính"),
        index=0,
    )

    input_img: np.ndarray | None = None
    input_gt_mask: np.ndarray | None = None
    sample_id: str | None = None

    if source_mode == "Kho chuẩn TCGA-LGG (3,929 lát)":
        if all_files:
            patient_filter = st.text_input(
                "Tìm nhanh mã bệnh nhân",
                placeholder="Ví dụ: TCGA_CS_4942, TCGA_DU...",
            ).strip().upper()

            filtered = (
                [f for f in all_files if patient_filter in f.upper()]
                if patient_filter
                else all_files
            )

            if filtered:
                # Tìm index của preset hiện tại nếu có trong danh sách
                curr_id = st.session_state.get("current_sample_id", "")
                default_idx = 0
                for i, fname in enumerate(filtered):
                    if curr_id in fname:
                        default_idx = i
                        break

                selected_file = st.selectbox(
                    f"Lát cắt MRI ({len(filtered)} ảnh)",
                    filtered,
                    index=default_idx,
                )
                sample_id = os.path.splitext(selected_file)[0]
                st.session_state["current_sample_id"] = sample_id
                input_img, input_gt_mask = load_image_and_mask(sample_id)
            else:
                st.warning("Không tìm thấy ảnh nào khớp với mã lọc.")
        else:
            st.error("Chưa tìm thấy thư mục data/full/images.")
    else:
        uploaded_image = st.file_uploader(
            "Ảnh MRI cắt lát",
            type=("png", "jpg", "jpeg", "tif", "tiff"),
        )
        input_img = decode_upload(uploaded_image)
        uploaded_mask = st.file_uploader(
            "Mặt nạ Ground Truth (Tùy chọn)",
            type=("png", "jpg", "jpeg", "tif", "tiff"),
        )
        input_gt_mask = decode_upload(uploaded_mask)
        sample_id = uploaded_image.name if uploaded_image else "Uploaded_Case"

    st.markdown("---")
    st.markdown("### Chế Độ Chẩn Đoán")

    analysis_mode = st.radio(
        "Chế độ hiển thị",
        (
            "Chi tiết 4 tầng xử lý (Pipeline Inspection)",
            "So sánh song song 2 thuật toán (Dual Comparison)",
            "Bản đồ sai số y khoa (Diagnostic Error Map)",
        ),
        index=0,
    )

    st.markdown("---")
    st.markdown("### Cấu Hình Siêu Tham Số")

    method_choice = st.selectbox(
        "Giải thuật chính",
        ("Marker-controlled Watershed (Baseline)", "Seeded Region Growing (Đối chứng)"),
        index=0,
    )
    is_ws = "Watershed" in method_choice
    primary_method_key = "watershed" if is_ws else "region_growing"

    with st.expander("Tinh chỉnh tham số nâng cao", expanded=True):
        if is_ws:
            dist_ratio = st.slider(
                "Ngưỡng khoảng cách EDT (dist_thresh_ratio)",
                min_value=0.1,
                max_value=0.8,
                value=0.4,
                step=0.05,
                help="Tỷ lệ so với khoảng cách cực đại để định vị hạt giống u (Sure Foreground).",
            )
            pipeline_params = {"dist_thresh_ratio": dist_ratio}
        else:
            tolerance = st.slider(
                "Dung sai mức xám (intensity_tolerance)",
                min_value=5,
                max_value=40,
                value=15,
                step=1,
                help="Ngưỡng chênh lệch cường độ sáng tối đa để lan truyền pixel u.",
            )
            pipeline_params = {"intensity_tolerance": tolerance}

        st.caption("Lưu ý: Mặc định tối ưu: Watershed ratio = 0.4, Region Growing tolerance = 15.")

    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 0.75rem; color: var(--text-muted); line-height: 1.4;'>
          <b>Đồ án Xử lý ảnh số (HUIT - 2026)</b><br>
          Nhóm sinh viên: Hà Mạnh Trường & Huỳnh Tâm Trí<br>
          GVHD: ThS. Đinh Nguyễn Trọng Nghĩa
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# 6. THỰC THI PIPELINE VÀ TÍNH TOÁN KẾT QUẢ
# =============================================================================

if input_img is None:
    st.info("Vui lòng chọn một ca chụp trong danh mục hoặc tải ảnh MRI lên từ máy tính.")
else:
    # 1. Chạy thuật toán chính
    t_start = time.perf_counter()
    pipeline_primary = BrainTumorPipeline(method=primary_method_key, params=pipeline_params)
    diag_primary, inter_primary = pipeline_primary.process(input_img, gt_mask=input_gt_mask)
    latency_primary = (time.perf_counter() - t_start) * 1000.0

    # 2. Chạy thuật toán phụ phục vụ chế độ so sánh song song
    t_start_sec = time.perf_counter()
    secondary_method_key = "region_growing" if is_ws else "watershed"
    sec_params = {"intensity_tolerance": 15} if secondary_method_key == "region_growing" else {"dist_thresh_ratio": 0.4}
    pipeline_sec = BrainTumorPipeline(method=secondary_method_key, params=sec_params)
    diag_sec, inter_sec = pipeline_sec.process(input_img, gt_mask=input_gt_mask)
    latency_sec = (time.perf_counter() - t_start_sec) * 1000.0

    # =========================================================================
    # 7. DẢI THẺ KPI Y SINH NỔI BẬT (HERO CLINICAL CARDS)
    # =========================================================================

    has_gt = input_gt_mask is not None
    gt_tumor_px = int(np.sum(input_gt_mask > 0)) if has_gt else None
    has_pred_tumor = diag_primary.tumor_detected

    # Đối chiếu chẩn đoán giữa thuật toán phân đoạn và Ground Truth y tế
    if has_gt:
        if gt_tumor_px == 0 and has_pred_tumor:
            status_card_class = "card-amber"
            status_badge_text = "DƯƠNG TÍNH GIẢ (BÁO NHẦM)"
            status_color = "#d97706"
            status_sub_text = "Thực tế bệnh nhân: Não lành không u (GT: 0 px)"
        elif gt_tumor_px == 0 and not has_pred_tumor:
            status_card_class = "alert-success"
            status_badge_text = "MÔ NÃO LÀNH TÍNH"
            status_color = "#059669"
            status_sub_text = "Khớp chuẩn y tế: Không có khối u (GT: 0 px)"
        elif gt_tumor_px > 0 and has_pred_tumor:
            status_card_class = "alert-danger"
            status_badge_text = "PHÁT HIỆN KHỐI U NÃO"
            status_color = "#dc2626"
            status_sub_text = f"Dương tính thật: GT {gt_tumor_px:,} px"
        else:
            status_card_class = "card-amber"
            status_badge_text = "BỎ SÓT KHỐI U (ÂM TÍNH GIẢ)"
            status_color = "#d97706"
            status_sub_text = f"Thực tế bệnh nhân: Có u (GT: {gt_tumor_px:,} px)"
    else:
        status_card_class = "alert-danger" if has_pred_tumor else "alert-success"
        status_badge_text = "PHÁT HIỆN KHỐI U NÃO" if has_pred_tumor else "MÔ NÃO LÀNH TÍNH"
        status_color = "#dc2626" if has_pred_tumor else "#059669"
        status_sub_text = f"Độ trễ xử lý: {latency_primary:.1f} ms"

    # Điểm Dice và IoU
    if has_gt and gt_tumor_px == 0:
        dice_val = "0.0000 (Ca âm tính)"
        iou_val = "0.0000 (Ca âm tính)"
        dice_color = "#64748b"
    elif diag_primary.dice_score is not None:
        dice_val = f"{diag_primary.dice_score:.4f}"
        iou_val = f"{diag_primary.iou_score:.4f}"
        dice_color = "#059669" if diag_primary.dice_score >= 0.75 else "#0284c7"
    else:
        dice_val = "N/A"
        iou_val = "N/A"
        dice_color = "#64748b"

    # Nhận xét hình thái học
    if not has_pred_tumor or diag_primary.tumor_area_px == 0:
        circ_note = "Không ghi nhận bờ tổn thương"
    elif diag_primary.circularity >= 0.6:
        circ_note = "Bờ u tròn đều (Lành tính)"
    elif diag_primary.circularity >= 0.4:
        circ_note = "Bờ u gồ ghề (Trung bình)"
    else:
        circ_note = "Bờ u chân rết (Xâm lấn)"

    st.markdown(
        f"""
        <div class="kpi-container">
          <div class="kpi-card {status_card_class}">
            <div class="kpi-label">Trạng Thái Chẩn Đoán</div>
            <div class="kpi-val" style="color: {status_color}; font-size: 1.35rem;">
              {status_badge_text}
            </div>
            <div class="kpi-sub">{status_sub_text}</div>
          </div>

          <div class="kpi-card card-blue">
            <div class="kpi-label">Diện Tích Tổn Thương</div>
            <div class="kpi-val">{diag_primary.tumor_area_px:,} <span style="font-size: 0.9rem; color: var(--text-muted);">px</span></div>
            <div class="kpi-sub">Khoang não: {diag_primary.brain_area_px:,} px</div>
          </div>

          <div class="kpi-card card-amber">
            <div class="kpi-label">Tỷ Lệ Xâm Lấn Não</div>
            <div class="kpi-val">{diag_primary.tumor_ratio_percent:.2f}%</div>
            <div class="kpi-sub">Chiếm dụng khoang sọ não</div>
          </div>

          <div class="kpi-card card-purple">
            <div class="kpi-label">Độ Tròn Bờ U (Circularity)</div>
            <div class="kpi-val">{diag_primary.circularity:.3f}</div>
            <div class="kpi-sub">{circ_note}</div>
          </div>

          <div class="kpi-card {'alert-success' if diag_primary.dice_score and diag_primary.dice_score >= 0.75 else 'card-blue'}">
            <div class="kpi-label">Độ Tương Đồng Y Sinh</div>
            <div class="kpi-val" style="color: {dice_color};">
              Dice: {dice_val}
            </div>
            <div class="kpi-sub">IoU (Jaccard): {iou_val}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================================
    # 8. CÁC CHẾ ĐỘ HIỂN THỊ CHẨN ĐOÁN
    # =========================================================================

    if "Chi tiết 4 tầng" in analysis_mode:
        st.markdown(
            "<div class='section-heading'>Chi Tiết 4 Tầng Xử Lý Ảnh Số (Quad Pipeline Inspection)</div>",
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                """
                <div class="img-card">
                  <div class="img-card-header">
                    <span class="img-card-title">1. Ảnh MRI Gốc</span>
                    <span class="img-card-tag">FLAIR / T1</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(inter_primary["original"], use_container_width=True)
            st.caption("Ảnh xám đầu vào kích thước 256x256 pixel.")

        with col2:
            st.markdown(
                """
                <div class="img-card">
                  <div class="img-card-header">
                    <span class="img-card-title">2. Tách Sọ Não 6 Bước</span>
                    <span class="img-card-tag">Skull Stripped</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(inter_primary["stripped"], use_container_width=True)
            st.caption("Otsu + Opening + LCC loại bỏ 100% xương sọ.")

        with col3:
            st.markdown(
                """
                <div class="img-card">
                  <div class="img-card-header">
                    <span class="img-card-title">3. Mặt Nạ Phân Đoạn</span>
                    <span class="img-card-tag">Binary Mask</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(inter_primary["tumor_mask"], use_container_width=True)
            st.caption(f"Giải thuật: {method_choice.split()[0]}.")

        with col4:
            st.markdown(
                """
                <div class="img-card">
                  <div class="img-card-header">
                    <span class="img-card-title">4. Cảnh Báo Thị Giác</span>
                    <span class="img-card-tag">BBox + Contour</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(cv2.cvtColor(inter_primary["overlay"], cv2.COLOR_BGR2RGB), use_container_width=True)
            st.caption("Khung viền đỏ Bounding Box và đường bao viền vàng.")

    elif "So sánh song song" in analysis_mode:
        st.markdown(
            "<div class='section-heading'>Đối Chứng Song Song 2 Giải Thuật Trên Cùng Một Lát Cắt</div>",
            unsafe_allow_html=True,
        )

        ws_inter = inter_primary if is_ws else inter_sec
        ws_diag = diag_primary if is_ws else diag_sec
        ws_latency = latency_primary if is_ws else latency_sec

        rg_inter = inter_sec if is_ws else inter_primary
        rg_diag = diag_sec if is_ws else diag_primary
        rg_latency = latency_sec if is_ws else latency_primary

        col_ws, col_rg = st.columns(2)

        with col_ws:
            st.markdown(
                """
                <div class="img-card" style="border-top: 3px solid #0ea5e9;">
                  <div class="img-card-header">
                    <span class="img-card-title">Phương Án A: Marker-Controlled Watershed (Baseline)</span>
                    <span class="img-card-tag">Đề Xuất Chính</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(cv2.cvtColor(ws_inter["overlay"], cv2.COLOR_BGR2RGB), use_container_width=True)

            ws_dice_str = f"{ws_diag.dice_score:.4f}" if ws_diag.dice_score is not None else "N/A"
            ws_iou_str = f"{ws_diag.iou_score:.4f}" if ws_diag.iou_score is not None else "N/A"
            st.markdown(
                f"""
                <div class="stat-box">
                  - <b>Dice Similarity:</b> <span style="color: #059669; font-weight: bold;">{ws_dice_str}</span><br>
                  - <b>IoU (Jaccard):</b> {ws_iou_str}<br>
                  - <b>Diện tích phát hiện:</b> {ws_diag.tumor_area_px:,} px<br>
                  - <b>Độ trễ xử lý:</b> {ws_latency:.2f} ms<br>
                  - <i>Cơ chế: Biến đổi khoảng cách Euclidean EDT neo hạt giống trung tâm u bền vững.</i>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_rg:
            st.markdown(
                """
                <div class="img-card" style="border-top: 3px solid #f59e0b;">
                  <div class="img-card-header">
                    <span class="img-card-title">Phương Án B: Seeded Region Growing (Đối Chứng)</span>
                    <span class="img-card-tag">Giải Thuật Lan Vùng</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(cv2.cvtColor(rg_inter["overlay"], cv2.COLOR_BGR2RGB), use_container_width=True)

            rg_dice_str = f"{rg_diag.dice_score:.4f}" if rg_diag.dice_score is not None else "N/A"
            rg_iou_str = f"{rg_diag.iou_score:.4f}" if rg_diag.iou_score is not None else "N/A"
            st.markdown(
                f"""
                <div class="stat-box">
                  - <b>Dice Similarity:</b> <span style="color: #d97706; font-weight: bold;">{rg_dice_str}</span><br>
                  - <b>IoU (Jaccard):</b> {rg_iou_str}<br>
                  - <b>Diện tích phát hiện:</b> {rg_diag.tumor_area_px:,} px<br>
                  - <b>Độ trễ xử lý:</b> {rg_latency:.2f} ms<br>
                  - <i>Cơ chế: Dò hạt giống cường độ cực đại và lan truyền theo hàng đợi 8 hướng BFS.</i>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:  # Bản đồ sai số y khoa (Error Map)
        st.markdown(
            "<div class='section-heading'>Bản Đồ Phân Rã Sai Số Y Khoa (Diagnostic Error Map)</div>",
            unsafe_allow_html=True,
        )

        if input_gt_mask is None:
            st.warning("Ca chụp này chưa có mặt nạ Ground Truth. Vui lòng chọn một ca trong kho TCGA-LGG để xem bản đồ phân rã sai số.")
        else:
            error_img = generate_error_map(input_img, inter_primary["tumor_mask"], input_gt_mask)

            col_err_img, col_err_stats = st.columns([1.1, 1.0])

            with col_err_img:
                st.markdown(
                    """
                    <div class="img-card">
                      <div class="img-card-header">
                        <span class="img-card-title">Bản Đồ Phân Tích Điểm Ảnh (Pixel-Level Error Breakdown)</span>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.image(error_img, use_container_width=True)

            with col_err_stats:
                # Tính chi tiết số pixel
                pred_bin = inter_primary["tumor_mask"] > 0
                gt_bin = input_gt_mask > 0
                tp_px = int(np.sum(pred_bin & gt_bin))
                fp_px = int(np.sum(pred_bin & (~gt_bin)))
                fn_px = int(np.sum((~pred_bin) & gt_bin))
                tn_px = int(np.sum((~pred_bin) & (~gt_bin)))

                sens = tp_px / (tp_px + fn_px) if (tp_px + fn_px) > 0 else 1.0
                spec = tn_px / (tn_px + fp_px) if (tn_px + fp_px) > 0 else 1.0

                st.markdown(
                    f"""
                    <div class="error-breakdown-box">
                      <div style="font-weight: 700; font-size: 1rem; color: var(--text-primary); margin-bottom: 0.8rem;">Chú Giải & Thống Kê Điểm Ảnh:</div>

                      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem; padding: 0.4rem 0.6rem; background: rgba(34, 197, 94, 0.12); border-left: 4px solid #059669; border-radius: 4px;">
                        <span><b style="color: #059669;">Đúng Chuẩn (True Positive - TP):</b></span>
                        <span style="font-family: 'JetBrains Mono'; font-weight: bold; color: var(--text-primary);">{tp_px:,} px</span>
                      </div>

                      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem; padding: 0.4rem 0.6rem; background: rgba(239, 68, 68, 0.12); border-left: 4px solid #dc2626; border-radius: 4px;">
                        <span><b style="color: #dc2626;">Báo Nhầm (False Positive - FP):</b></span>
                        <span style="font-family: 'JetBrains Mono'; font-weight: bold; color: var(--text-primary);">{fp_px:,} px</span>
                      </div>

                      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; padding: 0.4rem 0.6rem; background: rgba(245, 158, 11, 0.12); border-left: 4px solid #d97706; border-radius: 4px;">
                        <span><b style="color: #d97706;">Bỏ Sót (False Negative - FN):</b></span>
                        <span style="font-family: 'JetBrains Mono'; font-weight: bold; color: var(--text-primary);">{fn_px:,} px</span>
                      </div>

                      <div style="font-size: 0.85rem; color: var(--text-secondary); border-top: 1px solid var(--border-color); padding-top: 0.8rem; line-height: 1.6;">
                        - <b>Độ nhạy (Sensitivity / Recall):</b> <span style="color: #0284c7; font-weight: bold;">{sens*100:.2f}%</span><br>
                        - <b>Độ đặc hiệu (Specificity):</b> <span style="color: #059669; font-weight: bold;">{spec*100:.2f}%</span><br>
                        - <b>Dice Similarity:</b> <span style="color: #0284c7; font-weight: bold;">{diag_primary.dice_score:.4f}</span>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # =========================================================================
    # 9. KHU VỰC XUẤT HỒ SƠ CHẨN ĐOÁN VÀ TẢI BÁO CÁO
    # =========================================================================

    st.markdown("---")
    st.markdown(
        "<div class='section-heading' style='font-size: 1rem;'>Hồ Sơ Chẩn Đoán & Xuất Báo Cáo Y Khoa</div>",
        unsafe_allow_html=True,
    )

    report_csv = io.StringIO()
    writer = csv.writer(report_csv)
    writer.writerow((
        "Mã_Ca_Chụp",
        "Thuật_Toán",
        "Trạng_Thái_Phát_Hiện",
        "Diện_Tích_U_px",
        "Diện_Tích_Não_px",
        "Tỷ_Lệ_U_Não_Percent",
        "Độ_Tròn_Circularity",
        "Điểm_Dice",
        "Điểm_IoU",
        "Độ_Trễ_ms",
    ))
    writer.writerow((
        sample_id or "Upload_Case",
        primary_method_key,
        diag_primary.tumor_detected,
        diag_primary.tumor_area_px,
        diag_primary.brain_area_px,
        round(diag_primary.tumor_ratio_percent, 4),
        round(diag_primary.circularity, 4),
        round(diag_primary.dice_score, 4) if diag_primary.dice_score is not None else "N/A",
        round(diag_primary.iou_score, 4) if diag_primary.iou_score is not None else "N/A",
        round(latency_primary, 2),
    ))

    down_col1, down_col2 = st.columns([1, 3])
    with down_col1:
        st.download_button(
            "Tải Báo Cáo Chẩn Đoán CSV",
            data=report_csv.getvalue().encode("utf-8-sig"),
            file_name=f"NeuroScan_Report_{sample_id or 'MRI'}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with down_col2:
        st.caption(f"Hồ sơ mã ca: {sample_id} | Phương pháp: {primary_method_key} | Trạng thái xác thực: Đạt chuẩn (PASSED)")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: var(--text-muted); font-size: 0.8rem; padding: 1rem 0;'>
      Đồ án Học phần Xử lý ảnh số (0101006276) - Bộ môn Khoa học Dữ liệu - Khoa CNTT - Trường ĐH Công Thương TP.HCM (HUIT).<br>
      <i>Sản phẩm phục vụ nghiên cứu khoa học và minh chứng đồ án. Không dùng thay thế chỉ định y tế chính thức.</i>
    </div>
    """,
    unsafe_allow_html=True,
)
