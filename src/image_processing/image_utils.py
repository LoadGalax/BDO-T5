"""
Image utility functions for preprocessing and manipulation.
"""

import hashlib
from pathlib import Path
from typing import Tuple, Optional

import cv2
import numpy as np
from PIL import Image


class ImageUtils:
    """Utility class for image processing operations."""

    @staticmethod
    def load_image(image_path: str) -> Optional[np.ndarray]:
        """
        Load an image from file.

        Args:
            image_path: Path to image file

        Returns:
            Image as numpy array (BGR format) or None if failed
        """
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                print(f"Failed to load image: {image_path}")
            return img
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None

    @staticmethod
    def save_image(image: np.ndarray, save_path: str) -> bool:
        """
        Save image to file.

        Args:
            image: Image as numpy array
            save_path: Path where to save the image

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(save_path), image)
            return True
        except Exception as e:
            print(f"Error saving image to {save_path}: {e}")
            return False

    @staticmethod
    def compute_image_hash(image: np.ndarray) -> str:
        """
        Compute a hash for an image based on its content.

        Args:
            image: Image as numpy array

        Returns:
            Hash string (MD5)
        """
        # Resize to standard size for consistent hashing
        resized = cv2.resize(image, (64, 64))
        # Convert to grayscale
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        # Compute hash
        img_hash = hashlib.md5(gray.tobytes()).hexdigest()
        return img_hash

    @staticmethod
    def preprocess_for_matching(image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for template matching.

        Args:
            image: Input image

        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply slight Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        return blurred

    @staticmethod
    def preprocess_for_ocr(image: np.ndarray, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """
        Preprocess image region for OCR.

        Args:
            image: Input image
            region: Optional (x, y, w, h) tuple to extract region

        Returns:
            Preprocessed image optimized for OCR
        """
        # Extract region if specified
        if region:
            x, y, w, h = region
            image = image[y:y+h, x:x+w]

        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply adaptive thresholding for better text recognition
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Denoise
        denoised = cv2.fastNlMeansDenoising(binary, None, 10, 7, 21)

        # Resize for better OCR (2x upscale)
        height, width = denoised.shape
        upscaled = cv2.resize(denoised, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)

        return upscaled

    @staticmethod
    def draw_detection(
        image: np.ndarray,
        position: Tuple[int, int],
        size: Tuple[int, int],
        label: str = "",
        confidence: float = 0.0,
        color: Tuple[int, int, int] = (0, 255, 0)
    ) -> np.ndarray:
        """
        Draw detection box and label on image.

        Args:
            image: Input image
            position: (x, y) top-left corner
            size: (width, height) of detection box
            label: Label text to display
            confidence: Confidence score to display
            color: BGR color tuple

        Returns:
            Image with detection drawn
        """
        result = image.copy()
        x, y = position
        w, h = size

        # Draw rectangle
        cv2.rectangle(result, (x, y), (x + w, y + h), color, 2)

        # Prepare label text
        if label:
            text = f"{label}"
            if confidence > 0:
                text += f" ({confidence:.2f})"

            # Calculate text size for background
            (text_width, text_height), baseline = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
            )

            # Draw background for text
            cv2.rectangle(
                result,
                (x, y - text_height - baseline - 5),
                (x + text_width, y),
                color,
                -1
            )

            # Draw text
            cv2.putText(
                result,
                text,
                (x, y - baseline - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

        return result

    @staticmethod
    def extract_region(image: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
        """
        Extract a region from an image.

        Args:
            image: Input image
            x: X coordinate
            y: Y coordinate
            w: Width
            h: Height

        Returns:
            Extracted region
        """
        return image[y:y+h, x:x+w].copy()

    @staticmethod
    def resize_maintain_aspect(image: np.ndarray, max_width: int = 1920, max_height: int = 1080) -> np.ndarray:
        """
        Resize image while maintaining aspect ratio.

        Args:
            image: Input image
            max_width: Maximum width
            max_height: Maximum height

        Returns:
            Resized image
        """
        h, w = image.shape[:2]

        if w <= max_width and h <= max_height:
            return image

        scale = min(max_width / w, max_height / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    @staticmethod
    def create_thumbnail(image: np.ndarray, size: Tuple[int, int] = (128, 128)) -> np.ndarray:
        """
        Create a thumbnail of the image.

        Args:
            image: Input image
            size: Thumbnail size (width, height)

        Returns:
            Thumbnail image
        """
        return cv2.resize(image, size, interpolation=cv2.INTER_AREA)
