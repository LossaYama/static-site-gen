import unittest
from markdown_to_textnode import split_nodes_delimiter
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
                        [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                        ])

    def test_nontext_input(self):
        node = TextNode("This is bold text", TextType.BOLD)
        new_node = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_node, [TextNode("This is bold text", TextType.BOLD)])

    def test_edge_delimiter(self):
        node = TextNode("**Start bold** to keep them reading", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
                         [
                             TextNode("Start bold", TextType.BOLD),
                             TextNode(" to keep them reading", TextType.TEXT)
                         ])

    def test_unclosed_delimiter(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter("hello `code world", TextType.TEXT)


if __name__ == "__main__":
    unittest.main()