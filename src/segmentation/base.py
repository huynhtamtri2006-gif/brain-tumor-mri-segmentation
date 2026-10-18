"""Giao diện trừu tượng (Base Segmenter) định nghĩa chuẩn chung cho các thuật toán phân đoạn u não.

Phụ trách: Hà Mạnh Trường (MSSV: 2045240326).
"""

from abc import ABC, abstractmethod
import numpy as np


class BaseSegmenter(ABC):
    """Abstract Base Class cho mọi thuật toán phân đoạn khối u não."""

    @abstractmethod
    def segment(self, brain_image: np.ndarray) -> np.ndarray:
        """Thực thi phân đoạn khối u trên ảnh não đã tách sọ.
        
        Args:
            brain_image: Ảnh nhu mô não đã tách sọ (H, W), dtype uint8 [0, 255].
            
        Returns:
            np.ndarray: Mặt nạ nhị phân khối u (H, W), dtype uint8 với {0, 255}.
        """
        pass
