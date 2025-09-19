from .textnode import TextType, TextNode

def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:

    valid_delimiters = [
        "**",
        "_",
        "`",
    ]
    
    if delimiter not in valid_delimiters:
        raise ValueError("Invalid delimiter.")
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
        else:
            parts = node.text.split(delimiter)
            odd_check = len(parts) % 2
            if odd_check == 0:
                raise Exception("Invalid markdown syntax, unclosed delimiter")
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part != "":
                        results.append(TextNode(part, TextType.TEXT))
                else:
                    results.append(TextNode(part, text_type))
    return results
