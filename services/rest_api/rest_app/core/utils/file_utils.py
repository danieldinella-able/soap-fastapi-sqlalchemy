from pathlib import PurePosixPath

import json
from pathlib import Path


class FileUtil:
    @staticmethod
    def separate_file_name(filename):
        file = PurePosixPath(filename)
        file_name = file.name  # e.g. 'file.pdf'
        extension = file.suffix  # e.g. '.pdf'
        if not file_name or not extension:
            return None
        return {'name': file_name, 'extension': extension}

    @staticmethod
    def save_to_json_file(data: list[dict]|dict, filepath: str | Path, indent: int = 2):
        path = Path(filepath)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        print(f"[OK] Dati salvati in {path.resolve()}")
