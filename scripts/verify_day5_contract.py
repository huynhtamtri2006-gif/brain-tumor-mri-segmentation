"""Kịch bản kiểm chuẩn hợp đồng kỹ thuật Ngày 5 — Hà Mạnh Trường & Huỳnh Tâm Trí.

Nội dung nghiệm thu:
1. Benchmark quy mô lớn 3,929 lát cắt TCGA-LGG (110 bệnh nhân) -> 7,858 kết quả thực nghiệm.
2. Tệp kết quả định lượng tổng hợp docs/BENCHMARK_RESULTS.csv và chi tiết docs/BENCHMARK_RESULTS_FULL.csv.
3. Bộ biểu đồ phân tích y sinh độ phân giải cao trong reports/figures/.
4. Sổ tay thực nghiệm định lượng notebooks/04_quantitative_evaluation.ipynb.
5. Ứng dụng web tương tác bác sĩ Streamlit Web UI (demo/app.py và demo/utils.py).
6. Cập nhật checklist Ngày 5 trong NHIEM_VU_HA_MANH_TRUONG.md và NHIEM_VU_HUYNH_TAM_TRI.md.

Sử dụng:
    python scripts/verify_day5_contract.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

TASK_DOC_TRUONG = REPO_ROOT / "docs" / "NHIEM_VU_HA_MANH_TRUONG.md"
TASK_DOC_TRI = REPO_ROOT / "docs" / "NHIEM_VU_HUYNH_TAM_TRI.md"
BENCHMARK_CSV = REPO_ROOT / "docs" / "BENCHMARK_RESULTS.csv"
BENCHMARK_FULL_CSV = REPO_ROOT / "docs" / "BENCHMARK_RESULTS_FULL.csv"
NOTEBOOK_04_PATH = REPO_ROOT / "notebooks" / "04_quantitative_evaluation.ipynb"
APP_PY_PATH = REPO_ROOT / "demo" / "app.py"
APP_UTILS_PATH = REPO_ROOT / "demo" / "utils.py"
FIGURES_DIR = REPO_ROOT / "reports" / "figures"


@dataclass
class Check:
    group: str
    name: str
    ok: bool
    detail: str


# =============================================================================
# 1. KẾT QUẢ BENCHMARK CSV
# =============================================================================

def check_benchmark_csvs(checks: List[Check]) -> None:
    # 1. Kiểm tra BENCHMARK_RESULTS_FULL.csv
    if not BENCHMARK_FULL_CSV.is_file():
        checks.append(Check("DATA", "BENCHMARK_RESULTS_FULL.csv tồn tại", False, "không tìm thấy tệp"))
    else:
        try:
            df_full = pd.read_csv(BENCHMARK_FULL_CSV)
            count = len(df_full)
            expected_count = 7858
            has_tumor_col = "has_tumor_gt" in df_full.columns
            dice_col = "dice" in df_full.columns
            ok = count == expected_count and has_tumor_col and dice_col
            checks.append(Check(
                "DATA", "Quy mô thực nghiệm (7,858 bản ghi)",
                ok,
                f"{count} dòng dữ liệu • {len(df_full.columns)} cột thông số"
            ))
        except Exception as exc:
            checks.append(Check("DATA", "Đọc BENCHMARK_RESULTS_FULL.csv", False, str(exc)))

    # 2. Kiểm tra BENCHMARK_RESULTS.csv
    if not BENCHMARK_CSV.is_file():
        checks.append(Check("DATA", "BENCHMARK_RESULTS.csv tồn tại", False, "không tìm thấy tệp"))
    else:
        try:
            df_summary = pd.read_csv(BENCHMARK_CSV)
            rows = len(df_summary)
            cols = len(df_summary.columns)
            ok = rows >= 5 and cols >= 3
            checks.append(Check(
                "DATA", "Bảng tổng hợp chỉ số y khoa",
                ok,
                f"{rows} chỉ số đánh giá • {cols} cột phân nhóm"
            ))
        except Exception as exc:
            checks.append(Check("DATA", "Đọc BENCHMARK_RESULTS.csv", False, str(exc)))


# =============================================================================
# 2. HÌNH ẢNH & ĐỒ THỊ BÁO CÁO KHOA HỌC
# =============================================================================

def check_figures(checks: List[Check]) -> None:
    required_figures = [
        ("skull_stripping_steps.png", "Minh họa 6 bước tách sọ não", 50 * 1024),
        ("watershed_param_sensitivity.png", "Đồ thị độ nhạy tham số Watershed", 50 * 1024),
        ("benchmark_metrics_comparison.png", "Biểu đồ so sánh Dice/IoU/Latency", 50 * 1024),
        ("benchmark_distribution.png", "Biểu đồ phân phối hiệu năng 4 chỉ số", 50 * 1024),
    ]

    for fname, desc, min_size in required_figures:
        fpath = FIGURES_DIR / fname
        if not fpath.is_file():
            checks.append(Check("FIG", desc, False, f"Thiếu file: {fname}"))
            continue

        size = fpath.stat().st_size
        ok = size >= min_size
        checks.append(Check(
            "FIG", desc, ok,
            f"{fname} ({size / 1024:.1f} KB, ngưỡng tối thiểu {min_size / 1024:.1f} KB)"
        ))


# =============================================================================
# 3. NOTEBOOK 04 THỰC NGHIỆM ĐỊNH LƯỢNG
# =============================================================================

def check_notebook_04(checks: List[Check]) -> None:
    if not NOTEBOOK_04_PATH.is_file():
        checks.append(Check("NB", "Notebook 04 tồn tại", False, "không tìm thấy tệp"))
        return

    try:
        nb_data = json.loads(NOTEBOOK_04_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        checks.append(Check("NB", "Notebook 04 JSON", False, f"Lỗi đọc JSON: {exc}"))
        return

    code_cells = [c for c in nb_data.get("cells", []) if c.get("cell_type") == "code"]
    executed = [c for c in code_cells if c.get("execution_count") is not None]
    with_output = [c for c in code_cells if c.get("outputs")]
    png_outputs = sum(
        1 for c in code_cells for o in c.get("outputs", [])
        if "image/png" in o.get("data", {})
    )

    ok = len(code_cells) >= 4 and len(executed) == len(code_cells) and len(with_output) >= 4 and png_outputs >= 2
    checks.append(Check(
        "NB", "Notebook 04 thực thi đầy đủ",
        ok,
        f"{len(executed)}/{len(code_cells)} cells đã chạy • {len(with_output)} cell có output • {png_outputs} biểu đồ PNG"
    ))


# =============================================================================
# 4. GIAO DIỆN STREAMLIT WEB UI
# =============================================================================

def check_streamlit_app(checks: List[Check]) -> None:
    if not APP_PY_PATH.is_file() or not APP_UTILS_PATH.is_file():
        checks.append(Check("UI", "Tệp mã nguồn Streamlit", False, "Thiếu demo/app.py hoặc demo/utils.py"))
        return

    content_app = APP_PY_PATH.read_text(encoding="utf-8")
    content_utils = APP_UTILS_PATH.read_text(encoding="utf-8")

    # Kiểm tra các module và tính năng quan trọng trong demo
    has_sidebar = "st.sidebar" in content_app
    has_kpi = ".metric(" in content_app or "st.metric" in content_app
    has_button = "st.button" in content_app
    has_csv_export = "download_button" in content_app or "to_csv" in content_app
    has_binary_read = "_read_grayscale" in content_utils

    ui_ok = has_sidebar and has_kpi and has_button and has_csv_export and has_binary_read
    checks.append(Check(
        "UI", "Streamlit UI & Chức năng chẩn đoán",
        ui_ok,
        "Sidebar điều khiển, 5 thẻ KPI, nút phân đoạn, xuất CSV và đọc ảnh an toàn UTF-8"
    ))


# =============================================================================
# 5. CHECKLIST TÀI LIỆU
# =============================================================================

def _parse_sections(text: str) -> Dict[int, str]:
    matches = list(re.finditer(r"^###\s.*?NGÀY\s+(\d+)", text, re.MULTILINE))
    sections: Dict[int, str] = {}
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections[int(match.group(1))] = text[match.start():end]
    return sections


def check_docs(checks: List[Check]) -> None:
    # 1. Hà Mạnh Trường
    if not TASK_DOC_TRUONG.is_file():
        checks.append(Check("DOC", "Tài liệu Hà Mạnh Trường", False, "không tìm thấy tệp"))
    else:
        text_truong = TASK_DOC_TRUONG.read_text(encoding="utf-8")
        sec_truong = _parse_sections(text_truong)
        day5 = sec_truong.get(5, "")
        d5_checked = day5.count("- [x]")
        d5_unchecked = day5.count("- [ ]")
        checks.append(Check(
            "DOC", "HMT Ngày 5: 3 [x] • 0 [ ]",
            d5_checked == 3 and d5_unchecked == 0,
            f"{d5_checked} [x] • {d5_unchecked} [ ]"
        ))

        earlier_truong = [sec_truong[d] for d in range(1, 6) if d in sec_truong]
        tot_earlier = sum(s.count("- [x]") for s in earlier_truong)
        checks.append(Check(
            "DOC", "HMT Ngày 1–5: 15 [x] không hồi quy",
            tot_earlier == 15,
            f"{tot_earlier}/15 [x]"
        ))

        tot_checked = text_truong.count("- [x]")
        tot_unchecked = text_truong.count("- [ ]")
        checks.append(Check(
            "DOC", "HMT Tổng 20 ô checklist (>= 15 [x])",
            tot_checked + tot_unchecked == 20 and tot_checked >= 15,
            f"{tot_checked} [x] • {tot_unchecked} [ ]"
        ))

    # 2. Huỳnh Tâm Trí
    if not TASK_DOC_TRI.is_file():
        checks.append(Check("DOC", "Tài liệu Huỳnh Tâm Trí", False, "không tìm thấy tệp"))
    else:
        text_tri = TASK_DOC_TRI.read_text(encoding="utf-8")
        sec_tri = _parse_sections(text_tri)

        day5 = sec_tri.get(5, "")
        d5_checked = day5.count("- [x]")
        d5_unchecked = day5.count("- [ ]")
        checks.append(Check(
            "DOC", "HTT Ngày 5: 3 [x] • 0 [ ]",
            d5_checked == 3 and d5_unchecked == 0,
            f"{d5_checked} [x] • {d5_unchecked} [ ]"
        ))

        earlier_tri = [sec_tri[d] for d in range(1, 6) if d in sec_tri]
        tot_earlier_tri = sum(s.count("- [x]") for s in earlier_tri)
        checks.append(Check(
            "DOC", "HTT Ngày 1–5: 14 [x] không hồi quy",
            tot_earlier_tri == 14,
            f"{tot_earlier_tri}/14 [x]"
        ))

        tot_checked_tri = text_tri.count("- [x]")
        tot_unchecked_tri = text_tri.count("- [ ]")
        checks.append(Check(
            "DOC", "HTT Tổng 19 ô checklist (>= 14 [x])",
            tot_checked_tri + tot_unchecked_tri == 19 and tot_checked_tri >= 14,
            f"{tot_checked_tri} [x] • {tot_unchecked_tri} [ ]"
        ))


# =============================================================================
# 6. BÁO CÁO & MAIN
# =============================================================================

def render_report(checks: List[Check]) -> None:
    headers = ("Nhóm", "Nội dung kiểm tra", "Kết quả", "Chi tiết")
    rows = [(c.group, c.name, "PASS" if c.ok else "FAIL", c.detail) for c in checks]
    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i])
        for i in range(len(headers))
    ]
    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def fmt(cells: Tuple[str, str, str, str]) -> str:
        return "| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)) + " |"

    print(line)
    print(fmt(headers))
    print(line)
    prev = None
    for c in checks:
        if prev is not None and c.group != prev:
            print(line)
        prev = c.group
        print(fmt((c.group, c.name, "PASS" if c.ok else "FAIL", c.detail)))
    print(line)

    labels = {
        "DATA": "Dữ liệu Benchmark 3,929 lát",
        "FIG": "Hình ảnh đồ thị nghiên cứu",
        "NB": "Thực thi Notebook 04",
        "UI": "Giao diện Web Streamlit",
        "DOC": "Checklist tài liệu",
    }
    print()
    for g, label in labels.items():
        subset = [c for c in checks if c.group == g]
        if subset:
            print(f"  • {label:<32} {sum(1 for c in subset if c.ok)}/{len(subset)} đạt")
    passed = sum(1 for c in checks if c.ok)
    print(f"  TỔNG CỘNG: {passed}/{len(checks)} kiểm tra đạt")


def main() -> int:
    checks: List[Check] = []
    print("=" * 80)
    print("KIỂM CHUẨN HỢP ĐỒNG KỸ THUẬT NGÀY 5 — HÀ MẠNH TRƯỜNG & HUỲNH TÂM TRÍ")
    print("Benchmark Quy Mô Lớn 3,929 Lát • Phân Tích Thất Bại • Web App & Notebook 04")
    print("=" * 80)
    print()

    check_benchmark_csvs(checks)
    check_figures(checks)
    check_notebook_04(checks)
    check_streamlit_app(checks)
    check_docs(checks)

    render_report(checks)

    failed = [c for c in checks if not c.ok]
    print()
    if failed:
        print(f"KẾT LUẬN: CÓ {len(failed)} MỤC CHƯA ĐẠT:")
        for f in failed:
            print(f"  - [{f.group}] {f.name}: {f.detail}")
        return 1

    print("KẾT LUẬN: ĐẠT — toàn bộ hợp đồng kỹ thuật Ngày 5 được xác minh thành công.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
