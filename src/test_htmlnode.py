import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr1(self):
        node = HTMLNode(tag="myTag", value="myValue")
        string = node.__repr__()
        expected_string = f"""
        -- HTML Node -- 
        Tag: myTag
        Value: myValue
        Children: None
        props: None
        """
        self.assertEqual(string, expected_string)
    
    def test_props_to_html1(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        expected_html = 'href="https://www.google.com" target="_blank"'
        
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), expected_html)
        
    def test_props_to_html2(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
            "rel": "stylesheet",
        }
        expected_html = 'href="https://www.google.com" target="_blank" rel="stylesheet"'
        
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), expected_html)
        
    