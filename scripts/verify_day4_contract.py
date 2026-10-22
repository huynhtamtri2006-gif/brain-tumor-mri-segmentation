"""Kịch bản kiểm chuẩn hợp đồng kỹ thuật Ngày 4 — Hà Mạnh Trường & Huỳnh Tâm Trí.

Nội dung nghiệm thu:
1. Seeded Region Growing (find_seed_point, segment_region_growing, RegionGrowingSegmenter)
2. Bộ điều phối trung tâm BrainTumorPipeline 4 tầng DIP
3. Bộ unit tests tests/test_segmentation.py và tests/test_pipeline.py
4. Notebook 03: So sánh đối chứng Watershed vs. Region Growing
5. Cập nhật checklist Ngày 4 trong NHIEM_VU_HA_MANH_TRUONG.md và Ngày 3 + 4 trong NHIEM_VU_HUYNH_TAM_TRI.md

Sử dụng:
    python scripts/verify_day4_contract.py
"""

from __future__ import annotations

import inspect
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.preprocessing.skull_strip import strip_skull
from src.segmentation.region_growing import (
    RegionGrowingSegmenter,
    find_seed_point,
    segment_region_growing,
)
from src.pipeline import BrainTumorPipeline
from src.measurement.features import DiagnosticResult

CONFIG_PATH = REPO_ROOT / "configs" / "default_params.yaml"
TASK_DOC_TRUONG = REPO_ROOT / "docs" / "NHIEM_VU_HA_MANH_TRUONG.md"
TASK_DOC_TRI = REPO_ROOT / "docs" / "NHIEM_VU_HUYNH_TAM_TRI.md"
NOTEBOOK_03_PATH = REPO_ROOT / "notebooks" / "03_tumor_segmentation_comparison.ipynb"
SAMPLE_IMAGE = REPO_ROOT / "data" / "full" / "images" / "TCGA_CS_4941_19960909_13.png"
SAMPLE_MASK = REPO_ROOT / "data" / "full" / "masks" / "TCGA_CS_4941_19960909_13_mask.png"


@dataclass
class Check:
    group: str
    name: str
    ok: bool
    detail: str


# =============================================================================
# 1. CẤU HÌNH YAML
# =============================================================================

def check_config(checks: List[Check]) -> None:
    try:
        raw = CONFIG_PATH.read_text(encoding="utf-8")
        cfg = yaml.safe_load(raw)
        checks.append(Check("CFG", "Nạp YAML (encoding=utf-8)", True, str(CONFIG_PATH.relative_to(REPO_ROOT))))
    except Exception as exc:
        checks.append(Check("CFG", "Nạp YAML (encoding=utf-8)", False, str(exc)))
        return

    rg = cfg.get("segmentation", {}).get("region_growing", {})
    ok_rg = (
        rg.get("intensity_tolerance") == 15
        and rg.get("min_tumor_area") == 50
        and rg.get("max_tumor_area") == 25000
    )
    checks.append(Check(
        "CFG", "segmentation.region_growing", ok_rg,
        f"tolerance={rg.get('intensity_tolerance')}, min_area={rg.get('min_tumor_area')}, max_area={rg.get('max_tumor_area')}"
    ))

    ws = cfg.get("segmentation", {}).get("watershed", {})
    ok_ws = ws.get("dist_thresh_ratio") == 0.4 and ws.get("bg_dilate_kernel") == 3
    checks.append(Check(
        "CFG", "segmentation.watershed", ok_ws,
        f"dist_thresh_ratio={ws.get('dist_thresh_ratio')}, bg_dilate_kernel={ws.get('bg_dilate_kernel')}"
    ))


# =============================================================================
# 2. CHỮ KÝ HÀM (SIGNATURE CONTRACT)
# =============================================================================

_REQUIRED = object()


import typing

