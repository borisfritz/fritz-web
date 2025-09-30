import unittest

from src.block_markdown import markdown_to_html_node

class TestMDtoHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",)
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
    and this as well!
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n    and this as well!</code></pre></div>",)


    def test_full_md(self):
        md = """
# Main Heading

This is a paragraph with some **bold text**, some _italic text_, and some `inline code`.

## Subheading

Another paragraph here. You can combine **bold**, _italic_, and `inline code` together.

### Code Block Example

```
def greet(name):
    print(f"Hello, {name}!")
greet("World")
```

#### Blockquote Example

> This is a quote block.
> You can put multiple lines in it.
> Even bold and italic can appear here if supported by your parser.

##### Ordered List

1. First item
2. Second item with inline code
3. Third item with bold text and italic text

###### Unordered List

- Item A
- Item B with inline code
- Item C with bold and italic
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            '<div>' +
            '<h1>Main Heading</h1>' +
            '<p>This is a paragraph with some <b>bold text</b>, some <i>italic text</i>, and some <code>inline code</code>.</p>' +
            '<h2>Subheading</h2><p>Another paragraph here. You can combine <b>bold</b>, <i>italic</i>, and <code>inline code</code> together.</p>' +
            '<h3>Code Block Example</h3>' +
            '<pre><code>def greet(name):\n    print(f"Hello, {name}!")\ngreet("World")</code></pre>' +
            '<h4>Blockquote Example</h4>' +
            '<blockquote>This is a quote block. You can put multiple lines in it. Even bold and italic can appear here if supported by your parser.</blockquote>' +
            '<h5>Ordered List</h5>' +
            '<ol>' +
            '<li>First item</li>' +
            '<li>Second item with inline code</li>' +
            '<li>Third item with bold text and italic text</li>' +
            '</ol>' +
            '<h6>Unordered List</h6>' +
            '<ul>' +
            '<li>Item A</li>' +
            '<li>Item B with inline code</li>' +
            '<li>Item C with bold and italic</li></ul></div>'
        )
