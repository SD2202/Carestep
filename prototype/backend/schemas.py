from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class User(UserBase):
    id: int
    role: str
    address: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class ServiceBase(BaseModel):
    name: str
    description: str
    price: float
    icon: str

class Service(ServiceBase):
    id: int

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    service_id: int
    scheduled_date: datetime
    address: str

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    user_id: int
    status: str
    booking_date: datetime

    class Config:
        from_attributes = True

class BloodRequestCreate(BaseModel):
    blood_group: str
    hospital_name: str
    reason: str
    urgency: str

class ColdStorageRequestCreate(BaseModel):
    item_type: str
    duration_days: int
