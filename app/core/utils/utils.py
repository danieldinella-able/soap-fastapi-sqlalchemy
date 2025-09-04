"""Raccolta di utility generiche per dict, parsing sicuro e token."""

import ast
import random
import secrets
import string
from typing import Mapping, Any

from app.core.utils.logger import log_warning


class Utils:

    @staticmethod
    def merge_dict(orig_dict, new_dict):
        """Fonde ricorsivamente due dizionari (sovrascrive valori)."""
        for key, val in new_dict.items():
            if isinstance(val, Mapping):
                tmp = Utils.merge_dict(orig_dict.get(key, {}), val)
                orig_dict[key] = tmp
            else:
                orig_dict[key] = new_dict[key]
        return orig_dict

    @staticmethod
    def random_string(string_length):
        """Genera stringa casuale alfanumerica della lunghezza richiesta."""
        symbols = string.ascii_letters + string.digits
        return ''.join(random.choices(symbols, k=string_length))

    @staticmethod
    def try_parse_python_obj(value: str, expected_type=None, default: Any = None):
        """Esegue `ast.literal_eval` restituendo `default` in caso di errore o tipo inatteso."""
        try:
            converted_object = ast.literal_eval(value)
        except (ValueError, SyntaxError) as e:
            log_warning(f"literal_eval failed: {e}; \n value: {value}")
            return default

        if expected_type is not None and not isinstance(converted_object, expected_type):
            return default
        return converted_object

    @staticmethod
    def generate_token(length: int):
        """Genera token esadecimale sicuro (lunghezza in byte)."""
        return secrets.token_hex(length)

    @staticmethod
    def get_or_default_with_type_check_none(collection, key, default_value):
        """Restituisce il valore di `key` o `default_value`, convertendo al tipo di default."""
        default_type = type(default_value)
        if not collection:
            return default_value
        value = collection.get(key, None)
        if value is None:
            value = default_value
        return default_type(value)
