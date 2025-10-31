"""Blacklist management for wallpapers."""
import sqlite3
from pathlib import Path
from enum import Enum

from .config import WALLPAPER_FOLDER


class BlacklistReason(Enum):
    """Reasons for blacklisting a wallpaper."""
    TOO_SMALL = "TOO_SMALL"
    DELETED = "DELETED"
    BORING_BACKGROUND = "BORING_BACKGROUND"


class BlacklistDB:
    """Database for tracking blacklisted wallpapers."""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = WALLPAPER_FOLDER / ".blacklist.db"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS blacklist (
                    filename TEXT PRIMARY KEY,
                    reason TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def add(self, filename, reason):
        """Add a file to the blacklist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO blacklist (filename, reason) VALUES (?, ?)",
                (filename, reason.value if isinstance(reason, BlacklistReason) else reason)
            )
            conn.commit()
    
    def is_blacklisted(self, filename):
        """Check if a file is blacklisted."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT 1 FROM blacklist WHERE filename = ?",
                (filename,)
            )
            return cursor.fetchone() is not None
    
    def get_reason(self, filename):
        """Get the reason a file was blacklisted."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT reason FROM blacklist WHERE filename = ?",
                (filename,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
    
    def list_all(self):
        """List all blacklisted files with reasons."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT filename, reason, timestamp FROM blacklist ORDER BY timestamp DESC"
            )
            return cursor.fetchall()
