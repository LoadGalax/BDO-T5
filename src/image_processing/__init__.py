"""
Image Processing module for BDO-T5 Icon Recognition System.
Handles icon detection and template matching.
"""

from .icon_detector import IconDetector
from .image_utils import ImageUtils

__all__ = ['IconDetector', 'ImageUtils']
