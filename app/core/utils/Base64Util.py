import base64

class Base64Util:

    @staticmethod
    def decode_base64(base64_string: str) -> bytes:
        return base64.b64decode(base64_string)

    @staticmethod
    def base64_str_to_str(base64_string: str) -> str:
        decoded_bytes = Base64Util.decode_base64(base64_string)
        return decoded_bytes.decode("utf-8")

    @staticmethod
    def encode_base64(string: str) -> str:
        return base64.b64encode(string.encode("utf-8")).decode("utf-8")