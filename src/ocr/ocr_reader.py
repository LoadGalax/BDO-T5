"""
OCR Reader module for extracting text and numbers from images.
"""

import re
from typing import Optional, Tuple, List, Dict

import cv2
import numpy as np

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False
    print("Warning: pytesseract not available. Install with: pip install pytesseract")

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    print("Warning: easyocr not available. Install with: pip install easyocr")

from ..image_processing.image_utils import ImageUtils


class OCRResult:
    """Represents OCR detection result."""

    def __init__(self, text: str, confidence: float, bbox: Optional[Tuple[int, int, int, int]] = None):
        """
        Initialize OCR result.

        Args:
            text: Detected text
            confidence: Confidence score (0.0 to 1.0)
            bbox: Bounding box as (x, y, width, height)
        """
        self.text = text
        self.confidence = confidence
        self.bbox = bbox

        # Try to extract numbers
        self.numbers = self._extract_numbers(text)

    @staticmethod
    def _extract_numbers(text: str) -> List[int]:
        """
        Extract all numbers from text.

        Args:
            text: Input text

        Returns:
            List of integers found in text
        """
        # Find all number sequences
        number_strings = re.findall(r'\d+', text)
        return [int(num) for num in number_strings]

    def get_primary_number(self) -> Optional[int]:
        """
        Get the primary/largest number from detected text.

        Returns:
            Largest number or None if no numbers found
        """
        if self.numbers:
            return max(self.numbers)
        return None

    def __repr__(self):
        return f"OCRResult(text='{self.text}', confidence={self.confidence:.3f}, numbers={self.numbers})"


