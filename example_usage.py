#!/usr/bin/env python
"""
Example usage script for BDO-T5 Icon Recognition System.
Demonstrates common usage patterns.
"""

from pathlib import Path
from src.main import BDOIconRecognizer
from src.database import DatabaseManager
from src.image_processing import IconDetector, ImageUtils


def example_full_workflow():
    """Example: Full workflow from template to detection."""
    print("=" * 60)
    print("EXAMPLE 1: Full Workflow")
    print("=" * 60)

    # Initialize application
    app = BDOIconRecognizer()

    # Add a template (if you have one)
    # app.add_template("path/to/icon.png", "my_icon", "items")

    # Process an image
    # results = app.process_image("path/to/screenshot.png")

    # Show statistics
    app.show_statistics()

    # List all templates
    app.list_templates()

    app.close()


def example_database_queries():
    """Example: Database queries and operations."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Database Operations")
    print("=" * 60)

    with DatabaseManager() as db:
        # Get statistics
        stats = db.get_statistics()
        print(f"\nTotal Icons: {stats['total_icons']}")
        print(f"Total Detections: {stats['total_detections']}")

        # Get all icons
        icons = db.get_all_icons()
        print(f"\nIcons in database:")
        for icon in icons[:5]:  # Show first 5
            print(f"  - {icon.name} ({icon.category})")

        # Get recent detections
        recent = db.get_recent_icon_data(limit=10)
        print(f"\nRecent detections: {len(recent)}")
        for data in recent[:3]:  # Show first 3
            icon = db.get_icon_by_id(data.icon_id)
            if icon:
                print(f"  - {icon.name}: {data.detected_number} at {data.timestamp}")


def example_icon_detection():
    """Example: Icon detection with visualization."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Icon Detection")
    print("=" * 60)

    # Initialize detector
    detector = IconDetector("data/templates", confidence_threshold=0.75)

    print(f"Loaded {len(detector.templates)} templates")

    # If you have an image, detect icons
    # image = ImageUtils.load_image("screenshot.png")
    # if image:
    #     detections = detector.detect_icons(image, multi_scale=True)
    #     print(f"Found {len(detections)} icons")
    #
    #     for det in detections:
    #         print(f"  - {det.template_name} at {det.position} "
    #               f"(confidence: {det.confidence:.2f})")
    #
    #     # Save visualization
    #     vis_image = detector.visualize_detections(image, detections)
    #     ImageUtils.save_image(vis_image, "data/processed/example_output.png")


def example_ocr():
    """Example: OCR number recognition."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: OCR Number Recognition")
    print("=" * 60)

    from src.ocr import OCRReader

    # Initialize OCR
    ocr = OCRReader(engine="auto")
    print(f"OCR Engine: {ocr.engine}")

    # If you have an image with numbers
    # image = ImageUtils.load_image("screenshot.png")
    # if image:
    #     # Read all numbers
    #     results = ocr.read_numbers(image)
    #     print(f"Found {len(results)} text regions with numbers")
    #
    #     for result in results:
    #         print(f"  Text: '{result.text}'")
    #         print(f"  Numbers: {result.numbers}")
    #         print(f"  Primary: {result.get_primary_number()}")
    #
    #     # Read number near specific position (e.g., next to an icon)
    #     number_result = ocr.read_number_near_position(
    #         image,
    #         position=(500, 300),  # Icon position
    #         search_size=(100, 50),
    #         direction="right"
    #     )
    #
    #     if number_result:
    #         print(f"\nNumber near position: {number_result.get_primary_number()}")


def example_custom_processing():
    """Example: Custom image processing workflow."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Custom Processing")
    print("=" * 60)

    from src.database import Icon, IconData
    from src.image_processing import IconDetector
    from src.ocr import OCRReader

    # Custom workflow: Process multiple images
    detector = IconDetector()
    ocr = OCRReader()

    image_dir = Path("data/images")
    if image_dir.exists():
        image_files = list(image_dir.glob("*.png")) + list(image_dir.glob("*.jpg"))
        print(f"Found {len(image_files)} images to process")

        # for img_path in image_files:
        #     print(f"\nProcessing: {img_path.name}")
        #     image = ImageUtils.load_image(str(img_path))
        #
        #     if image:
        #         # Detect icons
        #         detections = detector.detect_icons(image)
        #
        #         # Process each detection
        #         for det in detections:
        #             # Read number near icon
        #             ocr_result = ocr.read_number_near_position(
        #                 image, det.position
        #             )
        #
        #             # Custom processing logic here
        #             if ocr_result:
        #                 number = ocr_result.get_primary_number()
        #                 print(f"  {det.template_name}: {number}")
    else:
        print(f"Image directory not found: {image_dir}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("BDO-T5 Icon Recognition System - Usage Examples")
    print("=" * 60)

    try:
        example_full_workflow()
        example_database_queries()
        example_icon_detection()
        example_ocr()
        example_custom_processing()

        print("\n" + "=" * 60)
        print("Examples completed!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Add icon templates to data/templates/")
        print("2. Place screenshots in data/images/")
        print("3. Run: python src/main.py process --image data/images/your_screenshot.png")
        print("4. Check results: python src/main.py stats")

    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
