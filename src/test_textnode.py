import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://site")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://site")
        self.assertNotEqual(node, node2)
        
    def test_not_eq_text(self):
        node = TextNode("This is a code node", TextType.CODE)
        node2 = TextNode("This is not a code node", TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_type(self):
        node = TextNode("This is a code node", TextType.CODE)
        node2 = TextNode("This is a code node", TextType.IMAGE)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://site")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://site")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()