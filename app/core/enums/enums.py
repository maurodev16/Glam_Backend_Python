import enum

class UserRole(str, enum.Enum):
    CLIENT = "client"
    SALON_OWNER = "salon_owner"
    ADMIN = "admin"
    
class StatusRole(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
