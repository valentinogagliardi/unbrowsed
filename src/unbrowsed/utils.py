"""unbrowsed utils."""

from selectolax.lexbor import LexborNode


def is_parent_of(parent: LexborNode, child: LexborNode) -> bool:
    """
    Determines if the given parent node is an ancestor of the given child node.
    """
    current = child.parent
    while current:
        if current == parent:
            return True
        current = current.parent
    return False
