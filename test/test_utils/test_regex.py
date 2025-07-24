import unittest
from utils.regex import extract_markdown_images, extract_markdown_links, is_block_heading, is_block_code, get_heading

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

class TestIsBlockHeading(unittest.TestCase):
    def test_is_heading1(self):
        block = "# Heading 1"
        result = is_block_heading(block)
        self.assertEqual(result, True)

    def test_is_heading2(self):
        block = "## Heading 2"
        result = is_block_heading(block)
        self.assertEqual(result, True)

    def test_is_heading3(self):
        block = "### Heading 3"
        result = is_block_heading(block)
        self.assertEqual(result, True)

    def test_is_heading4(self):
        block = "#### Heading 4"
        result = is_block_heading(block)
        self.assertEqual(result, True)

    def test_is_heading5(self):
        block = "##### Heading 5"
        result = is_block_heading(block)
        self.assertEqual(result, True)

    def test_is_heading6(self):
        block = "###### Heading 6"
        result = is_block_heading(block)
        self.assertEqual(result, True)
    
    def test_invalid_heading_spacing(self):
        block = "#Heading 1"
        result = is_block_heading(block)
        self.assertEqual(result, False)

    def test_invalid_heading7(self):
        block = "####### Heading 7"
        result = is_block_heading(block)
        self.assertEqual(result, False)

class TestIsBlockCode(unittest.TestCase):
    def test_is_block_code(self):
        block = "```my code = 'test code'```"
        result = is_block_code(block)
        self.assertEqual(result, True)

    def test_is_block_code_with_newlines(self):
        block = "```my code = 'test code'\nmy_var2 = 123```"
        result = is_block_code(block)
        self.assertEqual(result, True)

    def test_is_block_code_invalid(self):
        block = "```my code = 'test code'\nmy_var2 = 123``"
        result = is_block_code(block)
        self.assertEqual(result, False)

class TestHeadingNumber(unittest.TestCase):
    def test_heading_1(self):
        block = "# Heading 1"
        heading_num = get_heading(block)
        self.assertEqual(heading_num, "# ")

    def test_heading_3(self):
        block = "### Heading 3"
        heading_num = get_heading(block)
        self.assertEqual(heading_num, "### ")

    def test_heading_6(self):
        block = "###### Heading 6"
        heading_num = get_heading(block)
        self.assertEqual(heading_num, "###### ")

    def test_heading_6_invalid(self):
        block = "######Heading 6"
        heading_num = get_heading(block)
        self.assertEqual(heading_num, None)

    def test_heading_7_invalid(self):
        block = "####### Heading 7"
        heading_num = get_heading(block)
        self.assertEqual(heading_num, None)