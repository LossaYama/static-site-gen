import unittest
from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()