def _canonical(annotation: Any) -> str:
    if annotation is inspect.Parameter.empty or annotation is inspect.Signature.empty:
        return ""
    if annotation is None or annotation is type(None):
        return "None"
    if isinstance(annotation, str):
        return annotation
    origin = typing.get_origin(annotation)
    args = typing.get_args(annotation)
    if origin is typing.Union:
        if len(args) == 2 and type(None) in args:
            inner = args[0] if args[1] is type(None) else args[1]
            return f"Optional[{_canonical(inner)}]"
        return "Union[" + ", ".join(_canonical(a) for a in args) + "]"
    if origin is not None:
        prefix = {tuple: "Tuple", dict: "Dict", list: "List", set: "Set"}.get(
            origin, getattr(origin, "__name__", str(origin))
        )
        return f"{prefix}[" + ", ".join(_canonical(a) for a in args) + "]"
    if annotation is np.ndarray:
        return "np.ndarray"
    if annotation is typing.Any:
        return "Any"
    return getattr(annotation, "__name__", str(annotation))


def _render_signature(sig: inspect.Signature) -> str:
    parts = []
    for p in sig.parameters.values():
        canon = _canonical(p.annotation)
        text = f"{p.name}: {canon}" if canon else p.name
        if p.default is not inspect.Parameter.empty:
            text += f" = {p.default!r}"
        parts.append(text)
    ret = _canonical(sig.return_annotation)
    return f"({', '.join(parts)}) -> {ret}" if ret else f"({', '.join(parts)})"


def check_signatures(checks: List[Check]) -> None:
    signature_specs = [
        ("find_seed_point", find_seed_point, [("brain_image", _REQUIRED)], "Optional[Tuple[int, int]]"),
        (
            "segment_region_growing",
            segment_region_growing,
            [
                ("brain_image", _REQUIRED),
                ("tolerance", 15),
                ("seed_point", None),
                ("min_area", 50),
                ("max_area", 25000),
            ],
            "np.ndarray",
        ),
        (
            "RegionGrowingSegmenter.__init__",
            RegionGrowingSegmenter.__init__,
            [
                ("self", _REQUIRED),
                ("tolerance", 15),
                ("min_area", 50),
                ("max_area", 25000),
            ],
            "None",
        ),
        (
            "RegionGrowingSegmenter.segment",
            RegionGrowingSegmenter.segment,
            [
                ("self", _REQUIRED),
                ("brain_image", _REQUIRED),
            ],
            "np.ndarray",
        ),
        (
            "BrainTumorPipeline.__init__",
            BrainTumorPipeline.__init__,
            [
                ("self", _REQUIRED),
                ("method", "watershed"),
                ("params", None),
            ],
            "None",
        ),
        (
            "BrainTumorPipeline.process",
            BrainTumorPipeline.process,
            [
                ("self", _REQUIRED),
                ("image", _REQUIRED),
                ("gt_mask", None),
            ],
            "Tuple[DiagnosticResult, Dict[str, np.ndarray]]",
        ),
    ]

    for label, function, expected_params, expected_return in signature_specs:
        sig = inspect.signature(function)
        params = list(sig.parameters.values())
        problems: List[str] = []

        if len(params) != len(expected_params):
            problems.append(f"{len(params)} tham số (kỳ vọng {len(expected_params)})")
        for actual, (name, default) in zip(params, expected_params):
            if actual.name != name:
                problems.append(f"tham số '{actual.name}' thay vì '{name}'")
                continue
            if default is _REQUIRED:
                if actual.default is not inspect.Parameter.empty:
                    problems.append(f"'{name}' không được có giá trị mặc định")
            elif actual.default != default:
                problems.append(f"'{name}' mặc định {actual.default!r} thay vì {default!r}")

        actual_return = _canonical(sig.return_annotation)
        if actual_return != expected_return:
            problems.append(f"trả về {actual_return or '<empty>'} thay vì {expected_return}")

        checks.append(Check(
            "SIG", label, not problems,
            "; ".join(problems) if problems else f"{label}{_render_signature(sig)}"
        ))


