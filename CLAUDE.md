# CLAUDE.md - AI Assistant Guide for BDO-T5

**Last Updated:** 2025-11-18
**Repository:** LoadGalax/BDO-T5
**Current State:** Active development - Core functionality complete

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Development Workflow](#development-workflow)
4. [Git Conventions](#git-conventions)
5. [Code Conventions](#code-conventions)
6. [AI Assistant Guidelines](#ai-assistant-guidelines)
7. [Testing Strategy](#testing-strategy)
8. [Deployment](#deployment)
9. [Common Tasks](#common-tasks)

---

## Project Overview

### What is BDO-T5?

BDO-T5 is a Black Desert Online helper application that uses computer vision and OCR (Optical Character Recognition) to automatically identify game icons and extract associated numbers from screenshots. The system stores detected data in a SQLite database for tracking and analysis.

### Current Project State

- **Status:** Core functionality complete and ready for use
- **Primary Language:** Python 3.8+
- **Framework/Stack:**
  - Computer Vision: OpenCV
  - OCR: Pytesseract / EasyOCR
  - Database: SQLite3
  - Configuration: YAML
- **Dependencies:** Fully configured (see requirements.txt)

### Project Goals

1. **Icon Recognition**: Automatically detect and identify BDO icons in screenshots using template matching
2. **Number Extraction**: Use OCR to extract quantities, levels, or other numeric data associated with icons
3. **Data Storage**: Maintain a historical database of detected icons and their values
4. **Extensibility**: Allow easy addition of new icon templates and categories
5. **Automation**: Enable tracking of in-game resources, inventory, and progression over time

---

## Repository Structure

```
BDO-T5/
├── src/                           # Source code
│   ├── database/                  # Database layer
│   │   ├── __init__.py           # Database module exports
│   │   ├── models.py             # Icon and IconData models
│   │   └── db_manager.py         # DatabaseManager with CRUD operations
│   ├── image_processing/          # Computer vision
│   │   ├── __init__.py           # Image processing exports
│   │   ├── icon_detector.py      # IconDetector class for template matching
│   │   └── image_utils.py        # ImageUtils for preprocessing
│   ├── ocr/                       # OCR and text recognition
│   │   ├── __init__.py           # OCR module exports
│   │   └── ocr_reader.py         # OCRReader with multiple engine support
│   ├── utils/                     # Utilities
│   │   ├── __init__.py           # Utils exports
│   │   └── config_loader.py      # ConfigLoader for YAML config
│   ├── __init__.py               # Package metadata
│   └── main.py                   # Main application entry point
├── data/                          # Data directory (gitignored)
│   ├── images/                   # Source screenshots
│   ├── templates/                # Icon template images (by category)
│   └── processed/                # Visualization outputs
├── config/                        # Configuration
│   └── config.yaml               # Main configuration file
├── tests/                         # Test files (to be added)
├── requirements.txt               # Python dependencies
├── example_usage.py               # Usage examples and demonstrations
├── README.md                      # Project documentation
├── CLAUDE.md                      # This file - AI assistant guide
└── .gitignore                    # Git ignore rules
```

---

## Development Workflow

### Branch Strategy

This repository uses feature branches with the `claude/` prefix:

- **Branch naming:** `claude/<feature-description>-<session-id>`
- **Current branch:** `claude/claude-md-mi4618d3oigvdms2-01Wo4GXG7zc7js6MyoQJ1d2a`
- **Previous branches:**
  - `claude/black-desert-image-assistant-018uLdrjPMCQEqJrKbngYWse`

### Development Process

1. **Branch Creation:** Create feature branches from the main branch
2. **Development:** Make changes on the feature branch
3. **Commit:** Use descriptive commit messages
4. **Push:** Push to origin with `git push -u origin <branch-name>`
5. **PR Creation:** Create pull request when feature is complete
6. **Code Review:** (If applicable) Review before merging
7. **Merge:** Merge to main branch after approval

---

## Git Conventions

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples:**
```
feat(model): add T5 model integration
fix(data): resolve data loading issue
docs(readme): update installation instructions
```

### Branch Naming

- Feature branches: `claude/<feature-description>-<session-id>`
- All development branches must start with `claude/` prefix
- Use kebab-case for descriptions
- Session IDs are automatically appended

### Git Operations Best Practices

**Pushing:**
```bash
git push -u origin <branch-name>
```
- Always use `-u` flag for first push
- Retry up to 4 times with exponential backoff on network errors (2s, 4s, 8s, 16s)
- Branch must start with `claude/` or push will fail with 403

**Fetching:**
```bash
git fetch origin <branch-name>
git pull origin <branch-name>
```
- Prefer fetching specific branches
- Retry up to 4 times on network failures

---

## Code Conventions

### General Principles

1. **Readability:** Code should be self-documenting
2. **Modularity:** Keep functions/classes focused and single-purpose
3. **DRY:** Don't Repeat Yourself
4. **KISS:** Keep It Simple, Stupid
5. **Security:** Always consider security implications (avoid XSS, SQL injection, command injection, etc.)

### Python Conventions (if applicable)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 88 characters (Black formatter)
- Use docstrings for functions and classes
- Use `snake_case` for variables and functions
- Use `PascalCase` for classes

### JavaScript/TypeScript Conventions (if applicable)

- Follow Airbnb style guide or similar
- Use ESLint and Prettier
- Use `camelCase` for variables and functions
- Use `PascalCase` for classes and components
- Use `UPPER_CASE` for constants
- Prefer `const` over `let`, avoid `var`

### File Naming

- Use lowercase with hyphens for file names: `model-loader.py`
- Test files: `test_<module_name>.py` or `<module_name>.test.js`
- Config files: Clear, descriptive names

---

## AI Assistant Guidelines

### When Working on This Repository

1. **Always Check Current State:**
   - Run `git status` before making changes
   - Check current branch with `git branch`
   - Verify you're on the correct feature branch

2. **Use Todo Lists:**
   - For multi-step tasks, use the TodoWrite tool
   - Break down complex tasks into smaller steps
   - Mark tasks as completed immediately after finishing

3. **Code Quality:**
   - Never introduce security vulnerabilities
   - Write clean, maintainable code
   - Add comments for complex logic
   - Follow established conventions

4. **Git Operations:**
   - Commit related changes together
   - Write descriptive commit messages
   - Push to the correct branch
   - Never force push without explicit user permission

5. **Documentation:**
   - Update CLAUDE.md when project structure changes
   - Keep README.md current
   - Document new features and APIs
   - Add inline comments for complex code

6. **Testing:**
   - Write tests for new features
   - Run existing tests before committing
   - Fix failing tests immediately

### Common Pitfalls to Avoid

- ❌ Don't commit without clear commit messages
- ❌ Don't push to wrong branches
- ❌ Don't create files unnecessarily (prefer editing existing)
- ❌ Don't ignore security vulnerabilities
- ❌ Don't use emojis unless explicitly requested
- ❌ Don't create documentation files unless necessary
- ❌ Don't skip the TodoWrite tool for complex tasks

### Helpful Commands

```bash
# Check repository status
git status
git log --oneline --graph | head -20

# Branch management
git branch -a
git checkout -b <branch-name>

# View changes
git diff
git diff --staged

# Explore codebase (use appropriate tools)
# For file search: Use Glob tool
# For content search: Use Grep tool
# For reading files: Use Read tool
# For editing files: Use Edit tool
```

---

## Key Modules and Components

### Database Module (`src/database/`)

**Purpose:** Manages all SQLite database operations for storing icons and detection data.

**Key Classes:**
- `Icon`: Data model representing an icon template with metadata
- `IconData`: Data model representing a detection instance with position, confidence, and extracted data
- `DatabaseManager`: Handles all CRUD operations and database initialization

**Key Features:**
- Automatic schema creation with indexes
- Upsert operations (insert or update based on icon hash)
- Foreign key relationships between icons and detection data
- Query methods for retrieving by category, hash, or recent detections
- Statistics generation

**Usage Notes:**
- Always use context manager (`with DatabaseManager() as db:`) or manually call `close()`
- Icon hashes are unique identifiers computed from image content
- Database path is configurable via `config.yaml`

### Image Processing Module (`src/image_processing/`)

**Purpose:** Handles icon detection using template matching and image preprocessing.

**Key Classes:**
- `IconDetector`: Performs template matching to find icons in images
- `ImageUtils`: Utility functions for image loading, preprocessing, and manipulation
- `Detection`: Data class representing a single icon detection result

**Key Features:**
- Multi-scale template matching (searches at different sizes)
- Non-maximum suppression to remove duplicate detections
- Configurable confidence thresholds
- Support for template categories and organization
- Visualization capabilities

**Usage Notes:**
- Templates should be placed in `data/templates/` organized by category
- Supported image formats: PNG, JPG, JPEG, BMP
- Multi-scale detection improves accuracy but increases processing time
- Template images should closely match in-game icon appearance

### OCR Module (`src/ocr/`)

**Purpose:** Extracts text and numbers from images using OCR engines.

**Key Classes:**
- `OCRReader`: Main OCR interface supporting multiple engines
- `OCRResult`: Data class representing OCR detection with text, numbers, and confidence

**Key Features:**
- Support for Pytesseract and EasyOCR engines
- Automatic engine selection ("auto" mode)
- Image preprocessing for better OCR accuracy
- Region-based OCR for targeted extraction
- Number extraction from mixed text
- Position-relative number detection (e.g., number to the right of an icon)

**Usage Notes:**
- Pytesseract requires Tesseract OCR to be installed on the system
- EasyOCR downloads models automatically on first run (~100MB)
- Preprocessing significantly improves number recognition accuracy
- Configure search regions in `config.yaml` for optimal results

### Main Application (`src/main.py`)

**Purpose:** Command-line interface and workflow orchestration.

**Key Class:**
- `BDOIconRecognizer`: Main application class that coordinates all modules

**Commands:**
- `process`: Process an image to detect icons and numbers
- `add-template`: Add a new icon template to the system
- `list`: List all loaded templates
- `stats`: Display database statistics

**Workflow:**
1. Load configuration
2. Initialize database, detector, and OCR
3. Process image: detect icons → extract numbers → store in database
4. Optionally save visualization

### Configuration (`config/config.yaml`)

**Purpose:** Centralized configuration for all system parameters.

**Key Sections:**
- `database`: Database file path
- `image_processing`: Template directory, confidence thresholds, scale settings
- `ocr`: Engine selection, language, search regions
- `processing`: Image size limits, visualization settings

**Configuration Loading:**
- Uses `ConfigLoader` class with dot-notation access (`config.get('database.path')`)
- Falls back to defaults if config file missing
- Supports YAML format for readability

---

## Testing Strategy

### Test Framework

**Framework:** pytest with pytest-cov for coverage

**Setup:**
```bash
pip install pytest pytest-cov
pytest tests/
```

### Test Coverage

- Aim for >80% code coverage
- Focus on critical paths and edge cases
- Test both success and failure scenarios

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_database.py

# Run with verbose output
pytest -v tests/
```

### Test Organization

- `tests/test_database.py`: Database CRUD operations and queries
- `tests/test_image_processing.py`: Icon detection and image utilities
- `tests/test_ocr.py`: OCR functionality and number extraction
- `tests/test_integration.py`: End-to-end workflow tests

**Note:** Tests are not yet implemented. When adding tests:
- Use pytest fixtures for database and detector setup
- Mock external dependencies (file I/O, OCR engines)
- Test both success and failure scenarios
- Aim for >80% code coverage

---

## Deployment

### Environment Setup

This is a local Python application with no deployment pipeline. Users run it directly on their machines.

**Installation:**
```bash
git clone https://github.com/LoadGalax/BDO-T5.git
cd BDO-T5
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**System Requirements:**
- Python 3.8 or higher
- Tesseract OCR (optional, for Pytesseract engine)
- 2GB RAM minimum (4GB recommended for EasyOCR)
- Storage: ~500MB for dependencies and models

### Usage

The application is run via command line:

```bash
# Process a screenshot
python src/main.py process --image screenshot.png

# Add a template
python src/main.py add-template --image icon.png --name "health_potion" --category "items"

# View statistics
python src/main.py stats

# List templates
python src/main.py list
```

### Distribution

For sharing with other users:
1. Package with templates: Include common icon templates in `data/templates/`
2. Document template creation process
3. Provide example screenshots for testing
4. Consider creating a setup script for one-command installation

---

## Common Tasks

### Adding a New Feature

1. Create feature branch: `git checkout -b claude/<feature-name>-<session-id>`
2. Use TodoWrite to plan implementation steps
3. Implement feature following code conventions
4. Write/update tests
5. Update documentation
6. Commit changes with descriptive message
7. Push to remote: `git push -u origin <branch-name>`
8. Create pull request (if applicable)

### Fixing a Bug

1. Ensure on correct branch
2. Identify root cause
3. Write test that reproduces bug (if applicable)
4. Fix the bug
5. Verify fix with tests
6. Commit and push

### Updating Documentation

1. Make changes to relevant .md files
2. Update CLAUDE.md if structure changes
3. Commit with `docs:` prefix
4. Push changes

### Refactoring Code

1. Use TodoWrite to plan refactoring steps
2. Ensure tests exist and pass
3. Refactor incrementally
4. Run tests after each change
5. Commit with `refactor:` prefix

---

## Project-Specific Notes

### BDO (Black Desert Online) Context

This project is a helper tool for Black Desert Online players. When working on BDO-related features:

**Game Understanding:**
- BDO is an MMORPG with complex inventory, crafting, and enhancement systems
- Players often need to track resources, items, and progression
- Screenshots contain UI elements with icons and numbers

**Common Use Cases:**
- **Inventory Tracking**: Detect item icons and quantities
- **Enhancement Tracking**: Monitor enhancement levels and materials
- **Market Analysis**: Track prices and availability
- **Crafting Management**: Monitor crafting materials and recipes

**Icon Categories:**
- `items`: General game items (potions, materials, etc.)
- `enhancement`: Enhancement stones, cron stones, etc.
- `currency`: Silver, pearls, special currencies
- `buffs`: Active buffs and effects
- `skills`: Skill icons

### Template Matching Approach

This project uses template matching (not T5 transformers) for icon recognition:

**Why Template Matching:**
- Game icons are consistent and don't change
- Fast and accurate for static icon detection
- No training data or ML models required
- Works well with multi-scale detection

**Best Practices:**
- Crop icon templates precisely (no extra background)
- Use PNG format with transparency when possible
- Organize templates by category
- Test with different game resolutions
- Adjust confidence threshold per icon if needed

### OCR for Numbers

Number extraction is critical for tracking quantities:

**Common Scenarios:**
- Item quantities in inventory (e.g., "x573")
- Enhancement levels (e.g., "+15", "PRI", "DUO")
- Currency amounts (e.g., "1,234,567")
- Buff durations (e.g., "30:00")

**OCR Challenges:**
- Game fonts may be stylized
- Numbers may have decorative backgrounds
- Multiple numbers near same icon
- Different number formats (with/without commas)

**Solutions:**
- Preprocessing with adaptive thresholding
- Configurable search regions per icon
- Primary number selection (largest value)
- Custom number extraction regex patterns

---

## Questions or Issues?

When encountering unclear requirements or ambiguities:

1. **Check existing documentation** in README.md and this file
2. **Ask the user** for clarification using the AskUserQuestion tool
3. **Document assumptions** if proceeding without full clarity
4. **Update this file** when conventions are established

---

## Maintenance

### Updating This Document

This CLAUDE.md file should be updated when:

- Project structure changes significantly
- New conventions are established
- New tools or frameworks are added
- Deployment process is defined
- Testing strategy is implemented

**Responsibility:** Any AI assistant or developer making structural changes should update this file accordingly.

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-18 | 1.0.0 | Initial CLAUDE.md creation |
| 2025-11-18 | 1.1.0 | Updated with complete project details, module documentation, and BDO-specific guidance |

---

## Additional Resources

*To be added as project develops:*

- Project documentation links
- External API documentation
- Related projects
- Research papers (if applicable)
- Community resources

---

**End of CLAUDE.md**
