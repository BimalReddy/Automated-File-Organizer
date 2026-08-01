import logging
import shutil
import time
from pathlib import Path

# Common temporary download extensions to ignore until completed
TEMP_EXTENSIONS = {".crdownload", ".part", ".tmp", ".download"}


def get_destination_folder(file_path: Path, rules: dict, default_folder: str = "Others") -> str:
    """Determines the target folder name based on the file extension."""
    extension = file_path.suffix.lower()

    for category, extensions in rules.items():
        if extension in [ext.lower() for ext in extensions]:
            return category

    return default_folder


def resolve_collision(target_path: Path) -> Path:
    """Prevents overwriting existing files by appending a counter: e.g., file (1).pdf."""
    if not target_path.exists():
        return target_path

    stem = target_path.stem
    suffix = target_path.suffix
    parent = target_path.parent
    counter = 1

    while True:
        new_path = parent / f"{stem} ({counter}){suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def wait_for_file_ready(file_path: Path, timeout: int = 60) -> bool:
    """
    Waits for a file to finish writing by checking if its file size is stable.
    Prevents crashing when large files are still actively copying.
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # Check file size, wait a bit, then check again
            size_past = file_path.stat().st_size
            time.sleep(1)
            size_present = file_path.stat().st_size
            
            # If the size hasn't changed, the OS has likely finished writing it
            if size_past == size_present:
                return True
        except FileNotFoundError:
            # File might have been deleted quickly before we could process it
            return False
        except Exception as e:
            logging.debug(f"Waiting for file readiness: {e}")
            
    logging.warning(f"Timeout waiting for {file_path.name} to finish writing.")
    return False


def sort_file(file_path: Path, config: dict):
    """Sorts a single file into its designated subfolder according to config rules."""
    file_path = Path(file_path)

    # 1. Skip non-files, hidden files, or temporary browser downloads
    if not file_path.exists() or not file_path.is_file() or file_path.name.startswith("."):
        return

    if file_path.suffix.lower() in TEMP_EXTENSIONS:
        return

    rules = config.get("rules", {})
    watch_dir = Path(config["watch_directory"])
    default_folder = config.get("default_folder", "Others")

    # 2. Determine target directory
    dest_folder_name = get_destination_folder(file_path, rules, default_folder)
    dest_dir = watch_dir / dest_folder_name

    # Don't move a file if it's already in its target folder
    if file_path.parent.resolve() == dest_dir.resolve():
        return

    # 3. Create destination subfolder if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)

    # 4. Resolve filename collisions
    target_path = resolve_collision(dest_dir / file_path.name)

    # 5. Wait for OS to finish writing large files
    if not wait_for_file_ready(file_path):
        return

    # 6. Execute move with a fallback retry
    try:
        shutil.move(str(file_path), str(target_path))
        logging.info(f"Sorted: '{file_path.name}' -> '{dest_folder_name}/{target_path.name}'")
    except PermissionError:
        logging.error(f"Permission denied: {file_path.name} is locked by another process.")
    except Exception as e:
        logging.error(f"Failed to move '{file_path.name}': {e}")
