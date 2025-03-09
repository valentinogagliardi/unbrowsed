"""unbrowsed queries."""

from typing import Any, Optional, Union

from selectolax.lexbor import LexborHTMLParser as Parser
from selectolax.lexbor import LexborNode

from unbrowsed.exceptions import (
    MultipleElementsFoundError,
    NoElementsFoundError,
)
from unbrowsed.matchers import RoleMatcher, TextMatch
from unbrowsed.utils import is_parent_of


class QueryResult:
    """Wrapper class for query result."""

    def __init__(self, element: LexborNode):
        self.element = element

    def to_have_attribute(self, name: str, value: Any = None) -> bool:
        """
        Check if the element has the specified attribute
         (and optionally matches value).
        """

        if name not in self.element.attributes:
            return False

        if value is None:
            return True

        actual_value = self.element.attributes.get(name)
        return actual_value == value

    def to_have_text_content(self, text: str, exact: bool = True) -> bool:
        """
        Check if the element's text content matches the specified text.

        Args:
            text: The text content to check for.
            exact: Defaults to `True`; matches full strings, case-sensitive.
                   When `False`, matches substrings and is not case-sensitive.

        Returns:
            `True` if the element's text content matches the specified text,
            `False` otherwise.

        .. versionadded:: 0.1.0a11
        """
        element_text = self.element.text(strip=True)

        if exact:
            return element_text == text
        else:
            return text.lower() in element_text.lower()


def query_by_label_text(
    dom: Parser, text: str, exact=True
) -> Optional[QueryResult]:
    """
    Queries the DOM for an element associated with a label
    containing the specified text.

    Args:
        dom: The parsed DOM to search within.
        text: The label text to search for.
        exact: Defaults to `True`; matches full strings, case-sensitive.
               When `False`, matches substrings and is not case-sensitive.

    Returns:
        A QueryResult containing the matched element.

    Raises:
        MultipleElementsFoundError:
        If multiple elements with matching label text are found.

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
        raise MultipleElementsFoundError(
            text, len(matches), alt_method="get_all_by_label_text"
        )

    if not matches:
        return None
    return QueryResult(matches[0])


def get_by_label_text(dom: Parser, text: str, exact=True) -> QueryResult:
    """
    Retrieves an element from the DOM by its label text.

    Similar to query_by_label_text but throws an error if no element is found
    or if multiple elements are found with the matching label text.

    Args:
        dom: The parsed DOM to search within.
        text: The label text to search for.
        exact: Defaults to `True`; matches full strings, case-sensitive.
               When `False`, matches substrings and is not case-sensitive.

    Returns:
        A QueryResult containing the matched element.

    Raises:
        NoElementsFoundError:
            If no elements with the specified label text are found.
        MultipleElementsFoundError:
            If multiple elements with matching label text are found.

    .. versionadded:: 0.1.0a9
           The *exact* parameter.
    """
    try:
        result = query_by_label_text(dom, text, exact)
        if not result:
            raise NoElementsFoundError(text, alt_method="query_by_label_text")
        return result
    except MultipleElementsFoundError as e:
        raise MultipleElementsFoundError(
            text, e.args[0].split()[1], alt_method="get_all_by_label_text"
        )


def query_by_text(dom: Parser, text: str, exact=True) -> Optional[QueryResult]:
    """
    Queries the DOM for an element containing the specified text.

    Args:
        dom: The parsed DOM to search within.
        text: The text content to search for.
        exact: Defaults to `True`; matches full strings, case-sensitive.
               When `False`, matches substrings and is not case-sensitive.

    Returns:
        A QueryResult containing the matched element.

    Raises:
        MultipleElementsFoundError:
            If multiple elements with matching text are found.

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
        exclusions = ("html", "body")
        filtered_matches = [m for m in matches if m.tag not in exclusions]

        if filtered_matches:
            matches = filtered_matches

        if len(matches) > 1:
            for i, parent in enumerate(matches):
                for j, child in enumerate(matches):
                    if i != j and is_parent_of(parent, child):
                        return QueryResult(matches[i])

            raise MultipleElementsFoundError(
                text, len(matches), alt_method="query_all_by_text"
            )

    if not matches:
        return None
    return QueryResult(matches[0])


