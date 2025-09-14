import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from pathlib import Path




def get_sitemap_urls(url: str) -> list[str]:
    """Extract URLs from a sitemap XML file."""
    resp = requests.get(url + '/sitemap.xml')
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    # grab every <loc> that starts with your site
    return [
        loc.text
        for loc in root.findall(".//{*}loc")
        if loc.text and loc.text.startswith(url)
    ]


def url_to_filename(url: str) -> str:
    """Convert URL path to a safe filename."""
    # turn path /foo/bar/ into "aacg_foo_bar.yaml", root -> "aacg_home.yaml"
    path = urlparse(url).path.strip("/").replace("/", "_")
    safe = path or "home"
    return f"{safe}.yaml"


def get_dirs(parent_dir:Path) -> list[Path]:
    try:
        items = parent_dir.iterdir()
        subdirectories = [
            item for item in items if item.is_dir()
        ]
        return sorted(subdirectories, key=lambda f: f.stat().st_mtime, reverse=True)
    except FileNotFoundError:
        print(f"Directory '{parent_dir}' not found.")
        return []
    except PermissionError:
        print(f"Permission denied to access '{parent_dir}'.")
        return []


