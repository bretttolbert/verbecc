import json


def assert_json_str_equal(s1: str, s2: str):
    """Recursively compares two JSON strings for equality, ignoring order"""

    ss1_original = json.loads(s1)
    ss2_original = json.loads(s2)
    ss1_type = type(ss1_original)
    ss2_type = type(ss2_original)

    # check type first, we don't want to recurse if for example one is Dict and the other is List
    is_type_match = ss1_type == ss2_type
    assert is_type_match, f"types do not match ({ss1_type} != {ss2_type})"

    ss1 = []
    ss2 = []
    if hasattr(ss1_original, "items"):
        ss1 = sorted(ss1_original.items())
        ss2 = sorted(ss2_original.items())
    else:
        ss1 = ss1_original
        ss2 = ss2_original

    for index, _ in enumerate(ss1):
        ss1_child_value = ss1[index]
        ss2_child_value = ss2[index]
        ss1_child_type = type(ss1_child_value)
        ss2_child_type = type(ss2_child_value)
        RECURSE_TYPES = [
            type(tuple),
            type(list),
            type(dict),
            tuple,
            list,
            dict,
        ]

        # now check value or recurse
        if ss1_child_type in RECURSE_TYPES:
            assert_json_str_equal(
                json.dumps(ss1_child_value), json.dumps(ss2_child_value)
            )
        else:
            is_child_type_match = ss1_child_type == ss2_child_type
            is_child_value_match = ss1_child_value == ss2_child_value
            assert (
                is_child_type_match
            ), f"child types do not match ({ss1_child_type} != {ss2_child_type})"
            assert (
                is_child_value_match
            ), f"child values do not match ({ss1_child_value} != {ss2_child_value})"
