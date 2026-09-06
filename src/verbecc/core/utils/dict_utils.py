from typing import Any, Type, cast


class DictUtils:
    DEFAULT_ESCAPE_STR = "_"

    @staticmethod
    def marshall_keys_recursive(
        data: Any,
        values_to_marshall: list[str],
        escape_str: str = DEFAULT_ESCAPE_STR,
    ) -> dict[str, Any] | list[Any] | Any:
        """
        Recursively appends escape_str to all keys matching values_to_marshall
        """
        if isinstance(data, dict):
            new_data: dict[Any, Any] = {}
            for k, v in cast(dict[Any, Any], data).items():
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
                DictUtils.marshall_keys_recursive(v, values_to_marshall)
                for v in cast(list[Any], data)
            ]
        else:
            return data

    @staticmethod
    def unmarshall_keys_recursive(
        data: Any, escape_str: str = DEFAULT_ESCAPE_STR
    ) -> dict[str, Any] | list[Any] | Any:
        """
        Recursively strips trailing escape_str, if present, from all keys
        """
        if isinstance(data, dict):
            new_data: dict[Any, Any] = {}
            for k, v in cast(dict[Any, Any], data).items():
                if k.endswith(escape_str):
                    new_k = k[:-1]
                    new_data[new_k] = DictUtils.unmarshall_keys_recursive(v)
                else:
                    new_data[k] = DictUtils.unmarshall_keys_recursive(v)
            return new_data
        elif isinstance(data, list):
            return [
                DictUtils.unmarshall_keys_recursive(v)
                for v in cast(list[Any], data)
            ]
        else:
            return data

    @staticmethod
    def cast_values_recursive(data: object, key: str, type: Type[Any]) -> object:
        """
        Recursively casts values to the given type for all items with matching keys
        """
        if isinstance(data, dict):
            new_data: dict[Any, Any] = {}
            for k, v in cast(dict[Any, Any], data).items():
                if k == key:
                    new_data[k] = type(v)
                else:
                    new_data[k] = DictUtils.cast_values_recursive(v, key, type)
            return new_data
        elif isinstance(data, list):
            return [
                DictUtils.cast_values_recursive(v, key, type)
                for v in cast(list[Any], data)
            ]
        else:
            return data
