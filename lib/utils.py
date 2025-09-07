import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse




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



