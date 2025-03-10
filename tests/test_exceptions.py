import pickle

from unbrowsed.exceptions import (
    NoElementsFoundError,
    MultipleElementsFoundError,
)


def test_no_elements_found_serialization():
    e = NoElementsFoundError(
        "No elements found with 'the text'. "
        "Use query_by_label_text if expecting no matches."
    )
    serialized = pickle.dumps(e)
    pickle.loads(serialized)


def test_multiple_elements_found_serialization():
    e = MultipleElementsFoundError(
        "Found 1 elements with 'the text'. "
        "Use query_by_label_text if multiple matches are expected."
    )
    serialized = pickle.dumps(e)
    pickle.loads(serialized)
