from .create_tenant_service import CreateTenantService
from .update_tenant_service import UpdateTenantService
from .get_tenant_service import GetTenantService
from .delete_tenant_service import DeleteTenantService

class TenantService:
    # Create operations
    create_tenant = CreateTenantService.create
    
    # Read operations
    get_tenant = GetTenantService.get_by_id
    list_tenants = GetTenantService.list_all
    list_active_tenants = GetTenantService.list_active
    
    # Update operations
    update_tenant = UpdateTenantService.update
    
    # Delete operations
    delete_tenant = DeleteTenantService.delete

__all__ = ['TenantService']