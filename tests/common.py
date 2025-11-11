import json


def assert_json_str_equal(s1: str, s2: str):
    """Recursively compares two JSON strings for equality, ignoring order"""
    ss1 = sorted(json.loads(s1).items())
    ss2 = sorted(json.loads(s2).items())
    for index, _ in enumerate(ss1):
        if type(ss1[index]) in [type(list), type(dict)]:
            assert_json_str_equal(json.dumps(ss1), json.dumps(ss2))
        else:
            assert ss1[index] == ss2[index], f"{ss1[index]} != {ss2[index]}"
