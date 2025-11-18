# BDO-T5 Icon Recognition System

A Python-based Black Desert Online (BDO) assistant that uses computer vision and OCR to identify game icons and extract associated numbers from screenshots, storing the data in a SQLite database.

## Features

- **Icon Detection**: Template matching with multi-scale detection
- **OCR Number Recognition**: Extract numbers and text near detected icons
- **Database Storage**: SQLite database with automatic upsert functionality
- **Flexible Configuration**: YAML-based configuration system
- **Visualization**: Generate annotated images showing detected icons
- **Multiple OCR Engines**: Support for Pytesseract and EasyOCR

## Project Structure

```
BDO-T5/
├── src/
│   ├── database/           # Database models and manager
│   ├── image_processing/   # Icon detection and image utilities
│   ├── ocr/               # OCR and number recognition
│   ├── utils/             # Configuration loader and utilities
│   └── main.py            # Main application entry point
├── data/
│   ├── images/            # Source images (gitignored)
│   ├── templates/         # Icon template images
│   └── processed/         # Visualization outputs (gitignored)
├── config/
│   └── config.yaml        # Configuration file
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR (optional, for Pytesseract engine)

### Install Tesseract (Optional)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

### Install Python Dependencies

```bash
# Clone the repository
git clone https://github.com/LoadGalax/BDO-T5.git
cd BDO-T5

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Add Icon Templates

Before processing images, you need to add icon templates to recognize. Place your icon template images in the `data/templates/` directory.

**Organize by category (optional):**
```
data/templates/
├── items/
│   ├── health_potion.png
│   └── mana_potion.png
├── skills/
│   ├── fireball.png
│   └── shield.png
└── general/
    └── gold_icon.png
```

**Or add via command line:**
```bash
python src/main.py add-template --image path/to/icon.png --name "health_potion" --category "items"
```

### 2. Process an Image

```bash
python src/main.py process --image path/to/screenshot.png
```

This will:
1. Detect all matching icons in the image
2. Extract numbers near each detected icon
3. Store results in the database
4. Save a visualization to `data/processed/`

### 3. View Statistics

```bash
python src/main.py stats
```

### 4. List Templates

```bash
python src/main.py list
```

## Usage Examples

### Process a Game Screenshot

```bash
# Process with visualization
python src/main.py process --image screenshots/inventory.png

# Process without visualization
python src/main.py process --image screenshots/inventory.png --no-viz
```

### Add a New Icon Template

```bash
python src/main.py add-template \
  --image templates/red_potion.png \
  --name "red_potion" \
  --category "consumables"
```

### View Database Statistics

```bash
python src/main.py stats
```

Output example:
```
Database Statistics:
------------------------------------------------------------
Total Icons: 15
Total Detections: 342
Categories: 3

Icons by Category:
  consumables: 8
  items: 5
  skills: 2
```

## Configuration

Edit `config/config.yaml` to customize settings:

```yaml
# Database settings
database:
  path: "data/bdo_icons.db"

# Image processing settings
image_processing:
  template_dir: "data/templates"
  confidence_threshold: 0.8  # 0.0 to 1.0
  multi_scale_detection: true

# OCR settings
ocr:
  engine: "auto"  # "auto", "pytesseract", or "easyocr"
  language: "en"
  number_search_region:
    width: 100   # Pixels to search for numbers
    height: 50
  default_direction: "right"  # Where to look relative to icon

# Processing settings
processing:
  max_image_width: 1920
  max_image_height: 1080
  save_visualizations: true
```

## Python API Usage

You can also use the system programmatically:

```python
from src.main import BDOIconRecognizer

# Initialize
app = BDOIconRecognizer("config/config.yaml")

# Process an image
results = app.process_image("screenshot.png")

# Access detection results
for icon_data in results:
    print(f"Icon: {icon_data.icon_id}")
    print(f"Number: {icon_data.detected_number}")
    print(f"Position: ({icon_data.position_x}, {icon_data.position_y})")
    print(f"Confidence: {icon_data.confidence}")

# Add a template
app.add_template("new_icon.png", "my_icon", "items")

# Show statistics
app.show_statistics()

# Close when done
app.close()
```

### Direct Database Access

