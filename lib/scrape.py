from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Union, Tuple

def get_scrape_dir(name: Path) -> Tuple[Path, Path]:
    """Get the directory where scrape files are stored."""
    parent_dir = Path('storage') / name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    scrape_dir = parent_dir / ('scrape_' + timestamp) / 'yaml'
    return (parent_dir, scrape_dir)