# =============================================================================
# 3. BẤT BIẾN TOÁN HỌC & TƯƠNG THÍCH NGƯỢC
# =============================================================================

def check_region_growing_invariants(checks: List[Check]) -> None:
    img = cv2.imread(str(SAMPLE_IMAGE), cv2.IMREAD_GRAYSCALE)
    if img is None:
        checks.append(Check("INV", "Nạp ảnh mẫu", False, f"Không đọc được {SAMPLE_IMAGE}"))
        return

    stripped, brain_mask = strip_skull(img)
    checks.append(Check("INV", "Nạp ảnh & tách sọ", stripped.shape == (256, 256), f"shape={stripped.shape}"))

    # Kiểm tra find_seed_point
    seed = find_seed_point(stripped)
    seed_ok = seed is not None and 0 <= seed[0] < stripped.shape[0] and 0 <= seed[1] < stripped.shape[1]
    seed_in_brain = seed_ok and brain_mask[seed[0], seed[1]] > 0
    checks.append(Check(
        "INV", "find_seed_point nằm trong nhu mô não",
        seed_in_brain,
        f"seed={seed} • brain_mask={brain_mask[seed[0], seed[1]] if seed_ok else 'N/A'}"
    ))

    # Kiểm tra segment_region_growing
    mask = segment_region_growing(stripped, tolerance=15)
    mask_ok = (
        isinstance(mask, np.ndarray) and mask.shape == stripped.shape
        and mask.dtype == np.uint8 and set(np.unique(mask).tolist()).issubset({0, 255})
    )
    checks.append(Check(
        "BC", "segment_region_growing() trả mask 2D chuẩn",
        mask_ok,
        f"shape={mask.shape} • dtype={mask.dtype} • values={sorted(np.unique(mask).tolist())}"
    ))

    # Đối sánh hàm tự do và class đối tượng
    class_mask = RegionGrowingSegmenter(tolerance=15).segment(stripped)
    match_ok = np.array_equal(mask, class_mask)
    checks.append(Check(
        "BC", "RegionGrowingSegmenter.segment() khớp hàm tự do",
        match_ok,
        "100% pixel trùng khớp giữa class và hàm tự do" if match_ok else "Không khớp kết quả"
    ))

    # Bất biến nội não
    outside_brain = int(np.count_nonzero((mask > 0) & (brain_mask == 0)))
    checks.append(Check(
        "INV", "Mặt nạ u nằm trọn trong nội não",
        outside_brain == 0,
        f"{outside_brain} pixel u ngoài nhu mô não"
    ))

    # Fail-safe trên ảnh rỗng toàn 0
    empty_img = np.zeros((256, 256), dtype=np.uint8)
    empty_seed = find_seed_point(empty_img)
    empty_mask = segment_region_growing(empty_img)
    empty_ok = empty_seed is None and np.count_nonzero(empty_mask) == 0 and empty_mask.shape == (256, 256)
    checks.append(Check(
        "INV", "Fail-safe trên ảnh rỗng",
        empty_ok,
        f"seed={empty_seed} • tumor_pixels={np.count_nonzero(empty_mask)}"
    ))


# =============================================================================
# 4. ĐIỀU PHỐI TOÀN TRÌNH BRAINTUMORPIPELINE
# =============================================================================

