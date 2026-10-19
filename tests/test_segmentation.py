"""Unit test kiểm thử module phân đoạn khối u (Watershed & Region Growing)."""

import cv2
import numpy as np
from src.preprocessing.skull_strip import strip_skull
from src.segmentation.watershed import segment_watershed, WatershedSegmenter
from src.segmentation.region_growing import segment_region_growing, RegionGrowingSegmenter, find_seed_point


def test_watershed_segmentation(sample_mri_image):
    stripped, _ = strip_skull(sample_mri_image)
    mask = segment_watershed(stripped)
    assert mask.shape == sample_mri_image.shape
    assert set(np.unique(mask)).issubset({0, 255})

    segmenter = WatershedSegmenter()
    mask_obj = segmenter.segment(stripped)
    assert mask_obj.shape == sample_mri_image.shape


def test_region_growing_segmentation(sample_mri_image):
    stripped, _ = strip_skull(sample_mri_image)
    seed = find_seed_point(stripped)
    assert seed is not None
    assert 0 <= seed[0] < stripped.shape[0]
    assert 0 <= seed[1] < stripped.shape[1]

    mask = segment_region_growing(stripped, tolerance=20, seed_point=seed)
    assert mask.shape == sample_mri_image.shape
    assert set(np.unique(mask)).issubset({0, 255})

    segmenter = RegionGrowingSegmenter(tolerance=20)
    mask_obj = segmenter.segment(stripped)
    assert mask_obj.shape == sample_mri_image.shape


def test_watershed_intermediates(sample_mri_image):
    stripped, _ = strip_skull(sample_mri_image)
    result = segment_watershed(stripped, return_intermediates=True)

    assert isinstance(result, tuple) and len(result) == 2
    mask, intermediates = result

    expected_keys = {
        "original", "binary_high", "opened", "dist_transform",
        "sure_fg", "sure_bg", "unknown", "markers", "tumor_mask",
    }
    assert set(intermediates.keys()) == expected_keys

    for key in expected_keys:
        step_image = intermediates[key]
        assert step_image.shape == stripped.shape
        assert step_image.dtype == np.uint8

    assert np.array_equal(mask, intermediates["tumor_mask"])


def test_watershed_empty_image():
    empty = np.zeros((256, 256), dtype=np.uint8)

    mask = segment_watershed(empty)
    assert mask.shape == empty.shape
    assert mask.dtype == np.uint8
    assert np.count_nonzero(mask) == 0

    mask_rich, intermediates = segment_watershed(empty, return_intermediates=True)
    assert np.count_nonzero(mask_rich) == 0
    assert len(intermediates) == 9
    for step_image in intermediates.values():
        assert step_image.shape == empty.shape
        assert step_image.dtype == np.uint8
        assert np.count_nonzero(step_image) == 0


def test_watershed_min_tumor_area_filter():
    image = np.zeros((256, 256), dtype=np.uint8)
    cv2.circle(image, (128, 128), 100, 100, -1)  # Nhu mô não giả lập
    cv2.circle(image, (90, 128), 15, 255, -1)    # Đảo lớn ~700 px
    cv2.rectangle(image, (178, 128), (180, 131), 255, -1)  # Đảo nhỏ 3x4 = 12 px
    assert int(np.count_nonzero(image == 255)) >= 700

    def component_areas(mask):
        num_labels, _, stats, _ = cv2.connectedComponentsWithStats(
            (mask > 0).astype(np.uint8), connectivity=8
        )
        return sorted(stats[1:, cv2.CC_STAT_AREA].tolist(), reverse=True)

    unfiltered = component_areas(
        segment_watershed(image, dist_thresh_ratio=0.1, min_tumor_area=0)
    )
    assert any(area < 50 for area in unfiltered)
    assert any(area >= 500 for area in unfiltered)

    filtered = component_areas(
        segment_watershed(image, dist_thresh_ratio=0.1, min_tumor_area=50)
    )
    assert filtered and all(area >= 50 for area in filtered)
    assert max(filtered) >= 500


def test_watershed_parameter_variation(sample_mri_image):
    stripped, _ = strip_skull(sample_mri_image)
    for ratio in (0.2, 0.3, 0.4, 0.5, 0.6):
        mask = segment_watershed(stripped, dist_thresh_ratio=ratio)
        assert mask.shape == stripped.shape
        assert mask.dtype == np.uint8
        assert set(np.unique(mask)).issubset({0, 255})
