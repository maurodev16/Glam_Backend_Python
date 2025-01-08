# In models/salon_employees.py
from sqlalchemy import Integer, Table, Column, ForeignKey
from app.core.database import Base

# Association table for many-to-many relationship between users and salons
salon_employees = Table(
    'salon_employees',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('salon_id', Integer, ForeignKey('salons.id', ondelete='CASCADE'))
)

service_providers = Table(
    "service_providers",
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("users.id", ondelete='CASCADE')),
    Column("service_id", Integer, ForeignKey("offering_services.id", ondelete='CASCADE'))
)
