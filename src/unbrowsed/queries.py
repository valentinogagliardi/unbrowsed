from typing import Optional, Any

from selectolax.parser import Node
from selectolax.lexbor import LexborHTMLParser


class MultipleElementsFoundError(AssertionError):
    def __init__(self, text, count, query_type="label text"):
        query_all_method = f"query_all_by_{query_type.replace(' ', '_')}"
        super().__init__(
            f"Found {count} elements with {query_type} '{text}'. "
            f"Use {query_all_method} if multiple matches are expected."
        )


class NoElementsFoundError(AssertionError):
    def __init__(self, text, query_type="label text"):
        query_all_method = f"query_all_by_{query_type.replace(' ', '_')}"
        super().__init__(
            f"No elements found with {query_type} '{text}'. "
            f"Use {query_all_method} if expecting no matches."
        )


class QueryResult:
    def __init__(self, element: Optional[Node], context: str = ""):
        self.element = element
        self.context = context

    def __bool__(self) -> bool:
        return self.element is not None

    def __eq__(self, other) -> bool:
        if other is None:
            return self.element is None
        return super().__eq__(other)

    def to_have_attribute(self, name: str, value: Any = None) -> bool:
        """
        Check if the element has the specified attribute (and optionally matches value).
        """
        if not self.element:
            return False

        if name not in self.element.attributes:
            return False

        if value is None:
            return True

        actual_value = self.element.attributes.get(name)
        return actual_value == value


def query_by_label_text(dom: LexborHTMLParser, text: str) -> Optional[QueryResult]:
    """
    Queries the DOM for an element associated with a label containing the specified text.
    """
    search_text = text.strip()
    matches = []

    for label in dom.css("label"):
        label_text = label.text(deep=True, strip=True)
        if search_text == label_text:
            if target_id := label.attributes.get("for"):
                if target := dom.css_first(f"#{target_id}"):
                    matches.append(target)
            else:
                if control := label.css_first("input, select, textarea"):
                    matches.append(control)

    if len(matches) > 1:
        raise MultipleElementsFoundError(text, len(matches))

    if not matches:
        return None
    return QueryResult(matches[0], f"with label text '{text}'")


def get_by_label_text(dom: LexborHTMLParser, text: str) -> QueryResult:
    """
    Retrieves an element from the DOM by its label text.
    """
    result = query_by_label_text(dom, text)
    if not result:
        raise NoElementsFoundError(text)
    return result


def query_by_text(dom: LexborHTMLParser, text: str) -> Optional[QueryResult]:
    """
    Queries the DOM for an element with the exact specified text.
    """
    search_text = " ".join(text.strip().lower().split())
    matches = []

    for element in dom.css("*"):
        element_text = element.text(deep=True, strip=True).lower()
        element_text = " ".join(element_text.split())

        if element_text == search_text:
            matches.append(element)

    if len(matches) > 1:
        filtered_matches = [m for m in matches if m.tag not in ("html", "body")]

        if filtered_matches:
            matches = filtered_matches

        if len(matches) > 1:
            for i, parent in enumerate(matches):
                for j, child in enumerate(matches):
                    if i != j and is_parent_of(parent, child):
                        return child

            raise MultipleElementsFoundError(text, len(matches), "text")

    if not matches:
        return None
    return QueryResult(matches[0], f"with text '{text}'")


def is_parent_of(parent: Node, child: Node) -> bool:
    """
    Determines if the given parent node is an ancestor of the given child node.
    """
    current = child.parent
    while current:
        if current == parent:
            return True
        current = current.parent
    return False