```python
from src.database import DatabaseManager

# Open database
db = DatabaseManager("data/bdo_icons.db")

# Get all icons
icons = db.get_all_icons()

# Get recent detections
recent = db.get_recent_icon_data(limit=10)

# Get icons by category
consumables = db.get_icons_by_category("consumables")

# Get detection statistics
stats = db.get_statistics()

# Close connection
db.close()
```

### Icon Detection Only

```python
from src.image_processing import IconDetector, ImageUtils

# Initialize detector
detector = IconDetector("data/templates", confidence_threshold=0.8)

# Load image
image = ImageUtils.load_image("screenshot.png")

# Detect icons
detections = detector.detect_icons(image)

# Process results
for det in detections:
    print(f"Found: {det.template_name}")
    print(f"Position: {det.position}")
    print(f"Confidence: {det.confidence}")

# Visualize
vis_image = detector.visualize_detections(image, detections)
ImageUtils.save_image(vis_image, "output.png")
```

### OCR Only

```python
from src.ocr import OCRReader
from src.image_processing import ImageUtils

# Initialize OCR
ocr = OCRReader(engine="easyocr")

# Load image
image = ImageUtils.load_image("screenshot.png")

# Read all text
results = ocr.read_text(image)

# Read only numbers
number_results = ocr.read_numbers(image)

# Read specific region
region_results = ocr.read_region(image, (100, 100, 200, 50))

# Find numbers near a position
number = ocr.read_number_near_position(
    image,
    position=(500, 300),
    search_size=(100, 50),
    direction="right"
)

if number:
    print(f"Number: {number.get_primary_number()}")
```

## Database Schema

### Icons Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Icon name |
| icon_hash | TEXT | Unique hash of icon image |
| category | TEXT | Icon category |
| image_path | TEXT | Path to template image |
| confidence_threshold | REAL | Detection confidence threshold |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### Icon Data Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| icon_id | INTEGER | Foreign key to icons table |
| detected_number | INTEGER | Detected number near icon |
| detected_text | TEXT | Detected text near icon |
| source_image_path | TEXT | Source screenshot path |
| position_x | INTEGER | X coordinate of detection |
| position_y | INTEGER | Y coordinate of detection |
| confidence | REAL | Detection confidence |
| timestamp | TIMESTAMP | Detection timestamp |
| notes | TEXT | Additional notes |

## How It Works

### 1. Icon Detection

The system uses template matching with OpenCV to detect icons:

- **Multi-scale Detection**: Searches for icons at different scales (0.8x to 1.2x)
- **Template Matching**: Uses normalized cross-correlation
- **Non-Maximum Suppression**: Removes duplicate detections
- **Confidence Filtering**: Only returns matches above threshold

### 2. Number Recognition

OCR is applied to regions near detected icons:

- **Preprocessing**: Adaptive thresholding and denoising
- **Region Selection**: Searches configurable region near icon
- **Number Extraction**: Extracts numeric values from text
- **Multiple Engines**: Supports Pytesseract and EasyOCR

### 3. Database Storage

Results are automatically stored:

- **Upsert Logic**: Updates existing icons or creates new ones
- **Historical Tracking**: All detections are logged with timestamps
- **Relational Structure**: Icons and detections are properly linked

## Troubleshooting

### Common Issues

**"No templates loaded"**
- Make sure you have icon images in `data/templates/`
- Supported formats: PNG, JPG, JPEG, BMP

**"OCR engine not available"**
- Install Tesseract for Pytesseract engine
- Or let it use EasyOCR (downloads models automatically)

**Low detection accuracy**
- Adjust `confidence_threshold` in config (lower = more detections)
- Ensure template images closely match in-game icons
- Try different scales in `multi_scale_detection`

**Numbers not detected**
- Adjust `number_search_region` size in config
- Try different `default_direction` (right, left, top, bottom)
- Check OCR preprocessing in visualization output

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines.

```bash
# Format code
black src/

# Check style
flake8 src/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is for educational and personal use.

## Acknowledgments

- OpenCV for computer vision capabilities
- Tesseract OCR and EasyOCR for text recognition
- Black Desert Online community

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Happy Icon Hunting!** 🎮
