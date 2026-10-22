"""Web demo Streamlit chan doan u nao MRI - Giao dien NeuroScan PACS Workstation.
Khoa Cong nghe Thong tin - Bo mon Khoa hoc Du lieu - Dai hoc Cong Thuong TP.HCM (HUIT).
Giao dien chuan hoa y te, ho tro chuyen doi giua Che do Sang (mac dinh) va Che do Toi.
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
# 1. CAU HINH TRANG VA QUAN LY CHE DO GIAO DIEN (THEME)
# =============================================================================

st.set_page_config(
    page_title="NeuroScan Pro - Phan Doan U Nao MRI | HUIT",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Nhận diện chế độ giao diện từ session_state (mặc định Sáng theo yêu cầu)
if "theme_mode_selector" not in st.session_state:
    st.session_state["theme_mode_selector"] = "Che do Sang (Clinical Light)"

is_light = "Sang" in st.session_state["theme_mode_selector"]

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

      /* Secondary Buttons (nhu cac Preset) */
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

      /* Frame anh chuyen dung */
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

      /* Hop thong so thong ke doi chung */
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

      /* Hop phan tich ban do sai so */
      .error-breakdown-box {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
      }}

      /* Tuy chinh Tabs */
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
    """Doc anh tai len thanh anh xam OpenCV."""
    if uploaded_file is None:
        return None
    raw = np.frombuffer(uploaded_file.getvalue(), dtype=np.uint8)
    return cv2.imdecode(raw, cv2.IMREAD_GRAYSCALE)


# =============================================================================
# 2. KHOI TAO STATE VA QUAN LY DU LIEU
# =============================================================================

if "current_sample_id" not in st.session_state:
    st.session_state["current_sample_id"] = PRESET_CASES[0]["id"]

image_dir = os.path.join(PROJECT_ROOT, "data", "full", "images")
all_files = list_sample_cases(image_dir)


# =============================================================================
# 3. TOP BANNER / HEADER TRAM CHAN DOAN
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
        He thong phan doan tu dong va dinh luong hinh hoc khoi u nao tren anh cong huong tu MRI chuan hoa quoc te TCGA-LGG.
      </p>
      <div class="pacs-status-bar">
        <div class="pacs-pill">Kho du lieu: <b>3,929 lat cat chuan</b></div>
        <div class="pacs-pill">Quy mo: <b>110 benh nhan</b></div>
        <div class="pacs-pill">Bo giai thuat: <b>Watershed EDT vs Region Growing</b></div>
        <div class="pacs-pill">Do dac hieu nao lanh: <b>99.04%</b></div>
        <div class="pacs-pill">Do tre xu ly: <b>~6.13 ms / lat</b></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 4. THANH TRAI NGHIEM NHANH 4 CA LAM SANG TIEU BIEU (CURATED PRESETS)
# =============================================================================

st.markdown(
    "<div class='preset-bar-title'>Danh Muc Ca Lam Sang Tieu Bieu (Phan Tich Nhanh):</div>",
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
# 5. SIDEBAR: BANG DIEU KHIEN THAM SO VA DU LIEU
# =============================================================================

with st.sidebar:
    # 5.1. BO CHON CHE DO GIAO DIEN SANG / TOI
    st.markdown("### Giao Dien Hien Thi")
    st.radio(
        "Che do mau",
        ("Che do Sang (Clinical Light)", "Che do Toi (Clinical Dark)"),
        key="theme_mode_selector",
        label_visibility="collapsed",
        horizontal=True,
    )

    st.markdown("---")
    st.markdown("### Bang Dieu Khien")
    st.caption("Cau hinh nguon anh, giai thuat va cac sieu tham so xu ly.")

    source_mode = st.radio(
        "Nguon anh dau vao",
        ("Kho chuan TCGA-LGG (3,929 lat)", "Tai anh tu may tinh"),
        index=0,
    )

    input_img: np.ndarray | None = None
    input_gt_mask: np.ndarray | None = None
    sample_id: str | None = None

    if source_mode == "Kho chuan TCGA-LGG (3,929 lat)":
        if all_files:
            patient_filter = st.text_input(
                "Tim nhanh ma benh nhan",
                placeholder="Vi du: TCGA_CS_4942, TCGA_DU...",
            ).strip().upper()

            filtered = (
                [f for f in all_files if patient_filter in f.upper()]
                if patient_filter
                else all_files
            )

            if filtered:
                # Tim index cua preset hien tai neu co trong danh sach
                curr_id = st.session_state.get("current_sample_id", "")
                default_idx = 0
                for i, fname in enumerate(filtered):
                    if curr_id in fname:
                        default_idx = i
                        break

                selected_file = st.selectbox(
                    f"Lat cat MRI ({len(filtered)} anh)",
                    filtered,
                    index=default_idx,
                )
                sample_id = os.path.splitext(selected_file)[0]
                st.session_state["current_sample_id"] = sample_id
                input_img, input_gt_mask = load_image_and_mask(sample_id)
            else:
                st.warning("Khong tim thay anh nao khop voi ma loc.")
        else:
            st.error("Chua tim thay thu muc data/full/images.")
    else:
        uploaded_image = st.file_uploader(
            "Anh MRI cat lat",
            type=("png", "jpg", "jpeg", "tif", "tiff"),
        )
        input_img = decode_upload(uploaded_image)
        uploaded_mask = st.file_uploader(
            "Mat na Ground Truth (Tuy chon)",
            type=("png", "jpg", "jpeg", "tif", "tiff"),
        )
        input_gt_mask = decode_upload(uploaded_mask)
        sample_id = uploaded_image.name if uploaded_image else "Uploaded_Case"

    st.markdown("---")
    st.markdown("### Che Do Chan Doan")

    analysis_mode = st.radio(
        "Che do hien thi",
        (
            "Chi tiet 4 tang xu ly (Pipeline Inspection)",
            "So sanh song song 2 thuat toan (Dual Comparison)",
            "Ban do sai so y khoa (Diagnostic Error Map)",
        ),
        index=0,
    )

    st.markdown("---")
    st.markdown("### Cau Hinh Sieu Tham So")

    method_choice = st.selectbox(
        "Giai thuat chinh",
        ("Marker-controlled Watershed (Baseline)", "Seeded Region Growing (Doi chung)"),
        index=0,
    )
    is_ws = "Watershed" in method_choice
    primary_method_key = "watershed" if is_ws else "region_growing"

    with st.expander("Tinh chinh tham so nang cao", expanded=True):
        if is_ws:
            dist_ratio = st.slider(
                "Nguong khoang cach EDT (dist_thresh_ratio)",
                min_value=0.1,
                max_value=0.8,
                value=0.4,
                step=0.05,
                help="Ty le so voi khoang cach cuc dai de dinh vi hat giong u (Sure Foreground).",
            )
            pipeline_params = {"dist_thresh_ratio": dist_ratio}
        else:
            tolerance = st.slider(
                "Dung sai muc xam (intensity_tolerance)",
                min_value=5,
                max_value=40,
                value=15,
                step=1,
                help="Nguong chenh lech cuong do sang toi da de lan truyen pixel u.",
            )
            pipeline_params = {"intensity_tolerance": tolerance}

        st.caption("Luu y: Mac dinh toi uu: Watershed ratio = 0.4, Region Growing tolerance = 15.")

    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 0.75rem; color: var(--text-muted); line-height: 1.4;'>
          <b>Do an Xu ly anh so (HUIT - 2026)</b><br>
          Nhom sinh vien: Ha Manh Truong & Huynh Tam Tri<br>
          GVHD: ThS. Dinh Nguyen Trong Nghia
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# 6. THUC THI PIPELINE VA TINH TOAN KET QUA
# =============================================================================

if input_img is None:
    st.info("Vui long chon mot ca chup trong danh muc hoac tai anh MRI len tu may tinh.")
else:
    # 1. Chay thuat toan chinh
    t_start = time.perf_counter()
    pipeline_primary = BrainTumorPipeline(method=primary_method_key, params=pipeline_params)
    diag_primary, inter_primary = pipeline_primary.process(input_img, gt_mask=input_gt_mask)
    latency_primary = (time.perf_counter() - t_start) * 1000.0

    # 2. Chay thuat toan phu phuc vu che do so sanh song song
    t_start_sec = time.perf_counter()
    secondary_method_key = "region_growing" if is_ws else "watershed"
    sec_params = {"intensity_tolerance": 15} if secondary_method_key == "region_growing" else {"dist_thresh_ratio": 0.4}
    pipeline_sec = BrainTumorPipeline(method=secondary_method_key, params=sec_params)
    diag_sec, inter_sec = pipeline_sec.process(input_img, gt_mask=input_gt_mask)
    latency_sec = (time.perf_counter() - t_start_sec) * 1000.0

    # =========================================================================
    # 7. DAI THE KPI Y SINH NOI BAT (HERO CLINICAL CARDS)
    # =========================================================================

    has_tumor = diag_primary.tumor_detected
    status_card_class = "alert-danger" if has_tumor else "alert-success"
    status_badge_text = "PHAT HIEN KHOI U NAO" if has_tumor else "MO NAO LANH TINH"
    status_color = "#dc2626" if has_tumor else "#059669"

    dice_val = f"{diag_primary.dice_score:.4f}" if diag_primary.dice_score is not None else "N/A"
    iou_val = f"{diag_primary.iou_score:.4f}" if diag_primary.iou_score is not None else "N/A"

    # Nhan xet hinh thai hoc
    if diag_primary.circularity >= 0.6:
        circ_note = "Bo u tron deu (Lanh tinh)"
    elif diag_primary.circularity >= 0.4:
        circ_note = "Bo u go ghe (Trung binh)"
    else:
        circ_note = "Bo u chan ret (Xam lan)"

    st.markdown(
        f"""
        <div class="kpi-container">
          <div class="kpi-card {status_card_class}">
            <div class="kpi-label">Trang Thai Chan Doan</div>
            <div class="kpi-val" style="color: {status_color}; font-size: 1.35rem;">
              {status_badge_text}
            </div>
            <div class="kpi-sub">Do tre xu ly: {latency_primary:.1f} ms</div>
          </div>

          <div class="kpi-card card-blue">
            <div class="kpi-label">Dien Tich Ton Thuong</div>
            <div class="kpi-val">{diag_primary.tumor_area_px:,} <span style="font-size: 0.9rem; color: var(--text-muted);">px</span></div>
            <div class="kpi-sub">Khoang nao: {diag_primary.brain_area_px:,} px</div>
          </div>

          <div class="kpi-card card-amber">
            <div class="kpi-label">Ty Le Xam Lan Nao</div>
            <div class="kpi-val">{diag_primary.tumor_ratio_percent:.2f}%</div>
            <div class="kpi-sub">Chiem dung khoang so nao</div>
          </div>

          <div class="kpi-card card-purple">
            <div class="kpi-label">Do Tron Bo U (Circularity)</div>
            <div class="kpi-val">{diag_primary.circularity:.3f}</div>
            <div class="kpi-sub">{circ_note}</div>
          </div>

          <div class="kpi-card {'alert-success' if diag_primary.dice_score and diag_primary.dice_score >= 0.75 else 'card-blue'}">
            <div class="kpi-label">Do Tuong Dong Y Sinh</div>
            <div class="kpi-val" style="color: {'#059669' if diag_primary.dice_score and diag_primary.dice_score >= 0.75 else '#0284c7'};">
              Dice: {dice_val}
            </div>
            <div class="kpi-sub">IoU (Jaccard): {iou_val}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================================
    # 8. CAC CHE DO HIEN THI CHAN DOAN
    # =========================================================================

    if "Chi tiet 4 tang" in analysis_mode:
        st.markdown(
            "<div class='section-heading'>Chi Tiet 4 Tang Xu Ly Anh So (Quad Pipeline Inspection)</div>",
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                """
                <div class="img-card">
                  <div class="img-card-header">
                    <span class="img-card-title">1. Anh MRI Goc</span>
                    <span class="img-card-tag">FLAIR / T1</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(inter_primary["original"], use_container_width=True)
            st.caption("Anh xam dau vao kich thuoc 256x256 pixel.")

        with col2:
            st.markdown(
                """
                <div class="img-card">
                  <div class="img-card-header">
                    <span class="img-card-title">2. Tach So Nao 6 Buoc</span>
                    <span class="img-card-tag">Skull Stripped</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(inter_primary["stripped"], use_container_width=True)
            st.caption("Otsu + Opening + LCC loai bo 100% xuong so.")

        with col3:
            st.markdown(
                """
                <div class="img-card">
                  <div class="img-card-header">
                    <span class="img-card-title">3. Mat Na Phan Doan</span>
                    <span class="img-card-tag">Binary Mask</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(inter_primary["tumor_mask"], use_container_width=True)
            st.caption(f"Giai thuat: {method_choice.split()[0]}.")

        with col4:
            st.markdown(
                """
                <div class="img-card">
                  <div class="img-card-header">
                    <span class="img-card-title">4. Canh Bao Thi Giac</span>
                    <span class="img-card-tag">BBox + Contour</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(cv2.cvtColor(inter_primary["overlay"], cv2.COLOR_BGR2RGB), use_container_width=True)
            st.caption("Khung vien do Bounding Box va duong bao vien vang.")

    elif "So sanh song song" in analysis_mode:
        st.markdown(
            "<div class='section-heading'>Doi Chung Song Song 2 Giai Thuat Tren Cung Mot Lat Cat</div>",
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
                    <span class="img-card-title">Phuong An A: Marker-Controlled Watershed (Baseline)</span>
                    <span class="img-card-tag">De Xuat Chinh</span>
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
                  - <b>Dien tich phat hien:</b> {ws_diag.tumor_area_px:,} px<br>
                  - <b>Do tre xu ly:</b> {ws_latency:.2f} ms<br>
                  - <i>Co che: Bien doi khoang cach Euclidean EDT neo hat giong trung tam u ben vung.</i>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_rg:
            st.markdown(
                """
                <div class="img-card" style="border-top: 3px solid #f59e0b;">
                  <div class="img-card-header">
                    <span class="img-card-title">Phuong An B: Seeded Region Growing (Doi Chung)</span>
                    <span class="img-card-tag">Giai Thuat Lan Vung</span>
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
                  - <b>Dien tich phat hien:</b> {rg_diag.tumor_area_px:,} px<br>
                  - <b>Do tre xu ly:</b> {rg_latency:.2f} ms<br>
                  - <i>Co che: Do hat giong cuong do cuc dai va lan truyen theo hang doi 8 huong BFS.</i>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:  # Ban do sai so y khoa (Error Map)
        st.markdown(
            "<div class='section-heading'>Ban Do Phan Ra Sai So Y Khoa (Diagnostic Error Map)</div>",
            unsafe_allow_html=True,
        )

        if input_gt_mask is None:
            st.warning("Ca chup nay chua co mat na Ground Truth. Vui long chon mot ca trong kho TCGA-LGG de xem ban do phan ra sai so.")
        else:
            error_img = generate_error_map(input_img, inter_primary["tumor_mask"], input_gt_mask)

            col_err_img, col_err_stats = st.columns([1.1, 1.0])

            with col_err_img:
                st.markdown(
                    """
                    <div class="img-card">
                      <div class="img-card-header">
                        <span class="img-card-title">Ban Do Phan Tich Diem Anh (Pixel-Level Error Breakdown)</span>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.image(error_img, use_container_width=True)

            with col_err_stats:
                # Tinh chi tiet so pixel
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
                      <div style="font-weight: 700; font-size: 1rem; color: var(--text-primary); margin-bottom: 0.8rem;">Chu Giai & Thong Ke Diem Anh:</div>

                      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem; padding: 0.4rem 0.6rem; background: rgba(34, 197, 94, 0.12); border-left: 4px solid #059669; border-radius: 4px;">
                        <span><b style="color: #059669;">Dung Chuan (True Positive - TP):</b></span>
                        <span style="font-family: 'JetBrains Mono'; font-weight: bold; color: var(--text-primary);">{tp_px:,} px</span>
                      </div>

                      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem; padding: 0.4rem 0.6rem; background: rgba(239, 68, 68, 0.12); border-left: 4px solid #dc2626; border-radius: 4px;">
                        <span><b style="color: #dc2626;">Bao Nham (False Positive - FP):</b></span>
                        <span style="font-family: 'JetBrains Mono'; font-weight: bold; color: var(--text-primary);">{fp_px:,} px</span>
                      </div>

                      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; padding: 0.4rem 0.6rem; background: rgba(245, 158, 11, 0.12); border-left: 4px solid #d97706; border-radius: 4px;">
                        <span><b style="color: #d97706;">Bo Sot (False Negative - FN):</b></span>
                        <span style="font-family: 'JetBrains Mono'; font-weight: bold; color: var(--text-primary);">{fn_px:,} px</span>
                      </div>

                      <div style="font-size: 0.85rem; color: var(--text-secondary); border-top: 1px solid var(--border-color); padding-top: 0.8rem; line-height: 1.6;">
                        - <b>Do nhay (Sensitivity / Recall):</b> <span style="color: #0284c7; font-weight: bold;">{sens*100:.2f}%</span><br>
                        - <b>Do dac hieu (Specificity):</b> <span style="color: #059669; font-weight: bold;">{spec*100:.2f}%</span><br>
                        - <b>Dice Similarity:</b> <span style="color: #0284c7; font-weight: bold;">{diag_primary.dice_score:.4f}</span>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # =========================================================================
    # 9. KHU VUC XUAT HO SO CHAN DOAN VA TAI BAO CAO
    # =========================================================================

    st.markdown("---")
    st.markdown(
        "<div class='section-heading' style='font-size: 1rem;'>Ho So Chan Doan & Xuat Bao Cao Y Khoa</div>",
        unsafe_allow_html=True,
    )

    report_csv = io.StringIO()
    writer = csv.writer(report_csv)
    writer.writerow((
        "Ma_Ca_Chup",
        "Thuat_Toan",
        "Trang_Thai_Phat_Hien",
        "Dien_Tich_U_px",
        "Dien_Tich_Nao_px",
        "Ty_Le_U_Nao_Percent",
        "Do_Tron_Circularity",
        "Diem_Dice",
        "Diem_IoU",
        "Do_Tre_ms",
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
            "Tai Bao Cao Chan Doan CSV",
            data=report_csv.getvalue().encode("utf-8-sig"),
            file_name=f"NeuroScan_Report_{sample_id or 'MRI'}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with down_col2:
        st.caption(f"Ho so ma ca: {sample_id} | Phuong phap: {primary_method_key} | Trang thai xac thuc: PASSED")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: var(--text-muted); font-size: 0.8rem; padding: 1rem 0;'>
      Do an Hoc phan Xu ly anh so (0101006276) - Bo mon Khoa hoc Du lieu - Khoa CNTT - Truong DH Cong Thuong TP.HCM (HUIT).<br>
      <i>San pham phuc vu nghien cuu khoa hoc va minh chung do an. Khong dung thay the chi dinh y te chinh thuc.</i>
    </div>
    """,
    unsafe_allow_html=True,
)
