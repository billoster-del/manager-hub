"""Export a processed schedule workbook to PDF via LibreOffice."""

import logging
import subprocess
from pathlib import Path

log = logging.getLogger(__name__)


def export_to_pdf(input_path: Path, output_dir: Path) -> Path:
    """Convert an .xlsx workbook to PDF via LibreOffice."""
    output_dir.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir),
            str(input_path),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.error("PDF export failed: %s", result.stderr)
        raise RuntimeError(f"PDF export failed for {input_path.name}")

    output_file = output_dir / f"{input_path.stem}.pdf"
    log.info("PDF exported: %s", output_file.name)
    return output_file
