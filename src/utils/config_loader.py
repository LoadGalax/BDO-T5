"""
Configuration loader utility.
"""

from pathlib import Path
from typing import Any, Dict

import yaml


class ConfigLoader:
    """Loads and manages configuration from YAML file."""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize configuration loader.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Load configuration from file."""
        if not self.config_path.exists():
            print(f"Warning: Config file not found at {self.config_path}")
            self.config = self._get_default_config()
            return

        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            print(f"Configuration loaded from {self.config_path}")
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
            self.config = self._get_default_config()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key (supports dot notation, e.g., "database.path")
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration.

        Returns:
            Default configuration dictionary
        """
        return {
            'database': {
                'path': 'data/bdo_icons.db'
            },
            'image_processing': {
                'template_dir': 'data/templates',
                'confidence_threshold': 0.8,
                'multi_scale_detection': True,
                'scales': [0.8, 0.9, 1.0, 1.1, 1.2]
            },
            'ocr': {
                'engine': 'auto',
                'language': 'en',
                'preprocess': True,
                'number_search_region': {
                    'width': 100,
                    'height': 50
                },
                'default_direction': 'right'
            },
            'processing': {
                'max_image_width': 1920,
                'max_image_height': 1080,
                'save_visualizations': True,
                'visualization_dir': 'data/processed'
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/bdo_t5.log',
                'console_output': True
            }
        }
