import tempfile
import unittest
from pathlib import Path

from folder_browser import numbered_folders, review_folders


class FolderSelectionTests(unittest.TestCase):
    def test_empty_folder_set_has_no_reviews(self):
        self.assertEqual(review_folders({}), [])

    def test_selects_newest_and_available_review_intervals(self):
        folders = {number: f"/{number}" for number in (1, 2, 4, 7)}
        selected = review_folders(folders)
        self.assertEqual([number for number, _ in selected], [7, 4, 2])

    def test_finds_only_folders_with_leading_numbers(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("1 first", "20 review", "Lesson 30"):
                (root / name).mkdir()

            found = numbered_folders(root)

        self.assertEqual(sorted(found), [1, 20])

    def test_duplicate_numbers_are_deterministic(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "1 Alpha").mkdir()
            (root / "1 Beta").mkdir()

            found = numbered_folders(root)

        self.assertEqual(Path(found[1]).name, "1 Alpha")


if __name__ == "__main__":
    unittest.main()
