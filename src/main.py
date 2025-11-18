"""
Main application for BDO-T5 Icon Recognition System.
Processes images to detect icons and numbers, storing results in database.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np

from database import DatabaseManager, Icon, IconData
from image_processing import IconDetector, ImageUtils
from ocr import OCRReader
from utils import ConfigLoader


class BDOIconRecognizer:
    """Main application class for BDO icon recognition."""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the BDO Icon Recognizer.

        Args:
            config_path: Path to configuration file
        """
        print("Initializing BDO-T5 Icon Recognition System...")

        # Load configuration
        self.config = ConfigLoader(config_path)

        # Initialize database
        db_path = self.config.get('database.path', 'data/bdo_icons.db')
        self.db = DatabaseManager(db_path)

        # Initialize icon detector
        template_dir = self.config.get('image_processing.template_dir', 'data/templates')
        confidence = self.config.get('image_processing.confidence_threshold', 0.8)
        self.detector = IconDetector(template_dir, confidence)

        # Initialize OCR reader
        ocr_engine = self.config.get('ocr.engine', 'auto')
        ocr_language = self.config.get('ocr.language', 'en')
        self.ocr = OCRReader(ocr_engine, ocr_language)

        print("Initialization complete!")
        print(f"- Templates loaded: {len(self.detector.templates)}")
        print(f"- Database: {db_path}")
        print(f"- OCR Engine: {self.ocr.engine}")

    def process_image(self, image_path: str, save_visualization: bool = True) -> List[IconData]:
        """
        Process an image to detect icons and numbers.

        Args:
            image_path: Path to image file
            save_visualization: Whether to save visualization image

        Returns:
            List of IconData objects that were stored in database
        """
        print(f"\nProcessing image: {image_path}")

        # Load image
        image = ImageUtils.load_image(image_path)
        if image is None:
            print(f"Failed to load image: {image_path}")
            return []

        # Resize if needed
        max_width = self.config.get('processing.max_image_width', 1920)
        max_height = self.config.get('processing.max_image_height', 1080)
        image = ImageUtils.resize_maintain_aspect(image, max_width, max_height)

        # Detect icons
        print("Detecting icons...")
        multi_scale = self.config.get('image_processing.multi_scale_detection', True)
        detections = self.detector.detect_icons(image, multi_scale=multi_scale)
        print(f"Found {len(detections)} icon(s)")

        # Process each detection
        stored_data = []
        for i, detection in enumerate(detections, 1):
            print(f"\nProcessing detection {i}/{len(detections)}: {detection.template_name}")

            # Get or create icon in database
            icon = self.db.get_icon_by_hash(detection.template_hash)
            if icon is None:
                # Get template info
                template_info = self.detector.get_template_info(detection.template_name)

                # Create new icon
                icon = Icon(
                    name=detection.template_name,
                    icon_hash=detection.template_hash,
                    category=template_info['category'] if template_info else 'unknown',
                    image_path=template_info['path'] if template_info else '',
                    confidence_threshold=self.detector.confidence_threshold
                )
                icon_id, was_created = self.db.upsert_icon(icon)
                icon.id = icon_id
                print(f"  Icon {'created' if was_created else 'found'} in database (ID: {icon_id})")
            else:
                print(f"  Icon exists in database (ID: {icon.id})")

            # Read numbers near the detected icon
            search_width = self.config.get('ocr.number_search_region.width', 100)
            search_height = self.config.get('ocr.number_search_region.height', 50)
            direction = self.config.get('ocr.default_direction', 'right')

            ocr_result = self.ocr.read_number_near_position(
                image,
                detection.position,
                search_size=(search_width, search_height),
                direction=direction
            )

            # Extract detected number and text
            detected_number = None
            detected_text = ""

            if ocr_result:
                detected_number = ocr_result.get_primary_number()
                detected_text = ocr_result.text
                print(f"  Detected text: '{detected_text}' (number: {detected_number})")
            else:
                print(f"  No text/numbers detected near icon")

            # Create icon data record
            icon_data = IconData(
                icon_id=icon.id,
                detected_number=detected_number,
                detected_text=detected_text,
                source_image_path=str(image_path),
                position_x=detection.position[0],
                position_y=detection.position[1],
                confidence=detection.confidence
            )

            # Store in database
            data_id = self.db.add_icon_data(icon_data)
            icon_data.id = data_id
            stored_data.append(icon_data)
            print(f"  Stored in database (ID: {data_id})")

        # Save visualization if requested
        if save_visualization and detections:
            vis_image = self.detector.visualize_detections(image, detections)
            vis_dir = self.config.get('processing.visualization_dir', 'data/processed')
            Path(vis_dir).mkdir(parents=True, exist_ok=True)

            vis_path = Path(vis_dir) / f"{Path(image_path).stem}_processed.png"
            if ImageUtils.save_image(vis_image, str(vis_path)):
                print(f"\nVisualization saved to: {vis_path}")

        print(f"\nProcessing complete! Stored {len(stored_data)} detection(s)")
        return stored_data

    def add_template(self, image_path: str, name: str, category: str = "general") -> bool:
        """
        Add a new icon template.

        Args:
            image_path: Path to template image
            name: Name for the template
            category: Category of the template

        Returns:
            True if successful, False otherwise
        """
        print(f"Adding template: {name} (category: {category})")

        # Load image
        template_img = ImageUtils.load_image(image_path)
        if template_img is None:
            print(f"Failed to load template image: {image_path}")
            return False

        # Add to detector
        if self.detector.add_template(template_img, name, category):
            # Compute hash
            img_hash = ImageUtils.compute_image_hash(template_img)

            # Add to database
            template_info = self.detector.get_template_info(name)
            icon = Icon(
                name=name,
                icon_hash=img_hash,
                category=category,
                image_path=template_info['path'] if template_info else '',
                confidence_threshold=self.detector.confidence_threshold
            )

            icon_id, was_created = self.db.upsert_icon(icon)
            print(f"Template added to database (ID: {icon_id}, created: {was_created})")
            return True

        return False

    def list_templates(self):
        """List all loaded templates."""
        templates = self.detector.get_all_template_names()

        if not templates:
            print("No templates loaded.")
            return

        print(f"\nLoaded Templates ({len(templates)}):")
        print("-" * 60)

        # Group by category
        categories = {}
        for name in templates:
            info = self.detector.get_template_info(name)
            category = info['category'] if info else 'unknown'
            if category not in categories:
                categories[category] = []
            categories[category].append(name)

        for category, names in sorted(categories.items()):
            print(f"\n{category.upper()}:")
            for name in sorted(names):
                print(f"  - {name}")

    def show_statistics(self):
        """Display database statistics."""
        stats = self.db.get_statistics()

        print("\nDatabase Statistics:")
        print("-" * 60)
        print(f"Total Icons: {stats['total_icons']}")
        print(f"Total Detections: {stats['total_detections']}")
        print(f"Categories: {stats['categories_count']}")

        if stats['icons_by_category']:
            print("\nIcons by Category:")
            for category, count in sorted(stats['icons_by_category'].items()):
                print(f"  {category}: {count}")

    def close(self):
        """Clean up resources."""
        self.db.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BDO-T5 Icon Recognition System - Detect and track Black Desert Online icons"
    )

    parser.add_argument(
        'command',
        choices=['process', 'add-template', 'list', 'stats'],
        help='Command to execute'
    )

    parser.add_argument(
        '--image',
        '-i',
        type=str,
        help='Path to image file'
    )

    parser.add_argument(
        '--name',
        '-n',
        type=str,
        help='Template name (for add-template command)'
    )

    parser.add_argument(
        '--category',
        '-c',
        type=str,
        default='general',
        help='Template category (for add-template command)'
    )

    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help='Path to configuration file'
    )

    parser.add_argument(
        '--no-viz',
        action='store_true',
        help='Disable visualization output'
    )

    args = parser.parse_args()

    # Initialize application
    try:
        app = BDOIconRecognizer(args.config)
    except Exception as e:
        print(f"Error initializing application: {e}")
        return 1

    try:
        # Execute command
        if args.command == 'process':
            if not args.image:
                print("Error: --image is required for process command")
                return 1

            app.process_image(args.image, save_visualization=not args.no_viz)

        elif args.command == 'add-template':
            if not args.image or not args.name:
                print("Error: --image and --name are required for add-template command")
                return 1

            app.add_template(args.image, args.name, args.category)

        elif args.command == 'list':
            app.list_templates()

        elif args.command == 'stats':
            app.show_statistics()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        app.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())
