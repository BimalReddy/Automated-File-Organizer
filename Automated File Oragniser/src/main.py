import argparse
import logging
from pathlib import Path

# Local imports
from config_parser import load_config
from watcher import start_watching

def setup_logging():
    """Configures the logging format for the console."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def main():
    # 1. Set up command-line arguments
    parser = argparse.ArgumentParser(description="Automated File Organizer")
    parser.add_argument(
        "-c", "--config",
        type=str,
        default="config.json",  # FIX: Removed '../' and updated to config.json
        help="Path to the configuration file (default: config.json)"
    )
    args = parser.parse_args()

    setup_logging()
    logging.info("Starting Automated File Organizer...")

    # 2. Load and validate the configuration file
    config_path = Path(args.config)
    if not config_path.is_file():
        logging.error(f"Configuration file not found: {config_path.resolve()}")
        logging.info("Did you forget to copy config.example.json to config.json?")
        return

    config = load_config(config_path)
    
    # We expect the config file to define which directory to watch
    watch_directory = config.get("watch_directory")

    # Safe validation: short-circuits before passing None to Path()
    if not watch_directory or not Path(watch_directory).is_dir():
        logging.error(f"Watch directory is invalid or does not exist: {watch_directory}")
        return

    # 3. Start the background watcher
    logging.info(f"Monitoring directory: {watch_directory}")
    try:
        start_watching(watch_directory, config)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Stopping File Organizer...")

if __name__ == "__main__":
    main()
