# app/core/validators/document/__init__.py
from .cpf_validator import validate_cpf
from .cnpj_validator import validate_cnpj

def validate_document(document_type: str, document: str) -> bool:
    """Validate document based on type"""
    if document_type == "cpf":
        return validate_cpf(document)
    elif document_type == "cnpj":
        return validate_cnpj(document)
    return False

__all__ = ['validate_document', 'validate_cpf', 'validate_cnpj']
