# app/core/validators/document/cpf_validator.py
from .base_validator import DocumentValidator

class CPFValidator(DocumentValidator):
    def validate(self, cpf: str) -> bool:
        """Validate CPF number"""
        cleaned_cpf = self._clean_document(cpf)
        return self._validate_length(cleaned_cpf) and self._validate_check_digits(cleaned_cpf)
    
    def _validate_length(self, cpf: str) -> bool:
        """Validate CPF length and repeated digits"""
        return len(cpf) == 11 and len(set(cpf)) > 1
    
    def _validate_check_digits(self, cpf: str) -> bool:
        """Validate CPF check digits"""
        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if int(cpf[i]) != digit:
                return False
        return True
