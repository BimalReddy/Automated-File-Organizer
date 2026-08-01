import json
import logging
from pathlib import Path


def load_config(config_path: Path) -> dict:
    """
    Loads and parses the JSON configuration file.
    
    Args:
        config_path (Path): The path to the configuration file.
        
    Returns:
        dict: The parsed configuration as a Python dictionary. Returns an empty 
              dictionary if the file cannot be read or parsed.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = json.load(file)
            logging.info(f"Successfully loaded configuration from {config_path.name}")
            return config
            
    except json.JSONDecodeError as e:
        logging.error(f"Syntax error in configuration file '{config_path.name}': {e}")
        logging.error("Please ensure it is valid JSON (e.g., check for missing commas or quotes).")
        return {}
        
    except PermissionError:
        logging.error(f"Permission denied when trying to read '{config_path.name}'.")
        return {}
        
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading config: {e}")
        return {}
