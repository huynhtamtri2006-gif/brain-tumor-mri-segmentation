"""Unit test kiem thu toan dien lop dieu phoi BrainTumorPipeline.

Kiem tra su hop nhat 4 tang xu ly anh so:
Tien xu ly -> Tach so -> Phan doan (Watershed / Region Growing) -> Do dac trung & Truc quan hoa.
"""

import numpy as np
import pytest
from src.pipeline import BrainTumorPipeline
from src.measurement.features import DiagnosticResult


def test_pipeline_initialization():
    """Kiem tra khoi tao pipeline voi cac tham so mac dinh va tuy bien."""
    pipe_default = BrainTumorPipeline()
    assert pipe_default.method == "watershed"
    assert pipe_default.params == {}

    pipe_custom = BrainTumorPipeline(
        method="region_growing",
        params={"intensity_tolerance": 20, "min_tumor_area": 80}
    )
    assert pipe_custom.method == "region_growing"
    assert pipe_custom.params["intensity_tolerance"] == 20


def test_pipeline_watershed_process(sample_mri_image):
    """Kiem tra thuc thi pipeline voi phuong phap phan doan Marker-controlled Watershed."""
    pipeline = BrainTumorPipeline(method="watershed")
    diag_res, intermediates = pipeline.process(sample_mri_image)

    assert isinstance(diag_res, DiagnosticResult)
    assert isinstance(intermediates, dict)

    expected_keys = {
        "original", "filtered", "stripped", "brain_mask",
        "tumor_mask", "overlay", "quad"
    }
    assert set(intermediates.keys()) == expected_keys

    h, w = sample_mri_image.shape[:2]
    assert intermediates["original"].shape == (h, w)
    assert intermediates["filtered"].shape == (h, w)
    assert intermediates["stripped"].shape == (h, w)
    assert intermediates["brain_mask"].shape == (h, w)
    assert intermediates["tumor_mask"].shape == (h, w)
    assert intermediates["overlay"].shape == (h, w, 3)
    assert intermediates["quad"].shape == (h * 2, w * 2, 3)

    assert intermediates["tumor_mask"].dtype == np.uint8
    assert set(np.unique(intermediates["tumor_mask"])).issubset({0, 255})

    # Khi khong co ground truth, cac diem danh gia de None
    assert diag_res.dice_score is None
    assert diag_res.iou_score is None


def test_pipeline_region_growing_process(sample_mri_image):
    """Kiem tra thuc thi pipeline voi phuong phap doi chung Seeded Region Growing."""
    pipeline = BrainTumorPipeline(
        method="region_growing",
        params={"intensity_tolerance": 15}
    )
    diag_res, intermediates = pipeline.process(sample_mri_image)

    assert isinstance(diag_res, DiagnosticResult)
    assert isinstance(intermediates, dict)
    assert intermediates["tumor_mask"].shape == sample_mri_image.shape[:2]
    assert intermediates["tumor_mask"].dtype == np.uint8
    assert set(np.unique(intermediates["tumor_mask"])).issubset({0, 255})
    assert intermediates["quad"].shape == (
        sample_mri_image.shape[0] * 2,
        sample_mri_image.shape[1] * 2,
        3
    )


def test_pipeline_with_ground_truth(sample_mri_image, sample_tumor_mask):
    """Kiem tra pipeline tinh toan day du chi so Dice va IoU khi co Ground Truth."""
    pipeline = BrainTumorPipeline(method="watershed")
    diag_res, _ = pipeline.process(sample_mri_image, gt_mask=sample_tumor_mask)

    assert diag_res.dice_score is not None
    assert 0.0 <= diag_res.dice_score <= 1.0
    assert diag_res.iou_score is not None
    assert 0.0 <= diag_res.iou_score <= 1.0


def test_pipeline_empty_image():
    """Kiem tra kha nang xu ly an toan tuyet doi (fail-safe) tren anh den toan phan."""
    empty_image = np.zeros((256, 256), dtype=np.uint8)

    for method in ["watershed", "region_growing"]:
        pipeline = BrainTumorPipeline(method=method)
        diag_res, intermediates = pipeline.process(empty_image)

        assert isinstance(diag_res, DiagnosticResult)
        assert diag_res.tumor_detected is False
        assert diag_res.tumor_area_px == 0
        assert diag_res.tumor_ratio_percent == 0.0
        assert diag_res.circularity == 0.0
        assert diag_res.bbox is None

        assert intermediates["tumor_mask"].shape == (256, 256)
        assert np.count_nonzero(intermediates["tumor_mask"]) == 0
        assert intermediates["quad"].shape == (512, 512, 3)


def test_pipeline_custom_parameters(sample_mri_image):
    """Kiem tra truyen cac sieu tham so tuy bien vao pipeline."""
    pipeline = BrainTumorPipeline(
        method="watershed",
        params={"dist_thresh_ratio": 0.5, "min_tumor_area": 100}
    )
    diag_res, intermediates = pipeline.process(sample_mri_image)
    assert isinstance(diag_res, DiagnosticResult)
    assert intermediates["tumor_mask"].shape == sample_mri_image.shape[:2]
