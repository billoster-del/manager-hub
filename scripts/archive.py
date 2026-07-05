"""Archive processed schedule exports."""

import logging
import shutil
from pathlib import Path

log = logging.getLogger(__name__)


def archive_file(source: Path, archive_dir: Path) -> Path:
    """Move a processed file into the archive directory with a timestamp."""
    archive_dir.mkdir(parents=True, exist_ok=True)

    timestamp = archive_dir.joinpath(source.name)
    dest = shutil.move(str(source), str(timestamp))

    log.info("Archived %s -> %s", source.name, dest)
    return Path(dest)
