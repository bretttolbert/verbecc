from typing import Dict, List, Any


class DictUtils:
    DEFAULT_ESCAPE_STR = "_"

    @staticmethod
    def marshall_keys_recursive(
        data: Dict[str, Any],
        values_to_marshall: List[str],
        escape_str: str = DEFAULT_ESCAPE_STR,
    ) -> Dict[str, Any]:
        """
        Recursively appends escape_str to all keys matching values_to_marshall
        """
        if isinstance(data, dict):
            new_data = {}
            for k, v in data.items():
                if k in values_to_marshall:
                    new_k = k + escape_str
                    new_data[new_k] = DictUtils.marshall_keys_recursive(
                        v, values_to_marshall
                    )
                else:
                    new_data[k] = DictUtils.marshall_keys_recursive(
                        v, values_to_marshall
                    )
            return new_data
        elif isinstance(data, list):
            return [
                DictUtils.marshall_keys_recursive(v, values_to_marshall) for v in data
            ]
        else:
            return data

    @staticmethod
    def unmarshall_keys_recursive(
        data: Dict[str, Any], escape_str: str = DEFAULT_ESCAPE_STR
    ) -> Dict[str, Any]:
        """
        Recursively strips trailing escape_str, if present, from all keys
        """
        if isinstance(data, dict):
            new_data = {}
            for k, v in data.items():
                if k.endswith(escape_str):
                    new_k = k[:-1]
                    new_data[new_k] = DictUtils.unmarshall_keys_recursive(v)
                else:
                    new_data[k] = DictUtils.unmarshall_keys_recursive(v)
            return new_data
        elif isinstance(data, list):
            return [DictUtils.unmarshall_keys_recursive(v) for v in data]
        else:
            return data
