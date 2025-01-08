# app/core/validators/document/base_validator.py
from abc import ABC, abstractmethod

class DocumentValidator(ABC):
    @abstractmethod
    def validate(self, document: str) -> bool:
        pass

    def _clean_document(self, document: str) -> str:
        return ''.join(filter(str.isdigit, document))
