from typing import Protocol, Optional, Dict, List

class IBooksProvider(Protocol):
    def list_books(self) -> List[Dict]:
        ...
    def get_book(self, isbn: str) -> Optional[Dict]:
        ...