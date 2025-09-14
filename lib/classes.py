from dataclasses import dataclass
from lib.utils import get_dirs
import json
from typing import Optional, Dict, Any, Union
from pathlib import Path

@dataclass
class Project:
    name: str
    directory: Union[Path, None] = None
    config_path: Union[Path, None] = None
    config_data: Optional[Dict[str, Any]] = None
    def __post_init__(self):
        self.directory = Path('storage') / self.name
        self.config_path = self.directory / 'config.json'
        with open(self.config_path, "r") as file:
            self.config_data = json.load(file)

    def get_scrape_dirs(self) -> list[Path]:
        return get_dirs(self.directory)


@dataclass
class Scrape:
    project: Project
    name: str
    directory: Union[Path, None] = None
    csv_path: Union[Path, None] = None
    yaml_dir: Union[Path, None] = None
    db_created_flag_file_path: Union[Path, None] = None
    def __post_init__(self):
        self.directory = Path(self.project.directory) / self.name
        self.csv_path = self.directory / 'scrape.csv'
        self.yaml_dir = self.directory / "yaml"
        self.db_created_flag_file_path = self.directory / "db_created_flag.txt"
