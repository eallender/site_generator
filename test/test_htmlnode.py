import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr1(self):
        node = HTMLNode(tag="myTag", value="myValue")
        string = node.__repr__()
        expected_string = """
        -- HTML Node -- 
        Tag: myTag
        Value: myValue
        Children: None
        props: 
        """
        self.assertEqual(string, expected_string)

    def test_props_to_html1(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        expected_html = ' href="https://www.google.com" target="_blank"'

        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), expected_html)

    def test_props_to_html2(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
            "rel": "stylesheet",
        }
        expected_html = (
            ' href="https://www.google.com" target="_blank" rel="stylesheet"'
        )

        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), expected_html)

    def test_p(self):
        leaf = LeafNode("p", "Paragraph")
        self.assertEqual(leaf.to_html(), "<p>Paragraph</p>")

    def test_a(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            leaf.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_no_tag(self):
        leaf = leaf = LeafNode(None, "My text")
        self.assertEqual(leaf.to_html(), "My text")

    def test_leaf_no_value(self):
        leaf = LeafNode("p", None)
        result = leaf.to_html()
        self.assertIsInstance(result, ValueError)
        self.assertEqual(str(result), "LeafNode with no value")

    def test_parent_no_tag(self):
        child_node = LeafNode("span", "child")
        parent = ParentNode(None, [child_node])
        result = parent.to_html()
        self.assertIsInstance(result, ValueError)
        self.assertEqual(str(result), "ParentNode with no tag")

    def test_parent_no_child(self):
        parent = ParentNode("p", [])
        result = parent.to_html()
        self.assertIsInstance(result, ValueError)
        self.assertEqual(str(result), "ParentNode missing children")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("p", "child")
        child_node3 = LeafNode("h1", "child")
        child_node4 = LeafNode("h3", "child")
        parent_node = ParentNode(
            "div", [child_node1, child_node2, child_node3, child_node4]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span><p>child</p><h1>child</h1><h3>child</h3></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild")
        child_node1 = ParentNode("span", [grandchild_node1])

        grandchild_node2 = LeafNode("b", "grandchild")
        child_node2 = ParentNode("span", [grandchild_node2])

        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_and_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild")
        child_node1 = ParentNode("span", [grandchild_node1])

        child_node2 = LeafNode("h1", "child")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><h1>child</h1></div>",
        )

    def test_to_html_with_child_no_value(self):
        child_node = LeafNode("p", None)
        parent_node = ParentNode("div", [child_node])
        result = parent_node.to_html()
        self.assertIsInstance(result, ValueError)
        self.assertEqual(str(result), "LeafNode with no value")

    def test_to_html_with_child_no_tag(self):
        child_node = LeafNode(None, "My text")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), 
            "<div>My text</div>"
        )