def check_pipeline(checks: List[Check]) -> None:
    img = cv2.imread(str(SAMPLE_IMAGE), cv2.IMREAD_GRAYSCALE)
    gt = cv2.imread(str(SAMPLE_MASK), cv2.IMREAD_GRAYSCALE) if SAMPLE_MASK.exists() else None

    # Pipeline Watershed
    pipe_ws = BrainTumorPipeline(method="watershed")
    diag_ws, inter_ws = pipe_ws.process(img, gt)
    expected_keys = {"original", "filtered", "stripped", "brain_mask", "tumor_mask", "overlay", "quad"}
    ws_ok = (
        isinstance(diag_ws, DiagnosticResult)
        and set(inter_ws.keys()) == expected_keys
        and inter_ws["quad"].shape == (512, 512, 3)
        and diag_ws.dice_score is not None
        and 0.0 <= diag_ws.dice_score <= 1.0
    )
    checks.append(Check(
        "PIPE", "BrainTumorPipeline (Watershed)",
        ws_ok,
        f"Dice={diag_ws.dice_score:.4f} • IoU={diag_ws.iou_score:.4f} • quad={inter_ws['quad'].shape}"
    ))

    # Pipeline Region Growing
    pipe_rg = BrainTumorPipeline(method="region_growing", params={"intensity_tolerance": 15})
    diag_rg, inter_rg = pipe_rg.process(img, gt)
    rg_ok = (
        isinstance(diag_rg, DiagnosticResult)
        and set(inter_rg.keys()) == expected_keys
        and inter_rg["quad"].shape == (512, 512, 3)
        and diag_rg.dice_score is not None
        and 0.0 <= diag_rg.dice_score <= 1.0
    )
    checks.append(Check(
        "PIPE", "BrainTumorPipeline (Region Growing)",
        rg_ok,
        f"Dice={diag_rg.dice_score:.4f} • IoU={diag_rg.iou_score:.4f} • quad={inter_rg['quad'].shape}"
    ))

    # Pipeline Fail-Safe
    empty = np.zeros((256, 256), dtype=np.uint8)
    d_empty, i_empty = pipe_ws.process(empty)
    empty_ok = not d_empty.tumor_detected and d_empty.tumor_area_px == 0 and np.count_nonzero(i_empty["tumor_mask"]) == 0
    checks.append(Check(
        "PIPE", "BrainTumorPipeline fail-safe ảnh đen",
        empty_ok,
        f"detected={d_empty.tumor_detected} • tumor_area={d_empty.tumor_area_px}px"
    ))


# =============================================================================
# 5. NOTEBOOK 03
# =============================================================================

