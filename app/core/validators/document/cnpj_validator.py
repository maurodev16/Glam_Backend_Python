# app/core/validators/document/cnpj_validator.py
from .base_validator import DocumentValidator

class CNPJValidator(DocumentValidator):
    def validate(self, cnpj: str) -> bool:
        """Validate CNPJ number"""
        cleaned_cnpj = self._clean_document(cnpj)
        return self._validate_length(cleaned_cnpj) and self._validate_check_digits(cleaned_cnpj)
    
    def _validate_length(self, cnpj: str) -> bool:
        """Validate CNPJ length and repeated digits"""
        return len(cnpj) == 14 and len(set(cnpj)) > 1
    
    def _validate_check_digits(self, cnpj: str) -> bool:
        """Validate CNPJ check digits"""
        for i in range(12, 14):
            value = sum(int(cnpj[num]) * ((((i + 1) - num) % 8) + 2) for num in range(0, i))
            digit = ((value * 10) % 11) % 10
            if int(cnpj[i]) != digit:
                return False
        return True
