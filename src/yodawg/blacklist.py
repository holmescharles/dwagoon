"""Blacklist management for wallpapers."""
import csv
from pathlib import Path
from enum import Enum
from datetime import datetime


class BlacklistReason(Enum):
    """Reasons for blacklisting a wallpaper."""
    TOO_SMALL = "TOO_SMALL"
    DELETED = "DELETED"
    BORING_BACKGROUND = "BORING_BACKGROUND"


class BlacklistDB:
    """CSV-based storage for tracking blacklisted wallpapers.
    
    Uses a simple CSV file format: filename,reason,timestamp
    Each line represents one blacklisted file.
    """
    
    def __init__(self, csv_path=None):
        if csv_path is None:
            # Use ~/.cache/yodawg/blacklist.csv as default
            cache_dir = Path.home() / ".cache" / "yodawg"
            csv_path = cache_dir / "blacklist.csv"
        
        self.csv_path = Path(csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create file with header if it doesn't exist
        if not self.csv_path.exists():
            self._init_csv()
    
    def _init_csv(self):
        """Initialize the CSV file with header."""
        with open(self.csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['filename', 'reason', 'timestamp'])
    
    def _load_data(self):
        """Load all blacklist data from CSV into a dictionary."""
        data = {}
        try:
            with open(self.csv_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data[row['filename']] = {
                        'reason': row['reason'],
                        'timestamp': row['timestamp']
                    }
        except FileNotFoundError:
            self._init_csv()
        return data
    
    def _save_data(self, data):
        """Save all blacklist data from dictionary to CSV."""
        with open(self.csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['filename', 'reason', 'timestamp'])
            for filename, info in data.items():
                writer.writerow([filename, info['reason'], info['timestamp']])
    
    def add(self, filename, reason):
        """Add a file to the blacklist."""
        data = self._load_data()
        reason_str = reason.value if isinstance(reason, BlacklistReason) else reason
        timestamp = datetime.now().isoformat()
        
        # Update or add entry
        data[filename] = {'reason': reason_str, 'timestamp': timestamp}
        self._save_data(data)
    
    def is_blacklisted(self, filename):
        """Check if a file is blacklisted."""
        data = self._load_data()
        return filename in data
    
    def get_reason(self, filename):
        """Get the reason a file was blacklisted."""
        data = self._load_data()
        if filename in data:
            return data[filename]['reason']
        return None
    
    def list_all(self):
        """List all blacklisted files with reasons as tuples (filename, reason, timestamp)."""
        data = self._load_data()
        # Sort by timestamp descending
        sorted_items = sorted(
            data.items(), 
            key=lambda x: x[1]['timestamp'], 
            reverse=True
        )
        return [(filename, info['reason'], info['timestamp']) 
                for filename, info in sorted_items]
