"""Application configuration loaded from app_config.json."""

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AppConfig:
    imports_dir: str = "imports"
    archive_dir: str = "archive"
    output_dir: str = "output"
    shift_mappings_file: str = "config/shift_mappings.json"
    staff_data_file: str = "config/staff_data.json"
    watcher_interval_seconds: int = 30
    log_level: str = "INFO"
    extra: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "AppConfig":
        with open(path) as f:
            data = json.load(f)
        known = {
            "imports_dir",
            "archive_dir",
            "output_dir",
            "shift_mappings_file",
            "staff_data_file",
            "watcher_interval_seconds",
            "log_level",
        }
        extra = {k: v for k, v in data.items() if k not in known}
        return cls(**(data | {"extra": extra}))
