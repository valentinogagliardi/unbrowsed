import pickle

from unbrowsed.exceptions import (
    NoElementsFoundError,
    MultipleElementsFoundError,
)


def test_no_elements_found_serialization():
    e = NoElementsFoundError(text="the text", alt_method="query_by_label_text")
    serialized = pickle.dumps(e)
    pickle.loads(serialized)


def test_multiple_elements_found_serialization():
    e = MultipleElementsFoundError(
        text="the text", alt_method="query_by_label_text", count=1
    )
    serialized = pickle.dumps(e)
    pickle.loads(serialized)
