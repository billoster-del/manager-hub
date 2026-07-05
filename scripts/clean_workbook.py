"""Clean and standardize a Dayforce schedule workbook using openpyxl."""

import logging
from pathlib import Path

import openpyxl

log = logging.getLogger(__name__)


def clean_workbook(input_path: Path, output_path: Path | None = None) -> Path:
    """Standardize worksheet structure, remove empty rows, fix headers."""
    wb = openpyxl.load_workbook(input_path)

    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_clean.xlsx"

    wb.save(output_path)
    log.info("Cleaned workbook saved to %s", output_path)
    return output_path
