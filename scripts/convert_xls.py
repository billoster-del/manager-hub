"""Convert Dayforce .xls files to .xlsx using LibreOffice."""

import logging
import subprocess
from pathlib import Path

log = logging.getLogger(__name__)


def convert_xls_to_xlsx(input_path: Path, output_dir: Path) -> Path:
    """Convert a .xls file to .xlsx via LibreOffice headless mode."""
    output_dir.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "xlsx:Calc MS Excel 2007 XML",
            "--outdir",
            str(output_dir),
            str(input_path),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.error("LibreOffice conversion failed: %s", result.stderr)
        raise RuntimeError(f"Conversion failed for {input_path.name}")

    output_file = output_dir / f"{input_path.stem}.xlsx"
    log.info("Converted %s -> %s", input_path.name, output_file.name)
    return output_file
