from .base import Base
from .user_model import User
from .salon_model import Salon
from .services_model import Service
from .professional_model import Professional
from .professional_service_model import ProfessionalService
from .client_model import Client
from .appointment_model import Appointment
from .business_hours_model import BusinessHours
from .portfolio_item_model import PortfolioItem
from .rating_model import Rating


# This allows importing all models from the models package
__all__ = ['Base', 'User', 'Salon', 'Service', 'Professional', 'ProfessionalService', 'Client', 'Appointment', 'BusinessHours', 'PortfolioItem', 'Rating']