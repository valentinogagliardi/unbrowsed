from typing import Optional

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


def query_by_label_text(dom: LexborHTMLParser, text: str) -> Optional[Node]:
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

    return matches[0] if matches else None


def get_by_label_text(dom: LexborHTMLParser, text: str) -> Node:
    result = query_by_label_text(dom, text)
    if not result:
        raise NoElementsFoundError(text)
    return result


def query_by_text(dom: LexborHTMLParser, text: str) -> Optional[Node]:
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

    return matches[0] if matches else None


def is_parent_of(parent: Node, child: Node) -> bool:
    current = child.parent
    while current:
        if current == parent:
            return True
        current = current.parent
    return False
