from typing import List, Optional

from selectolax.parser import HTMLParser, Node


class MultipleElementsFoundError(AssertionError):
    def __init__(self, text, count):
        super().__init__(
            f"Found {count} elements with label text '{text}'. "
            "Use query_all_by_label_text if multiple matches are expected."
        )


def query_by_label_text(dom: HTMLParser, text: str) -> Optional[Node]:
    search_text = text.strip().lower()
    matches = []
    
    for label in dom.css('label'):
        label_text = label.text(deep=True, strip=True).lower()
        if search_text == label_text:
            target_id = label.attributes.get('for')
            if target_id:
                target = dom.css_first(f'#{target_id}')
                if target:
                    matches.append(target)
    
    if len(matches) > 1:
        raise MultipleElementsFoundError(text, len(matches))
    
    return matches[0] if matches else None
