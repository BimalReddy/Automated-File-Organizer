import logging
import time
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from sorter import sort_file


class FileOrganizerHandler(FileSystemEventHandler):
    """Custom event handler listening for file creation and rename events."""

    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def on_created(self, event):
        """Triggers when a new file is pasted or directly created in the folder."""
        if not event.is_directory:
            sort_file(Path(event.src_path), self.config)

    def on_moved(self, event):
        """
        Triggers when a file is renamed.
        Crucial for browser downloads which save as temp files and rename on completion.
        """
        if not event.is_directory:
            sort_file(Path(event.dest_path), self.config)


def start_watching(watch_directory: str, config: dict):
    """Initializes and runs the watchdog Observer."""
    event_handler = FileOrganizerHandler(config)
    observer = Observer()
    
    # Listen to target directory (non-recursive so subfolders aren't watched)
    observer.schedule(event_handler, path=watch_directory, recursive=False)
    observer.start()

    logging.info(f"Watching folder: {watch_directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Observer stopped.")

    observer.join()
