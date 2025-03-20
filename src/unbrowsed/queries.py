"""unbrowsed queries."""

from typing import Any, Optional

from selectolax.lexbor import LexborHTMLParser as Parser
from selectolax.lexbor import LexborNode

from unbrowsed.exceptions import (
    MultipleElementsFoundError,
    NoElementsFoundError,
)
from unbrowsed.matchers import TextMatch
from unbrowsed.utils import is_parent_of
from unbrowsed.types import AriaRoles
from unbrowsed.resolvers import RoleResolver
from unbrowsed.utils import get_selector


class Result:
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
) -> Optional[Result]:
    """
    Queries the DOM for an element associated with a label
    containing the specified text.

    Args:
        dom: The parsed DOM to search within.
        text: The label text to search for.
        exact: Defaults to `True`; matches full strings, case-sensitive.
               When `False`, matches substrings and is not case-sensitive.

    Returns:
        A Result containing the matched element.

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
        if search_text.matches(label_text):
            if target_id := label.attributes.get("for"):
                if target := dom.css_first(f"#{target_id}"):
                    matches.append(target)
            else:
                if control := label.css_first("input, select, textarea"):
                    matches.append(control)

    if len(matches) > 1:
        raise MultipleElementsFoundError(
            f"Found {len(matches)} elements with label '{text}'. "
            f"Use get_all_by_label_text if multiple matches are expected."
        )

    if not matches:
        return None
    return Result(matches[0])


def get_by_label_text(dom: Parser, text: str, exact=True) -> Result:
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
        A Result containing the matched element.

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
            raise NoElementsFoundError(
                f"No elements found with label '{text}'. "
                f"Use query_by_label_text if expecting no matches."
            )
        return result
    except MultipleElementsFoundError as e:
        count = e.message.split()[1]
        raise MultipleElementsFoundError(
            f"Found {count} elements with label '{text}'. "
            f"Use get_all_by_label_text if multiple matches are expected."
        )


def query_by_text(dom: Parser, text: str, exact=True) -> Optional[Result]:
    """
    Queries the DOM for an element containing the specified text.

    Args:
        dom: The parsed DOM to search within.
        text: The text content to search for.
        exact: Defaults to `True`; matches full strings, case-sensitive.
               When `False`, matches substrings and is not case-sensitive.

    Returns:
        A Result containing the matched element.

    Raises:
        MultipleElementsFoundError:
            If multiple elements with matching text are found.

    .. versionadded:: 0.1.0a9
           The *exact* parameter.
    """
    search_text = TextMatch(text, exact=exact)
    matches = []

    for element in dom.css(get_selector()):
        element_text = element.text(deep=True, strip=True)

        if search_text.matches(element_text):
            matches.append(element)

    if len(matches) > 1:
        for i, parent in enumerate(matches):
            for j, child in enumerate(matches):
                if i != j and is_parent_of(parent, child):
                    return Result(matches[i])

        raise MultipleElementsFoundError(
            f"Found {len(matches)} elements with text '{text}'. "
            f"Use query_all_by_text if multiple matches are expected."
        )

    if not matches:
        return None
    return Result(matches[0])


def get_by_text(dom: Parser, text: str, exact=True) -> Result:
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
        A Result containing the matched element.

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
            raise NoElementsFoundError(
                f"No elements found with '{text}'. "
                f"Use query_by_text if expecting no matches."
            )
        return result
    except MultipleElementsFoundError as e:
        count = e.message.split()[1]
        raise MultipleElementsFoundError(
            f"Found {count} elements with text '{text}'. "
            f"Use get_all_by_text if multiple matches are expected."
        )


def query_by_role(
    dom: Parser,
    role: AriaRoles,
    current: Optional[bool | str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Optional[Result]:
    """
    Queries the DOM for an element with the specified ARIA role.

    Args:
        dom: The parsed DOM to search within.
        role: The ARIA role to search for.
        current: The value to check for aria-current attribute.
                 Can be a boolean or string "true".
        name: The accessible name of the element.
        description: The accessible description of the element.

    Returns:
        A Result containing the matched element.

    Raises:
        MultipleElementsFoundError:
            If multiple elements with matching role are found.

    .. versionadded:: 0.1.0a10
    .. versionadded:: 0.1.0a15
           The *name* parameter.
    .. versionadded:: 0.1.0a16
           The *description* parameter.
    """

    matches = []

    for element in dom.css(get_selector(role)):
        role_matcher = RoleResolver(
            element=element,
            target_role=role,
            name=name,
            description=description,
        )
        if not role_matcher.matches():
            continue

        if current is not None:
            expected = str(current).lower() == "true"
            actual = element.attributes.get("aria-current", "") == "true"
            if actual != expected:
                continue

        matches.append(element)

        if len(matches) > 1:
            for i, parent in enumerate(matches):
                for j, child in enumerate(matches):
                    if i != j and is_parent_of(parent, child):
                        return Result(child)

            raise MultipleElementsFoundError(
                f"Found {len(matches)} elements with role '{role}'. "
                f"Use query_all_by_role if multiple matches are expected."
            )

    if not matches:
        return None

    return Result(matches[0])


def get_by_role(
    dom: Parser,
    role: AriaRoles,
    current: Optional[bool | str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Result:
    """
    Retrieves an element from the DOM by its ARIA role.

    Similar to query_by_role but throws an error if no element is found or if
    multiple elements are found with the matching role.

    Args:
        dom: The parsed DOM to search within.
        role: The ARIA role to search for.
        current: The value to check for aria-current attribute.
                 Can be a boolean or string "true".
        name: The accessible name of the element.
        description: The accessible description of the element.

    Returns:
        A Result containing the matched element and context description.

    Raises:
        NoElementsFoundError:
            If no elements with the specified role are found.
        MultipleElementsFoundError:
            If multiple elements with matching role are found.

    .. versionadded:: 0.1.0a10
    .. versionadded:: 0.1.0a15
           The *name* parameter.
    .. versionadded:: 0.1.0a16
           The *description* parameter.
    """
    try:
        result = query_by_role(
            dom, role, current=current, name=name, description=description
        )
        if not result:
            raise NoElementsFoundError(
                f"No elements found with '{role}'. "
                f"Use query_by_role if expecting no matches."
            )
        return result
    except MultipleElementsFoundError as e:
        count = e.message.split()[1]
        raise MultipleElementsFoundError(
            f"Found {count} elements with role '{role}'. "
            f"Use get_all_by_role if multiple matches are expected."
        )


def query_all_by_role(
    dom: Parser, role: AriaRoles, current: Optional[bool | str] = None
) -> list[Result]:
    """
    Queries the DOM for all elements with the specified ARIA role.

    Args:
        dom: The parsed DOM to search within.
        role: The ARIA role to search for.
        current: The value to check for aria-current attribute.
                 Can be a boolean or string "true".

    Returns:
        A list of Result objects containing the matched elements.

    .. versionadded:: 0.1.0a13
    """

    matches = []

    for element in dom.css("*"):
        role_matcher = RoleResolver(element=element, target_role=role)
        if not role_matcher.matches():
            continue

        if current is not None:
            expected = str(current).lower() == "true"
            actual = element.attributes.get("aria-current", "") == "true"
            if actual != expected:
                continue

        matches.append(Result(element))

    return matches


def get_all_by_role(
    dom: Parser, role: AriaRoles, current: Optional[bool | str] = None
) -> list[Result]:
    """
    Retrieves all elements from the DOM by their ARIA role.

    Similar to query_all_by_role but throws an error if no elements are found.

    Args:
        dom: The parsed DOM to search within.
        role: The ARIA role to search for.
        current: Optional value to check for aria-current attribute.
                 Can be a boolean or string "true".

    Returns:
        A list of Result objects containing the matched elements.

    Raises:
        NoElementsFoundError:
            If no elements with the specified role are found.

    .. versionadded:: 0.1.0a13
    """
    results = query_all_by_role(dom, role, current=current)
    if not results:
        raise NoElementsFoundError(
            f"No elements found with role '{role}'. "
            f"Use query_all_by_role if expecting no matches."
        )
    return results
