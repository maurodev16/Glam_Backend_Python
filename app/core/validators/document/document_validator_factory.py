# app/core/validators/document/document_validator_factory.py
from typing import Dict, Type
from .base_validator import DocumentValidator
from .cpf_validator import CPFValidator
from .cnpj_validator import CNPJValidator

class DocumentValidatorFactory:
    _validators: Dict[str, Type[DocumentValidator]] = {
        'cpf': CPFValidator,
        'cnpj': CNPJValidator
    }

    @classmethod
    def get_validator(cls, document_type: str) -> DocumentValidator:
        validator_class = cls._validators.get(document_type.lower())
        if not validator_class:
            raise ValueError(f"No validator found for document type: {document_type}")
        return validator_class()
