import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add the src directory to the system path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from config_parser import load_config


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        """Runs before every test to set up a temporary directory."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_dir_path = Path(self.test_dir.name)

    def tearDown(self):
        """Runs after every test to clean up."""
        self.test_dir.cleanup()

    def test_load_valid_config(self):
        """Test that a well-formatted JSON file loads correctly."""
        config_path = self.test_dir_path / "valid_config.json"
        valid_data = {"watch_directory": "/tmp", "rules": {"Images": [".jpg"]}}
        
        with open(config_path, "w") as f:
            json.dump(valid_data, f)

        loaded_config = load_config(config_path)
        self.assertEqual(loaded_config["watch_directory"], "/tmp")
        self.assertIn("Images", loaded_config["rules"])

    def test_load_invalid_config(self):
        """Test that a broken JSON file returns an empty dictionary."""
        config_path = self.test_dir_path / "invalid_config.json"
        
        with open(config_path, "w") as f:
            f.write("{ invalid json formatting")

        loaded_config = load_config(config_path)
        self.assertEqual(loaded_config, {})

    def test_missing_config_file(self):
        """Test that a non-existent file returns an empty dictionary."""
        config_path = self.test_dir_path / "does_not_exist.json"
        
        loaded_config = load_config(config_path)
        self.assertEqual(loaded_config, {})

if __name__ == "__main__":
    unittest.main()
