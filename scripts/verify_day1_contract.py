#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm chuẩn tự động Hợp đồng Kỹ thuật Ngày 1 — Hà Mạnh Trường (2045240326).

Script xác minh 100% các cam kết kỹ thuật của Ngày 1:
  1. Cấu hình `configs/default_params.yaml` đầy đủ khoá tham số (nạp UTF-8).
  2. 13 chữ ký hàm trong `src/` khớp bảng đặc tả `docs/SPEC_PIPELINE_MRI.md` §4.
  3. 7 bất biến dữ liệu I1–I7 của đặc tả §5.1 (kèm các kiểm tra riêng của
     nhiệm vụ Ngày 1: diện tích/độ tròn và ca ảnh rỗng không chia cho 0).

Chạy từ thư mục gốc repo:

    python scripts/verify_day1_contract.py

Mã thoát: 0 nếu toàn bộ kiểm tra đạt, 1 nếu có bất kỳ mục nào thất bại.
"""

from __future__ import annotations

import importlib
import inspect
import sys
import typing
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
import yaml

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover - môi trường không hỗ trợ reconfigure
        pass

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Ảnh mẫu mà nhiệm vụ chỉ định; tự động lùi về bộ dữ liệu đầy đủ nếu thiếu.
SAMPLE_IMAGE_NAME = "TCGA_CS_4941_19960909_1.png"
TARGET_SHAPE = (256, 256)

_REQUIRED = object()  # Đánh dấu tham số bắt buộc (không có giá trị mặc định).


# =============================================================================
# 1. KIỂM TRA CẤU HÌNH YAML
# =============================================================================

# Khoá YAML -> danh sách tham số bắt buộc phải có.
REQUIRED_CONFIG: Dict[str, List[str]] = {
    "preprocessing.bilateral_filter": ["d", "sigma_color", "sigma_space"],
    "preprocessing.clahe": ["clip_limit", "tile_grid_size"],
    "preprocessing.skull_strip": ["kernel_size", "morph_iterations"],
    "segmentation.watershed": ["dist_thresh_ratio", "bg_dilate_kernel"],
    "segmentation.region_growing": [
        "intensity_tolerance",
        "min_tumor_area",
        "max_tumor_area",
    ],
    "measurement": ["min_contour_area", "bbox_color", "bbox_thickness"],
}

# Tên khoá thực tế trong YAML khi khác tên gọi trong nhiệm vụ.
CONFIG_KEY_ALIASES: Dict[str, str] = {
    "preprocessing.skull_strip": "preprocessing.skull_stripping",
}


def _lookup(node: Any, dotted: str) -> Tuple[bool, Any]:
    """Đi theo đường dẫn phân cấp `a.b.c` trong cây dict."""
    current = node
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


def check_config(path: Path, checks: List["Check"]) -> None:
    """Nạp YAML bằng UTF-8 và xác minh đủ 6 nhóm khoá tham số."""
    group = "CFG"

    if not path.is_file():
        checks.append(Check(group, "Nạp YAML", False, f"không tìm thấy {path.relative_to(ROOT)}"))
        return

    try:
        with path.open("r", encoding="utf-8") as fh:
            config = yaml.safe_load(fh)
    except Exception as exc:  # noqa: BLE001 - báo lỗi cụ thể cho người chạy
        checks.append(Check(group, "Nạp YAML", False, f"{type(exc).__name__}: {exc}"))
        return

    checks.append(Check(group, "Nạp YAML (encoding=utf-8)", isinstance(config, dict),
                        f"{path.relative_to(ROOT)} • {len(config)} nhánh gốc"))

    for canonical_key, params in REQUIRED_CONFIG.items():
        lookup_key = CONFIG_KEY_ALIASES.get(canonical_key, canonical_key)
        found, node = _lookup(config, lookup_key)
        if not found:
            checks.append(Check(group, canonical_key, False, f"thiếu nhánh '{lookup_key}'"))
            continue

        missing = [p for p in params if not isinstance(node, dict) or p not in node]
        if missing:
            checks.append(Check(group, canonical_key, False, "thiếu khoá: " + ", ".join(missing)))
            continue

        rendered = ", ".join(f"{p}={node[p]!r}" for p in params)
        detail = rendered
        if lookup_key != canonical_key:
            detail += f" (khoá thực tế: {lookup_key})"
        checks.append(Check(group, canonical_key, True, detail))


# =============================================================================
# 2. KIỂM TRA 13 CHỮ KÝ HÀM
# =============================================================================

# Mỗi mục: (tên trong nhiệm vụ, module, đường dẫn định vị, tên thay thế,
#           tham số, kiểu trả về).
# Tham số: (tên, giá trị mặc định) — _REQUIRED nghĩa là bắt buộc.
SIGNATURE_CONTRACT = [
    (
        "apply_bilateral_filter", "src.preprocessing.filters", "apply_bilateral_filter", (),
        [("image", _REQUIRED), ("d", 9), ("sigma_color", 75.0), ("sigma_space", 75.0)],
        "np.ndarray",
    ),
    (
        "apply_clahe", "src.preprocessing.filters", "apply_clahe", (),
        [("image", _REQUIRED), ("clip_limit", 2.0), ("tile_grid_size", (8, 8))],
        "np.ndarray",
    ),
    (
        # Đặc tả §4.3 đặt tên hàm là strip_skull; nhiệm vụ Ngày 1 gọi là
        # apply_skull_stripping. Chấp nhận cả hai tên, ưu tiên tên nhiệm vụ.
        "apply_skull_stripping", "src.preprocessing.skull_strip",
        "apply_skull_stripping", ("strip_skull",),
        [("image", _REQUIRED), ("brain_mask", None), ("return_intermediates", False)],
        "Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, np.ndarray]]]",
    ),
    (
        "extract_brain_mask", "src.preprocessing.skull_strip", "extract_brain_mask", (),
        [("image", _REQUIRED), ("kernel_size", 5), ("return_intermediates", False)],
        "Union[np.ndarray, Tuple[np.ndarray, Dict[str, np.ndarray]]]",
    ),
    (
        "WatershedSegmenter.segment", "src.segmentation.watershed", "WatershedSegmenter.segment", (),
        [("self", _REQUIRED), ("brain_image", _REQUIRED)],
        "np.ndarray",
    ),
    (
        "find_seed_point", "src.segmentation.region_growing", "find_seed_point", (),
        [("brain_image", _REQUIRED)],
        "Optional[Tuple[int, int]]",
    ),
    (
        "RegionGrowingSegmenter.segment", "src.segmentation.region_growing",
        "RegionGrowingSegmenter.segment", (),
        [("self", _REQUIRED), ("brain_image", _REQUIRED)],
        "np.ndarray",
    ),
    (
        "calculate_circularity", "src.measurement.features", "calculate_circularity", (),
        [("area", _REQUIRED), ("perimeter", _REQUIRED)],
        "float",
    ),
    (
        "extract_tumor_features", "src.measurement.features", "extract_tumor_features", (),
        [("tumor_mask", _REQUIRED), ("brain_mask", None), ("min_area_thresh", 30)],
        "DiagnosticResult",
    ),
    (
        "draw_tumor_overlay", "src.measurement.visualization", "draw_tumor_overlay", (),
        [
            ("original_image", _REQUIRED), ("tumor_mask", _REQUIRED), ("result", _REQUIRED),
            ("color_bgr", (0, 0, 255)), ("thickness", 2),
        ],
        "np.ndarray",
    ),
    (
        "create_comparison_quad", "src.measurement.visualization", "create_comparison_quad", (),
        [("original", _REQUIRED), ("stripped", _REQUIRED), ("pred_mask", _REQUIRED),
         ("annotated", _REQUIRED)],
        "np.ndarray",
    ),
    (
        "calculate_all_metrics", "src.evaluation.metrics", "calculate_all_metrics", (),
        [("pred_mask", _REQUIRED), ("gt_mask", _REQUIRED)],
        "Dict[str, float]",
    ),
    (
        "BrainTumorPipeline.process", "src.pipeline", "BrainTumorPipeline.process", (),
        [("self", _REQUIRED), ("image", _REQUIRED), ("gt_mask", None)],
        "Tuple[DiagnosticResult, Dict[str, np.ndarray]]",
    ),
]


def _canonical(annotation: Any) -> str:
    """Chuẩn hoá annotation về chuỗi so sánh được với đặc tả."""
    if annotation is inspect.Parameter.empty or annotation is inspect.Signature.empty:
        return ""
    if annotation is type(None):
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


def _render_signature(signature: inspect.Signature) -> str:
    """Hiển thị chữ ký gọn theo tên chuẩn hoá (np.ndarray, DiagnosticResult...)."""
    parts: List[str] = []
    for param in signature.parameters.values():
        text = param.name
        annotation = _canonical(param.annotation)
        if annotation:
            text += f": {annotation}"
        if param.default is not inspect.Parameter.empty:
            text += f" = {param.default!r}"
        parts.append(text)
    rendered = "(" + ", ".join(parts) + ")"
    returns = _canonical(signature.return_annotation)
    return f"{rendered} -> {returns}" if returns else rendered


def _resolve_locator(module: Any, locator: str) -> Optional[Any]:
    """Lấy thành viên theo đường dẫn `Lớp.phương_thức` hoặc `hàm`."""
    current = module
    for name in locator.split("."):
        if not hasattr(current, name):
            return None
        current = getattr(current, name)
    return current


def check_signatures(checks: List["Check"]) -> None:
    """Đối chiếu 13 chữ ký hàm với đặc tả §4."""
    group = "SIG"

    for label, module_name, locator, aliases, expected_params, expected_return in SIGNATURE_CONTRACT:
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001
            checks.append(Check(group, label, False, f"import {module_name} lỗi: {exc}"))
            continue

        resolved_locator = locator
        target = _resolve_locator(module, locator)
        if target is None:
            for alias in aliases:
                target = _resolve_locator(module, alias)
                if target is not None:
                    resolved_locator = alias
                    break

        if target is None:
            checks.append(Check(group, label, False, "không tìm thấy trong " + module_name))
            continue

        try:
            signature = inspect.signature(target)
        except (TypeError, ValueError) as exc:
            checks.append(Check(group, label, False, f"inspect.signature lỗi: {exc}"))
            continue

        params = list(signature.parameters.values())
        problems: List[str] = []

        if len(params) != len(expected_params):
            problems.append(f"{len(params)} tham số (đặc tả {len(expected_params)})")

        for actual, (name, default) in zip(params, expected_params):
            if actual.name != name:
                problems.append(f"tham số '{actual.name}' thay vì '{name}'")
                continue
            if actual.kind is not inspect.Parameter.POSITIONAL_OR_KEYWORD:
                problems.append(f"'{name}' không phải positional-or-keyword")
            if default is _REQUIRED:
                if actual.default is not inspect.Parameter.empty:
                    problems.append(f"'{name}' không được có giá trị mặc định")
            elif actual.default != default:
                problems.append(f"'{name}' mặc định {actual.default!r} thay vì {default!r}")

        actual_return = _canonical(signature.return_annotation)
        if actual_return != expected_return:
            problems.append(f"trả về {actual_return or '<empty>'} thay vì {expected_return}")

        detail = f"{resolved_locator}{_render_signature(signature)}"
        if resolved_locator != label:
            detail += f" (alias của '{label}')"
        if problems:
            checks.append(Check(group, label, False, "; ".join(problems)))
        else:
            checks.append(Check(group, label, True, detail))


# =============================================================================
# 3. KIỂM TRA 7 BẤT BIẾN DỮ LIỆU I1–I7
# =============================================================================

@dataclass
class Check:
    """Một dòng kết quả kiểm tra."""

    group: str
    name: str
    ok: bool
    detail: str


def resolve_sample_image() -> Tuple[Optional[Path], str]:
    """Tìm ảnh mẫu: ưu tiên đường dẫn nhiệm vụ, sau đó bộ dữ liệu đầy đủ."""
    candidates = [
        ROOT / "data" / "sample" / "images" / SAMPLE_IMAGE_NAME,
        ROOT / "data" / "full" / "images" / SAMPLE_IMAGE_NAME,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate, str(candidate.relative_to(ROOT))

    sample_dir = ROOT / "data" / "sample" / "images"
    if sample_dir.is_dir():
        for candidate in sorted(sample_dir.glob("*.png")):
            return candidate, str(candidate.relative_to(ROOT))
    return None, "không có ảnh mẫu"


def resolve_gt_mask(image_path: Path) -> Optional[Path]:
    """Suy ra mặt nạ Ground Truth tương ứng với ảnh (nếu có)."""
    candidate = image_path.parent.parent / "masks" / f"{image_path.stem}_mask.png"
    return candidate if candidate.is_file() else None


def _to_bgr(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image.copy()


def check_invariants(checks: List["Check"]) -> None:
    """Chạy pipeline trên ảnh mẫu và ảnh rỗng để xác minh I1–I7."""
    group = "INV"

    from src.evaluation.metrics import calculate_all_metrics
    from src.pipeline import BrainTumorPipeline

    image_path, image_label = resolve_sample_image()
    if image_path is None:
        checks.append(Check(group, "Nạp ảnh mẫu", False, image_label))
        return

    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        checks.append(Check(group, "Nạp ảnh mẫu", False, f"cv2.imread thất bại: {image_label}"))
        return

    checks.append(Check(group, "Nạp ảnh mẫu", image.shape == TARGET_SHAPE,
                        f"{image_label} • shape={image.shape} • dtype={image.dtype}"))

    gt_path = resolve_gt_mask(image_path)
    gt_mask = cv2.imread(str(gt_path), cv2.IMREAD_GRAYSCALE) if gt_path else None

    pipeline = BrainTumorPipeline(method="watershed")
    diag, intermediates = pipeline.process(image, gt_mask)

    # --- I1 + I2: shape (H, W) 256x256 và dtype uint8 cho mọi ảnh/mặt nạ 2D ---
    expected_keys = {"original", "filtered", "stripped", "brain_mask", "tumor_mask", "overlay", "quad"}
    keys_ok = set(intermediates) == expected_keys
    shape_problems: List[str] = []
    for key in ("original", "filtered", "stripped", "brain_mask", "tumor_mask"):
        value = intermediates[key]
        if value.shape != TARGET_SHAPE:
            shape_problems.append(f"{key}.shape={value.shape}")
        if value.dtype != np.uint8:
            shape_problems.append(f"{key}.dtype={value.dtype}")
    checks.append(Check(
        group, "I1–I2: shape (256,256) & dtype uint8",
        not shape_problems and keys_ok,
        "; ".join(shape_problems) if shape_problems else "5 ảnh/mặt nạ 2D đạt • 7 khoá intermediates đủ",
    ))

    # --- I3: mặt nạ nhị phân cứng {0, 255} ---
    binary_ok = True
    binary_detail: List[str] = []
    for key in ("brain_mask", "tumor_mask"):
        values = set(np.unique(intermediates[key]).tolist())
        if not values.issubset({0, 255}):
            binary_ok = False
        binary_detail.append(f"{key}={sorted(values)}")
    checks.append(Check(group, "I3: mặt nạ ⊂ {0, 255}", binary_ok, " • ".join(binary_detail)))

    # --- I3 (nhiệm vụ): diện tích ≥ 0, độ tròn ∈ [0, 1] ---
    circ_ok = diag.tumor_area_px >= 0 and 0.0 <= diag.circularity <= 1.0
    checks.append(Check(
        group, "I3: S ≥ 0 & Circularity ∈ [0,1]", circ_ok,
        f"S={diag.tumor_area_px}px • C={diag.circularity:.4f} • detected={diag.tumor_detected}",
    ))

    # --- I4 (nhiệm vụ) + I6 (đặc tả): Dice/IoU/Sens/Spec ∈ [0, 1] ---
    metric_values: Dict[str, Optional[float]] = {
        "dice": diag.dice_score, "iou": diag.iou_score,
    }
    if gt_mask is not None:
        all_metrics = calculate_all_metrics(intermediates["tumor_mask"], gt_mask)
        metric_values.update(all_metrics)
        metrics_detail = ", ".join(f"{k}={v:.4f}" for k, v in all_metrics.items())
    else:
        metrics_detail = "không có Ground Truth: dice/iou=None (hợp lệ)"
    metric_problems = [
        name for name, value in metric_values.items()
        if value is not None and not (0.0 <= float(value) <= 1.0)
    ]
    checks.append(Check(
        group, "I6: Dice/IoU/Sens/Spec ∈ [0,1]", not metric_problems,
        metrics_detail if not metric_problems else "ngoài miền: " + ", ".join(metric_problems),
    ))

    # --- I4 (đặc tả): stripped ngoài brain_mask phải bằng 0 ---
    outside_ok = bool(np.all(intermediates["stripped"][intermediates["brain_mask"] == 0] == 0))
    checks.append(Check(group, "I4: stripped[brain_mask==0] == 0", outside_ok,
                        f"{int(np.count_nonzero(intermediates['brain_mask']))} px nhu mô não"))

    # --- I5 (đặc tả): overlay (H,W,3), quad (2H,2W,3), uint8 ---
    overlay = intermediates["overlay"]
    quad = intermediates["quad"]
    h, w = TARGET_SHAPE
    layout_ok = (
        overlay.shape == (h, w, 3) and overlay.dtype == np.uint8
        and quad.shape == (2 * h, 2 * w, 3) and quad.dtype == np.uint8
    )
    checks.append(Check(group, "I5: overlay (H,W,3) & quad (2H,2W,3)", layout_ok,
                        f"overlay={overlay.shape}/{overlay.dtype} • quad={quad.shape}/{quad.dtype}"))

    # --- I7: quad chứa đúng 4 ô theo thứ tự Gốc • Tách sọ • Mặt nạ • Khoanh u ---
    # Bỏ 30 hàng đầu vì create_comparison_quad có đóng dấu tiêu đề lên mỗi ô.
    quadrants = [
        ("original", quad[0:h, 0:w]), ("stripped", quad[0:h, w:2 * w]),
        ("tumor_mask", quad[h:2 * h, 0:w]), ("overlay", quad[h:2 * h, w:2 * w]),
    ]
    offsets = 30
    cell_problems = []
    for key, cell in quadrants:
        reference = _to_bgr(intermediates[key])
        if not np.array_equal(cell[offsets:], reference[offsets:]):
            cell_problems.append(key)
    checks.append(Check(
        group, "I7: quad đúng 4 ô theo thứ tự", not cell_problems,
        "Gốc • Tách sọ • Mặt nạ • Khoanh u" if not cell_problems
        else "ô lệch: " + ", ".join(cell_problems),
    ))

    # --- I5 (nhiệm vụ) / §5.2: ảnh rỗng không được ném ZeroDivisionError ---
    empty = np.zeros(TARGET_SHAPE, dtype=np.uint8)
    empty_gt = np.zeros(TARGET_SHAPE, dtype=np.uint8)
    try:
        empty_diag, empty_inter = BrainTumorPipeline(method="watershed").process(empty, empty_gt)
        empty_metrics = calculate_all_metrics(empty_inter["tumor_mask"], empty_gt)
        empty_ok = (
            int(np.count_nonzero(empty_inter["tumor_mask"])) == 0
            and not empty_diag.tumor_detected
            and empty_diag.tumor_area_px == 0
            and all(0.0 <= float(v) <= 1.0 for v in empty_metrics.values())
        )
        empty_detail = (
            "ảnh rỗng → mask 0, detected=False, "
            + ", ".join(f"{k}={v:.1f}" for k, v in empty_metrics.items())
        )
    except ZeroDivisionError as exc:
        empty_ok = False
        empty_detail = f"ZeroDivisionError: {exc}"
    except Exception as exc:  # noqa: BLE001 - mọi ngoại lệ đều vi phạm hợp đồng fail-safe
        empty_ok = False
        empty_detail = f"{type(exc).__name__}: {exc}"
    checks.append(Check(group, "I5: ảnh rỗng không chia cho 0", empty_ok, empty_detail))


def check_control_branch(checks: List["Check"]) -> None:
    """Xác minh nhánh đối chứng region_growing giữ đúng I1–I3."""
    group = "INV"

    from src.pipeline import BrainTumorPipeline

    image_path, _ = resolve_sample_image()
    if image_path is None:
        return
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        return

    diag, intermediates = BrainTumorPipeline(method="region_growing").process(image)
    mask = intermediates["tumor_mask"]
    ok = (
        mask.shape == image.shape and mask.dtype == np.uint8
        and set(np.unique(mask).tolist()).issubset({0, 255})
        and diag.tumor_area_px >= 0 and 0.0 <= diag.circularity <= 1.0
    )
    checks.append(Check(group, "I1–I3: nhánh region_growing", ok,
                        f"S={diag.tumor_area_px}px • C={diag.circularity:.4f}"))


# =============================================================================
# 4. BÁO CÁO TỔNG HỢP
# =============================================================================

def render_report(checks: List["Check"]) -> None:
    """In bảng tóm tắt kết quả kiểm tra."""
    headers = ("Nhóm", "Nội dung kiểm tra", "Kết quả", "Chi tiết")
    rows = [
        (c.group, c.name, "PASS" if c.ok else "FAIL", c.detail)
        for c in checks
    ]
    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i])
        for i in range(len(headers))
    ]

    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def fmt(cells: Tuple[str, str, str, str]) -> str:
        return "| " + " | ".join(
            cell.ljust(widths[i]) for i, cell in enumerate(cells)
        ) + " |"

    print(line)
    print(fmt(headers))
    print(line)
    previous_group = None
    for c in checks:
        if previous_group is not None and c.group != previous_group:
            print(line)
        previous_group = c.group
        print(fmt((c.group, c.name, "PASS" if c.ok else "FAIL", c.detail)))
    print(line)

    total = len(checks)
    passed = sum(1 for c in checks if c.ok)
    print()
    for group, label in (
        ("CFG", "Cấu hình YAML"),
        ("SIG", "Chữ ký hàm (SPEC §4)"),
        ("INV", "Bất biến dữ liệu I1–I7"),
    ):
        subset = [c for c in checks if c.group == group]
        if subset:
            print(f"  • {label:<28} {sum(1 for c in subset if c.ok)}/{len(subset)} đạt")
    print(f"  TỔNG CỘNG: {passed}/{total} kiểm tra đạt")


def main() -> int:
    checks: List[Check] = []

    print("=" * 78)
    print("KIỂM CHUẨN HỢP ĐỒNG KỸ THUẬT NGÀY 1 — HÀ MẠNH TRƯỜNG (2045240326)")
    print("Đồ án: Phân đoạn và phát hiện khối u não trên ảnh MRI (TCGA-LGG)")
    print("=" * 78)
    print()

    check_config(ROOT / "configs" / "default_params.yaml", checks)
    check_signatures(checks)
    check_invariants(checks)
    check_control_branch(checks)

    render_report(checks)

    failed = [c for c in checks if not c.ok]
    print()
    if failed:
        print(f"KẾT LUẬN: THẤT BẠI — {len(failed)} mục không đạt:")
        for c in failed:
            print(f"  - [{c.group}] {c.name}: {c.detail}")
        return 1

    print("KẾT LUẬN: ĐẠT — toàn bộ hợp đồng kỹ thuật Ngày 1 được xác minh.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
