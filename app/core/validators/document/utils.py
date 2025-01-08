# app/core/validators/document/utils.py
import re

def clean_document_number(document: str) -> str:
    """Remove non-numeric characters from document number"""
    return re.sub(r'[^0-9]', '', document)