def check_notebook(checks: List[Check]) -> None:
    if not NOTEBOOK_03_PATH.is_file():
        checks.append(Check("NB", "Notebook 03 tồn tại", False, "không tìm thấy tệp notebook 03"))
        return

    try:
        nb_data = json.loads(NOTEBOOK_03_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        checks.append(Check("NB", "Notebook 03 JSON", False, f"Lỗi đọc JSON: {exc}"))
        return

    code_cells = [c for c in nb_data.get("cells", []) if c.get("cell_type") == "code"]
    executed = [c for c in code_cells if c.get("execution_count") is not None]
    with_output = [c for c in code_cells if c.get("outputs")]
    ok = len(code_cells) >= 3 and len(executed) == len(code_cells) and len(with_output) >= 3
    checks.append(Check(
        "NB", "Notebook 03 đã thực thi đầy đủ",
        ok,
        f"{len(executed)}/{len(code_cells)} code cells đã chạy • {len(with_output)} cell có output"
    ))


# =============================================================================
# 6. CHECKLIST TÀI LIỆU
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
        day4 = sec_truong.get(4, "")
        d4_checked = day4.count("- [x]")
        d4_unchecked = day4.count("- [ ]")
        checks.append(Check(
            "DOC", "HMT Ngày 4: 3 [x] • 0 [ ]",
            d4_checked == 3 and d4_unchecked == 0,
            f"{d4_checked} [x] • {d4_unchecked} [ ]"
        ))

        earlier_truong = [sec_truong[d] for d in (1, 2, 3, 4) if d in sec_truong]
        tot_earlier = sum(s.count("- [x]") for s in earlier_truong)
        checks.append(Check(
            "DOC", "HMT Ngày 1–4: 12 [x] không hồi quy",
            tot_earlier == 12,
            f"{tot_earlier}/12 [x]"
        ))

        tot_checked = text_truong.count("- [x]")
        tot_unchecked = text_truong.count("- [ ]")
        checks.append(Check(
            "DOC", "HMT Tổng 20 ô checklist (>= 12 [x])",
            tot_checked + tot_unchecked == 20 and tot_checked >= 12,
            f"{tot_checked} [x] • {tot_unchecked} [ ]"
        ))

    # 2. Huỳnh Tâm Trí
    if not TASK_DOC_TRI.is_file():
        checks.append(Check("DOC", "Tài liệu Huỳnh Tâm Trí", False, "không tìm thấy tệp"))
    else:
        text_tri = TASK_DOC_TRI.read_text(encoding="utf-8")
        sec_tri = _parse_sections(text_tri)

        # Ngày 3 Trí (3 ô)
        day3 = sec_tri.get(3, "")
        d3_checked = day3.count("- [x]")
        d3_unchecked = day3.count("- [ ]")
        checks.append(Check(
            "DOC", "HTT Ngày 3: 3 [x] • 0 [ ]",
            d3_checked == 3 and d3_unchecked == 0,
            f"{d3_checked} [x] • {d3_unchecked} [ ]"
        ))

        # Ngày 4 Trí (2 ô)
        day4 = sec_tri.get(4, "")
        d4_checked = day4.count("- [x]")
        d4_unchecked = day4.count("- [ ]")
        checks.append(Check(
            "DOC", "HTT Ngày 4: 2 [x] • 0 [ ]",
            d4_checked == 2 and d4_unchecked == 0,
            f"{d4_checked} [x] • {d4_unchecked} [ ]"
        ))

        earlier_tri = [sec_tri[d] for d in (1, 2, 3, 4) if d in sec_tri]
        tot_earlier_tri = sum(s.count("- [x]") for s in earlier_tri)
        checks.append(Check(
            "DOC", "HTT Ngày 1–4: 11 [x] không hồi quy",
            tot_earlier_tri == 11,
            f"{tot_earlier_tri}/11 [x]"
        ))

        tot_checked_tri = text_tri.count("- [x]")
        tot_unchecked_tri = text_tri.count("- [ ]")
        checks.append(Check(
            "DOC", "HTT Tổng 19 ô checklist (>= 11 [x])",
            tot_checked_tri + tot_unchecked_tri == 19 and tot_checked_tri >= 11,
            f"{tot_checked_tri} [x] • {tot_unchecked_tri} [ ]"
        ))


# =============================================================================
# 7. BÁO CÁO & MAIN
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
        "CFG": "Cấu hình YAML",
        "SIG": "Chữ ký hàm",
        "BC": "Tương thích ngược",
        "INV": "Bất biến & fail-safe",
        "PIPE": "Điều phối toàn trình Pipeline",
        "NB": "Thực thi Notebook 03",
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
    print("KIỂM CHUẨN HỢP ĐỒNG KỸ THUẬT NGÀY 4 — HÀ MẠNH TRƯỜNG & HUỲNH TÂM TRÍ")
    print("Seeded Region Growing • BrainTumorPipeline • Đánh Giá Đối Chứng & Notebook 03")
    print("=" * 80)
    print()

    check_config(checks)
    check_signatures(checks)
    check_region_growing_invariants(checks)
    check_pipeline(checks)
    check_notebook(checks)
    check_docs(checks)

    render_report(checks)

    failed = [c for c in checks if not c.ok]
    print()
    if failed:
        print(f"KẾT LUẬN: CÓ {len(failed)} MỤC CHƯA ĐẠT:")
        for f in failed:
            print(f"  - [{f.group}] {f.name}: {f.detail}")
        return 1

    print("KẾT LUẬN: ĐẠT — toàn bộ hợp đồng kỹ thuật Ngày 4 được xác minh thành công.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
