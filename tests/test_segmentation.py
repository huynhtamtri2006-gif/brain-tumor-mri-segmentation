"""Unit test kiểm thử module phân đoạn khối u (Watershed & Region Growing)."""

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