def get_by_text(dom: Parser, text: str, exact=True) -> QueryResult:
    """
    Retrieves an element from the DOM by its text content.

    Similar to query_by_text but throws an error if no element is found or if
    multiple elements are found with the matching text content.

    Args:
        dom: The parsed DOM to search within.
        text: The text content to search for.
        exact: Defaults to `True`; matches full strings, case-sensitive.
               When `False`, matches substrings and is not case-sensitive.

    Returns:
        A QueryResult containing the matched element.

    Raises:
        NoElementsFoundError:
            If no elements with the specified text are found.
        MultipleElementsFoundError:
            If multiple elements with matching text are found.

    .. versionadded:: 0.1.0a9
           The *exact* parameter.
    """
    try:
        result = query_by_text(dom, text, exact=exact)
        if not result:
            raise NoElementsFoundError(text, alt_method="query_by_text")
        return result
    except MultipleElementsFoundError as e:
        raise MultipleElementsFoundError(
            text, e.args[0].split()[1], alt_method="get_all_by_text"
        )


def query_by_role(
    dom: Parser, role: str, current: Optional[Union[bool, str]] = None
) -> Optional[QueryResult]:
    """
    Queries the DOM for an element with the specified ARIA role.

    Args:
        dom: The parsed DOM to search within.
        role: The ARIA role to search for.
        current: Optional value to check for aria-current attribute.
                 Can be a boolean or string "true".

    Returns:
        A QueryResult containing the matched element.

    Raises:
        MultipleElementsFoundError:
            If multiple elements with matching role are found.

    .. versionadded:: 0.1.0a10
    """
    role_matcher = RoleMatcher(role)
    matches = []

    for element in dom.css("*"):
        if not role_matcher.matches(element):
            continue

        if current is not None:

            expected = str(current).lower() == "true"
            actual = element.attributes.get("aria-current", "") == "true"
            if actual != expected:
                continue

        matches.append(element)

    if len(matches) > 1:
        exclusions = ("html", "body")
        filtered_matches = [m for m in matches if m.tag not in exclusions]

        if filtered_matches:
            matches = filtered_matches

        if len(matches) > 1:
            for i, parent in enumerate(matches):
                for j, child in enumerate(matches):
                    if i != j and is_parent_of(parent, child):
                        return QueryResult(child)

            raise MultipleElementsFoundError(
                role, len(matches), alt_method="query_all_by_role"
            )

    if not matches:
        return None

    return QueryResult(matches[0])


def get_by_role(
    dom: Parser, role: str, current: Optional[Union[bool, str]] = None
) -> QueryResult:
    """
    Retrieves an element from the DOM by its ARIA role.

    Similar to query_by_role but throws an error if no element is found or if
    multiple elements are found with the matching role.

    Args:
        dom: The parsed DOM to search within.
        role: The ARIA role to search for.
        current: Optional value to check for aria-current attribute.
                 Can be a boolean or string "true".

    Returns:
        A QueryResult containing the matched element and context description.

    Raises:
        NoElementsFoundError:
            If no elements with the specified role are found.
        MultipleElementsFoundError:
            If multiple elements with matching role are found.

    .. versionadded:: 0.1.0a10
    """
    try:
        result = query_by_role(dom, role, current=current)
        if not result:
            raise NoElementsFoundError(role, alt_method="query_by_role")
        return result
    except MultipleElementsFoundError as e:
        raise MultipleElementsFoundError(
            role, e.args[0].split()[1], alt_method="get_all_by_role"
        )


def query_all_by_role(
    dom: Parser, role: str, current: Optional[Union[bool, str]] = None
) -> list[QueryResult]:
    """
    Queries the DOM for all elements with the specified ARIA role.

    Args:
        dom: The parsed DOM to search within.
        role: The ARIA role to search for.
        current: Optional value to check for aria-current attribute.
                 Can be a boolean or string "true".

    Returns:
        A list of QueryResult objects containing the matched elements.

    .. versionadded:: 0.1.0a13
    """
    role_matcher = RoleMatcher(role)
    matches = []

    for element in dom.css("*"):
        if not role_matcher.matches(element):
            continue

        if current is not None:
            expected = str(current).lower() == "true"
            actual = element.attributes.get("aria-current", "") == "true"
            if actual != expected:
                continue

        matches.append(QueryResult(element))

    return matches


def get_all_by_role(
    dom: Parser, role: str, current: Optional[Union[bool, str]] = None
) -> list[QueryResult]:
    """
    Retrieves all elements from the DOM by their ARIA role.

    Similar to query_all_by_role but throws an error if no elements are found.

    Args:
        dom: The parsed DOM to search within.
        role: The ARIA role to search for.
        current: Optional value to check for aria-current attribute.
                 Can be a boolean or string "true".

    Returns:
        A list of QueryResult objects containing the matched elements.

    Raises:
        NoElementsFoundError:
            If no elements with the specified role are found.

    .. versionadded:: 0.1.0a13
    """
    results = query_all_by_role(dom, role, current=current)
    if not results:
        raise NoElementsFoundError(role, alt_method="query_all_by_role")
    return results
