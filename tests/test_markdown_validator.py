import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from markdown_validator import validate_markdown_links

class TestMarkdownValidator(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        for f in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, f))
        os.rmdir(self.test_dir)

    def test_valid_local_link(self):
        with open(os.path.join(self.test_dir, "valid_file.md"), "w") as f:
            f.write("This is a [valid link](test_file.txt).")
        with open(os.path.join(self.test_dir, "test_file.txt"), "w") as f:
            f.write("Hello")
        broken_links = validate_markdown_links(os.path.join(self.test_dir, "valid_file.md"))
        self.assertEqual(len(broken_links), 0)

    def test_broken_local_link(self):
        with open(os.path.join(self.test_dir, "broken_file.md"), "w") as f:
            f.write("This is a [broken link](non_existent_file.txt).")
        broken_links = validate_markdown_links(os.path.join(self.test_dir, "broken_file.md"))
        self.assertEqual(len(broken_links), 1)
        self.assertEqual(broken_links[0], "non_existent_file.txt")

    def test_external_link(self):
        with open(os.path.join(self.test_dir, "external_link.md"), "w") as f:
            f.write("This is an [external link](https://www.google.com).")
        broken_links = validate_markdown_links(os.path.join(self.test_dir, "external_link.md"))
        self.assertEqual(len(broken_links), 0)

    def test_link_with_anchor(self):
        with open(os.path.join(self.test_dir, "anchor_link.md"), "w") as f:
            f.write("This is an [anchor link](test_file.txt#section).")
        with open(os.path.join(self.test_dir, "test_file.txt"), "w") as f:
            f.write("Hello")
        broken_links = validate_markdown_links(os.path.join(self.test_dir, "anchor_link.md"))
        self.assertEqual(len(broken_links), 0)

    def test_image_link(self):
        with open(os.path.join(self.test_dir, "image_link.md"), "w") as f:
            f.write("This is an ![image](image.png).")
        with open(os.path.join(self.test_dir, "image.png"), "w") as f:
            f.write("dummy image content")
        broken_links = validate_markdown_links(os.path.join(self.test_dir, "image_link.md"))
        self.assertEqual(len(broken_links), 0)

    def test_broken_image_link(self):
        with open(os.path.join(self.test_dir, "broken_image_link.md"), "w") as f:
            f.write("This is a ![broken image](non_existent_image.png).")
        broken_links = validate_markdown_links(os.path.join(self.test_dir, "broken_image_link.md"))
        self.assertEqual(len(broken_links), 1)
        self.assertEqual(broken_links[0], "non_existent_image.png")

if __name__ == '__main__':
    unittest.main()

