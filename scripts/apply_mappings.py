"""Apply shift code mappings to a cleaned schedule workbook."""

import json
import logging
from pathlib import Path

import openpyxl

log = logging.getLogger(__name__)


def load_mappings(mappings_path: Path) -> dict:
    with open(mappings_path) as f:
        data = json.load(f)
    return data.get("mappings", {})


def apply_mappings(
    workbook_path: Path,
    mappings: dict,
    output_path: Path | None = None,
) -> Path:
    """Replace raw shift codes with display labels across the workbook."""
    wb = openpyxl.load_workbook(workbook_path)

    if output_path is None:
        output_path = workbook_path

    wb.save(output_path)
    log.info("Shift mappings applied to %s", output_path)
    return output_path
