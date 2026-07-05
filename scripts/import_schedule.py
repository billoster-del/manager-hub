"""Watch the imports directory for new Dayforce .xls exports."""

import argparse
import json
import logging
import time
from pathlib import Path

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def load_config(config_path: Path) -> dict:
    with open(config_path) as f:
        return json.load(f)


class ScheduleHandler(PatternMatchingEventHandler):
    patterns = ["*.xls", "*.xlsx", "*.csv"]

    def on_created(self, event):
        log.info("New file detected: %s", event.src_path)


def main():
    parser = argparse.ArgumentParser(description="Manager Hub — Folder Watcher")
    parser.add_argument(
        "--config",
        default="config/app_config.json",
        type=Path,
    )
    args = parser.parse_args()

    config = load_config(args.config)
    watch_dir = Path(config.get("imports_dir", "imports")).resolve()
    watch_dir.mkdir(parents=True, exist_ok=True)

    log.info("Watching %s for new schedule exports...", watch_dir)

    handler = ScheduleHandler()
    observer = Observer()
    observer.schedule(handler, str(watch_dir), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
