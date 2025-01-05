import re

def validate_cpf(cpf: str) -> bool:
    """Validate CPF number"""
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        return False
        
    # Verifica se todos os dígitos são iguais
    if len(set(cpf)) == 1:
        return False
        
    # Validação dos dígitos verificadores
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if int(cpf[i]) != digit:
            return False
    return True

def validate_cnpj(cnpj: str) -> bool:
    """Validate CNPJ number"""
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    if len(cnpj) != 14:
        return False
        
    # Verifica se todos os dígitos são iguais
    if len(set(cnpj)) == 1:
        return False
        
    # Validação dos dígitos verificadores
    for i in range(12, 14):
        value = sum(int(cnpj[num]) * ((((i + 1) - num) % 8) + 2) for num in range(0, i))
        digit = ((value * 10) % 11) % 10
        if int(cnpj[i]) != digit:
            return False
    return True

def validate_document(document_type: str, document: str) -> bool:
    """Validate document based on type"""
    document = re.sub(r'[^0-9]', '', document)
    
    if document_type == "cpf":
        return validate_cpf(document)
    elif document_type == "cnpj":
        return validate_cnpj(document)
    return False