import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("test node", TextType.LINK, "www.testing.com")
        node2 = TextNode("test node", TextType.LINK, "www.testing.com")
        self.assertEqual(node, node2)

    def test_ineq(self):
        node = TextNode("test node", TextType.LINK, "www.testing.com")
        node2 = TextNode("test node", TextType.IMAGE, "www.testing.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is linked text", TextType.LINK, "www.test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is linked text")
        self.assertEqual(html_node.props, {"href": "www.test.com"})

    def test_italic(self):
        node = TextNode("This text is in italics", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This text is in italics")


if __name__ == "__main__":
    unittest.main()