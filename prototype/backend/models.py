from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from .database import Base
import datetime

class UserRole(str, enum.Enum):
    USER = "user"
    PROFESSIONAL = "professional"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.USER)
    address = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    bookings = relationship("Booking", back_populates="user")

class HealthcareService(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    icon = Column(String)  # Material icon name or SVG path

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    status = Column(String, default="Pending") # Pending, Confirmed, Completed, Cancelled
    booking_date = Column(DateTime, default=datetime.datetime.utcnow)
    scheduled_date = Column(DateTime)
    address = Column(String)

    user = relationship("User", back_populates="bookings")

class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    blood_group = Column(String)
    hospital_name = Column(String)
    reason = Column(String)
    urgency = Column(String) # Normal, Emergency
    status = Column(String, default="Pending")

class ColdStorageRequest(Base):
    __tablename__ = "cold_storage_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_type = Column(String)
    duration_days = Column(Integer)
    status = Column(String, default="Pending")
    request_date = Column(DateTime, default=datetime.datetime.utcnow)
