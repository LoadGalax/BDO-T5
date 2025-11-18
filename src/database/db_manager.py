"""
Database Manager for BDO-T5 Icon Recognition System.
Handles all SQLite database operations including schema creation and CRUD operations.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from .models import Icon, IconData


class DatabaseManager:
    """Manages SQLite database operations for icon and detection data."""

    def __init__(self, db_path: str = "data/bdo_icons.db"):
        """
        Initialize database manager.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self._initialize_database()

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def _initialize_database(self):
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Create icons table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS icons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                icon_hash TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                image_path TEXT,
                confidence_threshold REAL DEFAULT 0.8,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create icon_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS icon_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                icon_id INTEGER NOT NULL,
                detected_number INTEGER,
                detected_text TEXT,
                source_image_path TEXT NOT NULL,
                position_x INTEGER NOT NULL,
                position_y INTEGER NOT NULL,
                confidence REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (icon_id) REFERENCES icons (id) ON DELETE CASCADE
            )
        """)

        # Create indexes for better query performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_icon_hash
            ON icons(icon_hash)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_icon_category
            ON icons(category)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_icon_data_icon_id
            ON icon_data(icon_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_icon_data_timestamp
            ON icon_data(timestamp)
        """)

        conn.commit()

    # ==================== ICON CRUD OPERATIONS ====================

    def add_icon(self, icon: Icon) -> int:
        """
        Add a new icon to the database.

        Args:
            icon: Icon object to add

        Returns:
            ID of the newly created icon

        Raises:
            sqlite3.IntegrityError: If icon_hash already exists
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO icons (name, icon_hash, category, image_path, confidence_threshold)
            VALUES (?, ?, ?, ?, ?)
        """, (icon.name, icon.icon_hash, icon.category, icon.image_path, icon.confidence_threshold))

        conn.commit()
        return cursor.lastrowid

    def get_icon_by_id(self, icon_id: int) -> Optional[Icon]:
        """
        Get icon by ID.

        Args:
            icon_id: Icon ID

        Returns:
            Icon object or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM icons WHERE id = ?", (icon_id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_icon(row)
        return None

    def get_icon_by_hash(self, icon_hash: str) -> Optional[Icon]:
        """
        Get icon by hash.

        Args:
            icon_hash: Hash of the icon image

        Returns:
            Icon object or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM icons WHERE icon_hash = ?", (icon_hash,))
        row = cursor.fetchone()

        if row:
            return self._row_to_icon(row)
        return None

    def get_icons_by_category(self, category: str) -> List[Icon]:
        """
        Get all icons in a category.

        Args:
            category: Icon category

        Returns:
            List of Icon objects
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM icons WHERE category = ?", (category,))
        rows = cursor.fetchall()

        return [self._row_to_icon(row) for row in rows]

    def get_all_icons(self) -> List[Icon]:
        """
        Get all icons from the database.

        Returns:
            List of Icon objects
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM icons ORDER BY category, name")
        rows = cursor.fetchall()

        return [self._row_to_icon(row) for row in rows]

    def update_icon(self, icon: Icon) -> bool:
        """
        Update an existing icon.

        Args:
            icon: Icon object with updated data (must have id set)

        Returns:
            True if updated, False if icon not found
        """
        if icon.id is None:
            raise ValueError("Icon ID must be set for update operation")

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE icons
            SET name = ?, icon_hash = ?, category = ?, image_path = ?,
                confidence_threshold = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (icon.name, icon.icon_hash, icon.category, icon.image_path,
              icon.confidence_threshold, icon.id))

        conn.commit()
        return cursor.rowcount > 0

    def delete_icon(self, icon_id: int) -> bool:
        """
        Delete an icon and all associated data.

        Args:
            icon_id: Icon ID to delete

        Returns:
            True if deleted, False if icon not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM icons WHERE id = ?", (icon_id,))
        conn.commit()
        return cursor.rowcount > 0

    # ==================== ICON DATA CRUD OPERATIONS ====================

    def add_icon_data(self, icon_data: IconData) -> int:
        """
        Add detected icon data to the database.

        Args:
            icon_data: IconData object to add

        Returns:
            ID of the newly created record
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO icon_data
            (icon_id, detected_number, detected_text, source_image_path,
             position_x, position_y, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (icon_data.icon_id, icon_data.detected_number, icon_data.detected_text,
              icon_data.source_image_path, icon_data.position_x, icon_data.position_y,
              icon_data.confidence, icon_data.notes))

        conn.commit()
        return cursor.lastrowid

    def get_icon_data_by_id(self, data_id: int) -> Optional[IconData]:
        """
        Get icon data by ID.

        Args:
            data_id: IconData ID

        Returns:
            IconData object or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM icon_data WHERE id = ?", (data_id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_icon_data(row)
        return None

    def get_icon_data_by_icon_id(self, icon_id: int, limit: int = 100) -> List[IconData]:
        """
        Get all detection data for a specific icon.

        Args:
            icon_id: Icon ID
            limit: Maximum number of records to return

        Returns:
            List of IconData objects
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM icon_data
            WHERE icon_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (icon_id, limit))
        rows = cursor.fetchall()

        return [self._row_to_icon_data(row) for row in rows]

    def get_recent_icon_data(self, limit: int = 50) -> List[IconData]:
        """
        Get most recent icon detection data.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of IconData objects
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM icon_data
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()

        return [self._row_to_icon_data(row) for row in rows]

    def update_icon_data(self, icon_data: IconData) -> bool:
        """
        Update existing icon data.

        Args:
            icon_data: IconData object with updated data (must have id set)

        Returns:
            True if updated, False if not found
        """
        if icon_data.id is None:
            raise ValueError("IconData ID must be set for update operation")

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE icon_data
            SET icon_id = ?, detected_number = ?, detected_text = ?,
                source_image_path = ?, position_x = ?, position_y = ?,
                confidence = ?, notes = ?
            WHERE id = ?
        """, (icon_data.icon_id, icon_data.detected_number, icon_data.detected_text,
              icon_data.source_image_path, icon_data.position_x, icon_data.position_y,
              icon_data.confidence, icon_data.notes, icon_data.id))

        conn.commit()
        return cursor.rowcount > 0

    def delete_icon_data(self, data_id: int) -> bool:
        """
        Delete icon data record.

        Args:
            data_id: IconData ID to delete

        Returns:
            True if deleted, False if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM icon_data WHERE id = ?", (data_id,))
        conn.commit()
        return cursor.rowcount > 0

    # ==================== UPSERT OPERATIONS ====================

    def upsert_icon(self, icon: Icon) -> Tuple[int, bool]:
        """
        Insert or update icon based on icon_hash.

        Args:
            icon: Icon object

        Returns:
            Tuple of (icon_id, was_created)
            - icon_id: ID of the icon
            - was_created: True if new icon was created, False if updated
        """
        existing_icon = self.get_icon_by_hash(icon.icon_hash)

        if existing_icon:
            # Update existing icon
            icon.id = existing_icon.id
            self.update_icon(icon)
            return existing_icon.id, False
        else:
            # Create new icon
            icon_id = self.add_icon(icon)
            return icon_id, True

    # ==================== UTILITY METHODS ====================

    def get_statistics(self) -> dict:
        """
        Get database statistics.

        Returns:
            Dictionary with statistics
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as count FROM icons")
        icon_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM icon_data")
        data_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(DISTINCT category) as count FROM icons")
        category_count = cursor.fetchone()['count']

        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM icons
            GROUP BY category
        """)
        categories = {row['category']: row['count'] for row in cursor.fetchall()}

        return {
            'total_icons': icon_count,
            'total_detections': data_count,
            'categories_count': category_count,
            'icons_by_category': categories
        }

    def _row_to_icon(self, row: sqlite3.Row) -> Icon:
        """Convert database row to Icon object."""
        return Icon(
            id=row['id'],
            name=row['name'],
            icon_hash=row['icon_hash'],
            category=row['category'],
            image_path=row['image_path'],
            confidence_threshold=row['confidence_threshold'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
        )

    def _row_to_icon_data(self, row: sqlite3.Row) -> IconData:
        """Convert database row to IconData object."""
        return IconData(
            id=row['id'],
            icon_id=row['icon_id'],
            detected_number=row['detected_number'],
            detected_text=row['detected_text'],
            source_image_path=row['source_image_path'],
            position_x=row['position_x'],
            position_y=row['position_y'],
            confidence=row['confidence'],
            timestamp=datetime.fromisoformat(row['timestamp']) if row['timestamp'] else None,
            notes=row['notes']
        )

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
