from enum import Enum
class UserRole(str, Enum):
    CLIENT = "client"
    SALON_OWNER = "salon_owner"
    ADMIN = "admin"
    EMPLOYEE = "employee"
    
from enum import Enum  # Importe Enum diretamente

class StatusRole(str, Enum):  # Use Enum em vez de enum.Enum
    ACTIVE = "active"
    INACTIVE = "inactive"
    
class DocumentType(str, Enum):
    CPF = "cpf"
    CNPJ = "cnpj"

class CommissionType(str, Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"
    
class AppointmentStatus(str, Enum):
    PENDING = "pending"        # Initial status when appointment is created
    CONFIRMED = "confirmed"    # Appointment confirmed by salon/provider
    COMPLETED = "completed"    # Service was provided successfully
    CANCELLED = "cancelled"    # Appointment cancelled by either party
    NO_SHOW =   "no_show"        # Client didn't show up

