# app/core/utils/tenant_utils.py
from fastapi import Request
from sqlalchemy.orm import Query
from typing import Optional

def add_tenant_filter(query: Query, request: Request) -> Query:
    """
    Adiciona filtro de tenant à query
    """
    tenant_id = getattr(request.state, 'tenant_id', None)
    if tenant_id is not None:
        return query.filter_by(tenant_id=tenant_id)
    return query
