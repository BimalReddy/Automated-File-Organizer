import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add the src directory to the system path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from sorter import get_destination_folder, resolve_collision


class TestSorter(unittest.TestCase):
    def setUp(self):
        """Sets up mock configuration rules and a temporary directory."""
        self.rules = {
            "Images": [".jpg", ".png"],
            "PDFs": [".pdf"],
            "Documents": [".docx", ".txt"]
        }
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_dir_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_get_destination_folder_match(self):
        """Test that known extensions map to the correct folder."""
        file_path = Path("family_photo.jpg")
        folder = get_destination_folder(file_path, self.rules, "Others")
        self.assertEqual(folder, "Images")

    def test_get_destination_folder_case_insensitive(self):
        """Test that uppercase extensions are handled correctly."""
        file_path = Path("invoice.PDF")
        folder = get_destination_folder(file_path, self.rules, "Others")
        self.assertEqual(folder, "PDFs")

    def test_get_destination_folder_default(self):
        """Test that unknown extensions go to the default folder."""
        file_path = Path("unknown_file.xyz")
        folder = get_destination_folder(file_path, self.rules, "Others")
        self.assertEqual(folder, "Others")

    def test_resolve_collision_no_conflict(self):
        """Test that a file keeps its name if no duplicate exists."""
        target_path = self.test_dir_path / "report.pdf"
        resolved_path = resolve_collision(target_path)
        self.assertEqual(resolved_path.name, "report.pdf")

    def test_resolve_collision_with_conflict(self):
        """Test that a file is renamed if duplicates exist."""
        target_path = self.test_dir_path / "report.pdf"
        
        # Create a fake file to simulate a collision
        target_path.touch()
        
        resolved_path = resolve_collision(target_path)
        self.assertEqual(resolved_path.name, "report (1).pdf")

    def test_resolve_collision_multiple_conflicts(self):
        """Test that it increments the counter correctly for multiple duplicates."""
        target_path = self.test_dir_path / "data.csv"
        
        # Simulate multiple existing files
        target_path.touch()                                   # data.csv
        (self.test_dir_path / "data (1).csv").touch()         # data (1).csv
        
        resolved_path = resolve_collision(target_path)
        self.assertEqual(resolved_path.name, "data (2).csv")

if __name__ == "__main__":
    unittest.main()
