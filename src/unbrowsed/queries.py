from typing import Optional, Any

from selectolax.lexbor import LexborHTMLParser, LexborNode

from unbrowsed.matchers import TextMatch


class MultipleElementsFoundError(AssertionError):
    def __init__(self, text, count, query_type="label text", is_get_method=False):
        method_prefix = "get_all_by" if is_get_method else "query_all_by"
        suggested_method = f"{method_prefix}_{query_type.replace(' ', '_')}"
        super().__init__(
            f"Found {count} elements with {query_type} '{text}'. "
            f"Use {suggested_method} if multiple matches are expected."
        )


class NoElementsFoundError(AssertionError):
    def __init__(self, text, query_type="label text"):
        query_all_method = f"query_all_by_{query_type.replace(' ', '_')}"
        super().__init__(
            f"No elements found with {query_type} '{text}'. "
            f"Use {query_all_method} if expecting no matches."
        )


class QueryResult:
    """Wrapper class for query result."""

    def __init__(self, element: LexborNode, context: str = ""):
        self.element = element
        self.context = context

    def to_have_attribute(self, name: str, value: Any = None) -> bool:
        """
        Check if the element has the specified attribute (and optionally matches value).
        """

        if name not in self.element.attributes:
            return False

        if value is None:
            return True

        actual_value = self.element.attributes.get(name)
        return actual_value == value


def query_by_label_text(
    dom: LexborHTMLParser, text: str, exact=True
) -> Optional[QueryResult]:
    """
    Queries the DOM for an element associated with a label containing the specified text.

    Args:
        dom: The parsed DOM to search within.
        text: The label text to search for.
        exact: Defaults to True; matches full strings, case-sensitive. When False,
               matches substrings and is not case-sensitive.

    Returns:
        A QueryResult containing the matched element and context description,
        or None if no matches were found.

    Raises:
        MultipleElementsFoundError: If multiple elements with matching label text are found.

    .. versionadded:: 0.1.0a9
       The *exact* parameter.
    """
    search_text = TextMatch(text, exact=exact)
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
        raise MultipleElementsFoundError(text, len(matches), "label text")

    if not matches:
        return None
    return QueryResult(matches[0], f"with label text '{text}'")


def get_by_label_text(dom: LexborHTMLParser, text: str, exact=True) -> QueryResult:
    """
    Retrieves an element from the DOM by its label text.

    Similar to query_by_label_text but throws an error if no element is found or if
    multiple elements are found with the matching label text.

    Args:
        dom: The parsed DOM to search within.
        text: The label text to search for.
        exact: Defaults to True; matches full strings, case-sensitive. When False,
               matches substrings and is not case-sensitive.

    Returns:
        A QueryResult containing the matched element and context description.

    Raises:
        NoElementsFoundError: If no elements with the specified label text are found.
        MultipleElementsFoundError: If multiple elements with matching label text are found.

    .. versionadded:: 0.1.0a9
       The *exact* parameter.
    """
    try:
        result = query_by_label_text(dom, text, exact)
        if not result:
            raise NoElementsFoundError(text)
        return result
    except MultipleElementsFoundError as e:
        raise MultipleElementsFoundError(
            text, e.args[0].split()[1], "label text", is_get_method=True
        )


def query_by_text(
    dom: LexborHTMLParser, text: str, exact=True
) -> Optional[QueryResult]:
    """
    Queries the DOM for an element containing the specified text.

    Args:
        dom: The parsed DOM to search within.
        text: The text content to search for.
        exact: Defaults to True; matches full strings, case-sensitive. When False,
               matches substrings and is not case-sensitive.

    Returns:
        A QueryResult containing the matched element and context description,
        or None if no matches were found.

    Raises:
        MultipleElementsFoundError: If multiple elements with matching text are found.

    .. versionadded:: 0.1.0a9
       The *exact* parameter.
    """
    search_text = TextMatch(text, exact=exact)
    matches = []

    for element in dom.css("*"):
        element_text = element.text(deep=True, strip=True)

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


def get_by_text(dom: LexborHTMLParser, text: str, exact=True) -> QueryResult:
    """
    Retrieves an element from the DOM by its text content.

    Similar to query_by_text but throws an error if no element is found or if
    multiple elements are found with the matching text content.

    Args:
        dom: The parsed DOM to search within.
        text: The text content to search for.
        exact: Defaults to True; matches full strings, case-sensitive. When False,
               matches substrings and is not case-sensitive.

    Returns:
        A QueryResult containing the matched element and context description.

    Raises:
        NoElementsFoundError: If no elements with the specified text are found.
        MultipleElementsFoundError: If multiple elements with matching text are found.

    .. versionadded:: 0.1.0a9
       The *exact* parameter.
    """
    try:
        result = query_by_text(dom, text, exact=exact)
        if not result:
            raise NoElementsFoundError(text, "text")
        return result
    except MultipleElementsFoundError as e:
        raise MultipleElementsFoundError(
            text, e.args[0].split()[1], "text", is_get_method=True
        )


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
