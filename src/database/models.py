"""
Data models for the BDO-T5 Icon Recognition System.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Icon:
    """Represents an icon detected in an image."""

    id: Optional[int] = None
    name: str = ""
    icon_hash: str = ""  # Hash of the icon image for matching
    category: str = ""  # e.g., "item", "skill", "buff", "enhancement"
    image_path: str = ""  # Path to the template image
    confidence_threshold: float = 0.8
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        """Convert Icon to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'icon_hash': self.icon_hash,
            'category': self.category,
            'image_path': self.image_path,
            'confidence_threshold': self.confidence_threshold,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class IconData:
    """Represents detected icon data with associated numbers from game screenshots."""

    id: Optional[int] = None
    icon_id: int = 0  # Foreign key to Icon
    detected_number: Optional[int] = None  # Number detected near the icon (quantity, level, etc.)
    detected_text: str = ""  # Any text detected near the icon
    source_image_path: str = ""  # Path to the source screenshot
    position_x: int = 0  # X coordinate where icon was found
    position_y: int = 0  # Y coordinate where icon was found
    confidence: float = 0.0  # Detection confidence score
    timestamp: Optional[datetime] = None  # When this was detected
    notes: str = ""  # Additional notes or metadata

    def to_dict(self):
        """Convert IconData to dictionary."""
        return {
            'id': self.id,
            'icon_id': self.icon_id,
            'detected_number': self.detected_number,
            'detected_text': self.detected_text,
            'source_image_path': self.source_image_path,
            'position_x': self.position_x,
            'position_y': self.position_y,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'notes': self.notes,
        }
