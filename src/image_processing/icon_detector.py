"""
Icon detection module using template matching and computer vision.
"""

from pathlib import Path
from typing import List, Tuple, Optional, Dict

import cv2
import numpy as np

from .image_utils import ImageUtils


class Detection:
    """Represents a single icon detection."""

    def __init__(
        self,
        template_name: str,
        position: Tuple[int, int],
        size: Tuple[int, int],
        confidence: float,
        template_hash: str = ""
    ):
        self.template_name = template_name
        self.position = position  # (x, y)
        self.size = size  # (width, height)
        self.confidence = confidence
        self.template_hash = template_hash

    def __repr__(self):
        return (f"Detection(name={self.template_name}, pos={self.position}, "
                f"size={self.size}, conf={self.confidence:.3f})")


class IconDetector:
    """Detects icons in images using template matching."""

    def __init__(self, template_dir: str = "data/templates", confidence_threshold: float = 0.8):
        """
        Initialize icon detector.

        Args:
            template_dir: Directory containing template images
            confidence_threshold: Minimum confidence for detection (0.0 to 1.0)
        """
        self.template_dir = Path(template_dir)
        self.confidence_threshold = confidence_threshold
        self.templates: Dict[str, dict] = {}
        self.load_templates()

    def load_templates(self):
        """Load all template images from template directory."""
        if not self.template_dir.exists():
            print(f"Template directory does not exist: {self.template_dir}")
            self.template_dir.mkdir(parents=True, exist_ok=True)
            return

        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
        template_files = []

        for ext in image_extensions:
            template_files.extend(self.template_dir.glob(f"*{ext}"))
            template_files.extend(self.template_dir.glob(f"**/*{ext}"))

        if not template_files:
            print(f"No template images found in {self.template_dir}")
            return

        for template_path in template_files:
            template_img = ImageUtils.load_image(str(template_path))
            if template_img is not None:
                # Get template name (filename without extension)
                template_name = template_path.stem

                # Get category from subdirectory if exists
                if template_path.parent != self.template_dir:
                    category = template_path.parent.name
                else:
                    category = "general"

                # Compute hash for the template
                img_hash = ImageUtils.compute_image_hash(template_img)

                # Store template info
                self.templates[template_name] = {
                    'image': template_img,
                    'path': str(template_path),
                    'hash': img_hash,
                    'category': category,
                    'size': (template_img.shape[1], template_img.shape[0])  # (width, height)
                }

        print(f"Loaded {len(self.templates)} templates from {self.template_dir}")

    def add_template(self, template_image: np.ndarray, name: str, category: str = "general") -> bool:
        """
        Add a new template to the detector.

        Args:
            template_image: Template image as numpy array
            name: Name for the template
            category: Category of the template

        Returns:
            True if successful, False otherwise
        """
        try:
            # Compute hash
            img_hash = ImageUtils.compute_image_hash(template_image)

            # Save template to disk
            save_dir = self.template_dir / category
            save_dir.mkdir(parents=True, exist_ok=True)
            save_path = save_dir / f"{name}.png"

            if ImageUtils.save_image(template_image, str(save_path)):
                # Add to templates dict
                self.templates[name] = {
                    'image': template_image,
                    'path': str(save_path),
                    'hash': img_hash,
                    'category': category,
                    'size': (template_image.shape[1], template_image.shape[0])
                }
                print(f"Added template: {name} (category: {category})")
                return True
            return False
        except Exception as e:
            print(f"Error adding template {name}: {e}")
            return False

    def detect_icons(
        self,
        image: np.ndarray,
        template_names: Optional[List[str]] = None,
        method: int = cv2.TM_CCOEFF_NORMED,
        multi_scale: bool = True
    ) -> List[Detection]:
        """
        Detect icons in an image using template matching.

        Args:
            image: Input image to search
            template_names: List of template names to search for (None = all templates)
            method: OpenCV template matching method
            multi_scale: Whether to search at multiple scales

        Returns:
            List of Detection objects
        """
        detections = []

        # Determine which templates to use
        if template_names is None:
            templates_to_search = self.templates.items()
        else:
            templates_to_search = [(name, self.templates[name])
                                    for name in template_names if name in self.templates]

        # Preprocess image
        gray_image = ImageUtils.preprocess_for_matching(image)

        # Search for each template
        for template_name, template_info in templates_to_search:
            template = template_info['image']
            template_gray = ImageUtils.preprocess_for_matching(template)

            if multi_scale:
                # Multi-scale detection
                scale_detections = self._detect_multi_scale(
                    gray_image, template_gray, template_name, template_info, method
                )
                detections.extend(scale_detections)
            else:
                # Single scale detection
                single_detection = self._detect_single_scale(
                    gray_image, template_gray, template_name, template_info, method
                )
                if single_detection:
                    detections.append(single_detection)

        # Apply non-maximum suppression to remove overlapping detections
        detections = self._non_max_suppression(detections)

        return detections

    def _detect_single_scale(
        self,
        image: np.ndarray,
        template: np.ndarray,
        template_name: str,
        template_info: dict,
        method: int
    ) -> Optional[Detection]:
        """
        Detect template at single scale.

        Args:
            image: Grayscale input image
            template: Grayscale template image
            template_name: Name of the template
            template_info: Template information dict
            method: Template matching method

        Returns:
            Detection object if found, None otherwise
        """
        # Ensure template is smaller than image
        if template.shape[0] > image.shape[0] or template.shape[1] > image.shape[1]:
            return None

        # Perform template matching
        result = cv2.matchTemplate(image, template, method)

        # Find best match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # For methods where lower is better
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            confidence = 1 - min_val
            top_left = min_loc
        else:
            confidence = max_val
            top_left = max_loc

        # Check if confidence meets threshold
        if confidence >= self.confidence_threshold:
            template_h, template_w = template.shape
            return Detection(
                template_name=template_name,
                position=top_left,
                size=(template_w, template_h),
                confidence=confidence,
                template_hash=template_info['hash']
            )

        return None

    def _detect_multi_scale(
        self,
        image: np.ndarray,
        template: np.ndarray,
        template_name: str,
        template_info: dict,
        method: int,
        scales: List[float] = None
    ) -> List[Detection]:
        """
        Detect template at multiple scales.

        Args:
            image: Grayscale input image
            template: Grayscale template image
            template_name: Name of the template
            template_info: Template information dict
            method: Template matching method
            scales: List of scale factors (None = default scales)

        Returns:
            List of Detection objects
        """
        if scales is None:
            # Default scales: 0.8x to 1.2x in 0.1 increments
            scales = [0.8, 0.9, 1.0, 1.1, 1.2]

        detections = []

        for scale in scales:
            # Resize template
            scaled_template = cv2.resize(
                template,
                (int(template.shape[1] * scale), int(template.shape[0] * scale)),
                interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC
            )

            # Skip if template is larger than image
            if scaled_template.shape[0] > image.shape[0] or scaled_template.shape[1] > image.shape[1]:
                continue

            # Perform template matching
            result = cv2.matchTemplate(image, scaled_template, method)

            # Find matches above threshold
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                locations = np.where(result <= (1 - self.confidence_threshold))
                confidences = 1 - result[locations]
            else:
                locations = np.where(result >= self.confidence_threshold)
                confidences = result[locations]

            # Create detections
            for pt, conf in zip(zip(*locations[::-1]), confidences):
                detection = Detection(
                    template_name=template_name,
                    position=pt,
                    size=(scaled_template.shape[1], scaled_template.shape[0]),
                    confidence=float(conf),
                    template_hash=template_info['hash']
                )
                detections.append(detection)

        return detections

    def _non_max_suppression(self, detections: List[Detection], overlap_threshold: float = 0.3) -> List[Detection]:
        """
        Apply non-maximum suppression to remove overlapping detections.

        Args:
            detections: List of Detection objects
            overlap_threshold: Maximum allowed overlap (IoU)

        Returns:
            Filtered list of Detection objects
        """
        if not detections:
            return []

        # Sort by confidence (descending)
        detections = sorted(detections, key=lambda d: d.confidence, reverse=True)

        keep = []

        while detections:
            # Keep the detection with highest confidence
            best = detections.pop(0)
            keep.append(best)

            # Remove overlapping detections
            detections = [d for d in detections if self._compute_iou(best, d) < overlap_threshold]

        return keep

    @staticmethod
    def _compute_iou(det1: Detection, det2: Detection) -> float:
        """
        Compute Intersection over Union (IoU) between two detections.

        Args:
            det1: First detection
            det2: Second detection

        Returns:
            IoU value (0.0 to 1.0)
        """
        x1, y1 = det1.position
        w1, h1 = det1.size
        x2, y2 = det2.position
        w2, h2 = det2.size

        # Compute intersection
        x_left = max(x1, x2)
        y_top = max(y1, y2)
        x_right = min(x1 + w1, x2 + w2)
        y_bottom = min(y1 + h1, y2 + h2)

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        intersection = (x_right - x_left) * (y_bottom - y_top)

        # Compute union
        area1 = w1 * h1
        area2 = w2 * h2
        union = area1 + area2 - intersection

        return intersection / union if union > 0 else 0.0

    def visualize_detections(self, image: np.ndarray, detections: List[Detection]) -> np.ndarray:
        """
        Draw detections on image for visualization.

        Args:
            image: Input image
            detections: List of Detection objects

        Returns:
            Image with detections drawn
        """
        result = image.copy()

        for detection in detections:
            result = ImageUtils.draw_detection(
                result,
                detection.position,
                detection.size,
                label=detection.template_name,
                confidence=detection.confidence,
                color=(0, 255, 0)
            )

        return result

    def get_template_info(self, template_name: str) -> Optional[dict]:
        """
        Get information about a template.

        Args:
            template_name: Name of the template

        Returns:
            Template info dict or None if not found
        """
        return self.templates.get(template_name)

    def get_all_template_names(self) -> List[str]:
        """
        Get list of all loaded template names.

        Returns:
            List of template names
        """
        return list(self.templates.keys())

    def get_templates_by_category(self, category: str) -> List[str]:
        """
        Get template names filtered by category.

        Args:
            category: Category name

        Returns:
            List of template names in the category
        """
        return [name for name, info in self.templates.items() if info['category'] == category]