class OCRReader:
    """Reads text and numbers from images using OCR."""

    def __init__(self, engine: str = "auto", language: str = "en"):
        """
        Initialize OCR reader.

        Args:
            engine: OCR engine to use ("pytesseract", "easyocr", or "auto")
            language: Language code for OCR
        """
        self.language = language
        self.engine = engine
        self.easyocr_reader = None

        # Determine which engine to use
        if engine == "auto":
            if EASYOCR_AVAILABLE:
                self.engine = "easyocr"
            elif PYTESSERACT_AVAILABLE:
                self.engine = "pytesseract"
            else:
                raise RuntimeError("No OCR engine available. Install pytesseract or easyocr.")
        elif engine == "easyocr" and not EASYOCR_AVAILABLE:
            raise RuntimeError("EasyOCR not available. Install with: pip install easyocr")
        elif engine == "pytesseract" and not PYTESSERACT_AVAILABLE:
            raise RuntimeError("Pytesseract not available. Install with: pip install pytesseract")

        # Initialize EasyOCR if selected
        if self.engine == "easyocr":
            print("Initializing EasyOCR reader (this may take a moment)...")
            self.easyocr_reader = easyocr.Reader([language], gpu=False)

        print(f"OCR Reader initialized with engine: {self.engine}")

    def read_text(self, image: np.ndarray, preprocess: bool = True) -> List[OCRResult]:
        """
        Read all text from image.

        Args:
            image: Input image
            preprocess: Whether to preprocess image for better OCR

        Returns:
            List of OCRResult objects
        """
        if preprocess:
            processed = ImageUtils.preprocess_for_ocr(image)
        else:
            processed = image

        if self.engine == "pytesseract":
            return self._read_with_pytesseract(processed)
        elif self.engine == "easyocr":
            return self._read_with_easyocr(processed)
        else:
            return []

    def read_numbers(self, image: np.ndarray, preprocess: bool = True) -> List[OCRResult]:
        """
        Read only numbers from image.

        Args:
            image: Input image
            preprocess: Whether to preprocess image for better OCR

        Returns:
            List of OCRResult objects containing numbers
        """
        all_results = self.read_text(image, preprocess)
        # Filter to only results containing numbers
        return [result for result in all_results if result.numbers]

    def read_region(
        self,
        image: np.ndarray,
        region: Tuple[int, int, int, int],
        preprocess: bool = True
    ) -> List[OCRResult]:
        """
        Read text from specific region of image.

        Args:
            image: Input image
            region: (x, y, width, height) region to read
            preprocess: Whether to preprocess image for better OCR

        Returns:
            List of OCRResult objects
        """
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        return self.read_text(roi, preprocess)

    def read_number_near_position(
        self,
        image: np.ndarray,
        position: Tuple[int, int],
        search_size: Tuple[int, int] = (100, 50),
        direction: str = "right"
    ) -> Optional[OCRResult]:
        """
        Read number near a specific position (e.g., next to an icon).

        Args:
            image: Input image
            position: (x, y) reference position
            search_size: (width, height) of search region
            direction: Search direction ("right", "left", "top", "bottom")

        Returns:
            OCRResult with highest confidence number, or None
        """
        x, y = position
        w, h = search_size

        # Calculate search region based on direction
        if direction == "right":
            region = (x, y, w, h)
        elif direction == "left":
            region = (max(0, x - w), y, w, h)
        elif direction == "top":
            region = (x, max(0, y - h), w, h)
        elif direction == "bottom":
            region = (x, y, w, h)
        else:
            region = (x, y, w, h)

        # Ensure region is within image bounds
        img_h, img_w = image.shape[:2]
        x, y, w, h = region
        x = max(0, min(x, img_w - 1))
        y = max(0, min(y, img_h - 1))
        w = min(w, img_w - x)
        h = min(h, img_h - y)

        if w <= 0 or h <= 0:
            return None

        # Read numbers from region
        results = self.read_region(image, (x, y, w, h))

        # Filter to only results with numbers
        number_results = [r for r in results if r.numbers]

        if number_results:
            # Return result with highest confidence
            return max(number_results, key=lambda r: r.confidence)

        return None

    def _read_with_pytesseract(self, image: np.ndarray) -> List[OCRResult]:
        """
        Read text using Pytesseract.

        Args:
            image: Preprocessed image

        Returns:
            List of OCRResult objects
        """
        try:
            # Get detailed data from Pytesseract
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

            results = []
            n_boxes = len(data['text'])

            for i in range(n_boxes):
                text = data['text'][i].strip()
                conf = float(data['conf'][i])

                # Skip empty or low confidence detections
                if not text or conf < 0:
                    continue

                # Normalize confidence to 0-1 range (Tesseract uses 0-100)
                confidence = conf / 100.0

                # Get bounding box
                x = data['left'][i]
                y = data['top'][i]
                w = data['width'][i]
                h = data['height'][i]

                result = OCRResult(text, confidence, (x, y, w, h))
                results.append(result)

            return results

        except Exception as e:
            print(f"Error in Pytesseract OCR: {e}")
            return []

    def _read_with_easyocr(self, image: np.ndarray) -> List[OCRResult]:
        """
        Read text using EasyOCR.

        Args:
            image: Preprocessed image

        Returns:
            List of OCRResult objects
        """
        try:
            # EasyOCR expects RGB image
            if len(image.shape) == 2:
                # Convert grayscale to RGB
                image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif len(image.shape) == 3 and image.shape[2] == 3:
                # Convert BGR to RGB
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image

            # Read text
            detections = self.easyocr_reader.readtext(image_rgb)

            results = []
            for detection in detections:
                bbox_points, text, confidence = detection

                # Convert bbox points to (x, y, w, h)
                xs = [p[0] for p in bbox_points]
                ys = [p[1] for p in bbox_points]
                x = int(min(xs))
                y = int(min(ys))
                w = int(max(xs) - x)
                h = int(max(ys) - y)

                result = OCRResult(text.strip(), confidence, (x, y, w, h))
                results.append(result)

            return results

        except Exception as e:
            print(f"Error in EasyOCR: {e}")
            return []

    def extract_numbers_only(self, text: str) -> List[int]:
        """
        Extract only numbers from text string.

        Args:
            text: Input text

        Returns:
            List of integers
        """
        return OCRResult._extract_numbers(text)

    def visualize_ocr_results(self, image: np.ndarray, results: List[OCRResult]) -> np.ndarray:
        """
        Draw OCR results on image for visualization.

        Args:
            image: Input image
            results: List of OCRResult objects

        Returns:
            Image with OCR results drawn
        """
        result_img = image.copy()

        for ocr_result in results:
            if ocr_result.bbox:
                x, y, w, h = ocr_result.bbox

                # Draw rectangle
                cv2.rectangle(result_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Draw text
                label = f"{ocr_result.text} ({ocr_result.confidence:.2f})"
                cv2.putText(
                    result_img,
                    label,
                    (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    1
                )

        return result_img
