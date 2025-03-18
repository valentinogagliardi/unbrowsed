"""unbrowsed utils."""

from selectolax.lexbor import LexborNode
from unbrowsed.types import AriaRoles


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


def get_selector(role: AriaRoles | None = None):
    """Return the appropriate CSS selector for the traversal root."""
    if role == "document":
        return "*"
    return "*:not(html):not(body)"
