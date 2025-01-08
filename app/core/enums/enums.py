import enum

class UserRole(str, enum.Enum):
    CLIENT = "client"
    SALON_OWNER = "salon_owner"
    ADMIN = "admin"
    EMPLOYEE = "employee"
    
class StatusRole(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    
class DocumentType(str, enum.Enum):
    CPF = "cpf"
    CNPJ = "cnpj"
from enum import Enum

class CommissionType(str, Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"
class AppointmentStatus(str, Enum):
    PENDING = "pending"        # Initial status when appointment is created
    CONFIRMED = "confirmed"    # Appointment confirmed by salon/provider
    COMPLETED = "completed"    # Service was provided successfully
    CANCELLED = "cancelled"    # Appointment cancelled by either party
    NO_SHOW = "no_show"       # Client didn't show up

