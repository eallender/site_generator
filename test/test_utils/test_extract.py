import unittest
from utils.extract import extract_markdown_images, extract_markdown_links

class TestExtract(unittest.TestCase):
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)\n This is also text with an ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),("image2", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_invalid_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image]https://i.imgur.com/zjjcJKZ.png)")
        self.assertEqual(len(matches), 0)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_invalid_markdown_links(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev(https://www.boot.dev)")
        self.assertEqual(len(matches), 0)