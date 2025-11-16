import json


def assert_json_str_equal(s1: str, s2: str):
    """Recursively compares two JSON strings for equality, ignoring order"""

    ss1_original = json.loads(s1)
    ss2_original = json.loads(s2)
    ss1 = []
    ss2 = []
    try:
        ss1 = sorted(ss1_original.items())
        ss2 = sorted(ss2_original.items())
    except AttributeError as ex:
        print(ex)
    for index, _ in enumerate(ss1):
        ss1_child_value = ss1[index]
        ss2_child_value = ss2[index]
        ss1_child_type = type(ss1_child_value)
        ss2_child_type = type(ss2_child_value)
        RECURSE_TYPES = [
            type(tuple),
            type(list),
            type(dict),
            type(str),
            tuple,
            list,
            dict,
            str,
        ]
        if ss1_child_type in RECURSE_TYPES:
            assert_json_str_equal(json.dumps(ss1), json.dumps(ss2))
        else:
            is_type_match = ss1_child_type == ss2_child_type
            if not is_type_match:
                print(f"types do not match ({ss1_child_type} != {ss2_child_type})")
            is_value_match = ss1_child_value == ss2_child_value
            if not is_value_match:
                print(f"values do not match ({ss1_child_value} != {ss2_child_value})")
            assert is_type_match, f"type mismatch: {ss1_child_type} != {ss2_child_type}"
            assert (
                is_value_match
            ), f"values don't match: {ss1_child_value} != {ss2_child_value}"
