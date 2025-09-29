import os
from datetime import datetime

def get_today_date_str():
    """Returns the current date as a 'YYYY-MM-DD' string."""
    return datetime.now().strftime('%Y-%m-%d')

def ensure_dir_exists(directory_path):
    """Ensures that a directory exists, creating it if necessary."""
    if not os.path.exists(directory_path):
        print(f"Creating directory: {directory_path}")
        os.makedirs(directory_path)