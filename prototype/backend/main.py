from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import datetime

from . import models, schemas, auth
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Healthcare Doorstep Services API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth Endpoints
auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Mock OTP verification log
    print(f"DEBUG: SMS OTP sent to {user.phone}: 123456")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        hashed_password=hashed_password,
        role=models.UserRole.USER
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@auth_router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Using UserCreate for convenience in prototype, usually OAuth2PasswordRequestForm
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# User Endpoints
user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@user_router.put("/me", response_model=schemas.User)
def update_user_me(user_update: schemas.UserUpdate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user

# Service Endpoints
service_router = APIRouter(prefix="/services", tags=["Services"])

@service_router.get("/", response_model=List[schemas.Service])
def list_services(db: Session = Depends(get_db)):
    return db.query(models.HealthcareService).all()

# Booking Endpoints
booking_router = APIRouter(prefix="/bookings", tags=["Bookings"])

@booking_router.post("/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    new_booking = models.Booking(
        **booking.dict(),
        user_id=current_user.id,
        status="Pending",
        booking_date=datetime.datetime.utcnow()
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@booking_router.get("/history", response_model=List[schemas.Booking])
def get_booking_history(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Booking).filter(models.Booking.user_id == current_user.id).all()

# Blood Service Endpoints
blood_router = APIRouter(prefix="/blood", tags=["Blood Service"])

@blood_router.post("/request", response_model=schemas.BloodRequestCreate)
def blood_request(request: schemas.BloodRequestCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    new_request = models.BloodRequest(
        **request.dict(),
        user_id=current_user.id,
        status="Pending"
    )
    db.add(new_request)
    db.commit()
    return request

# Cold Storage Endpoints
cold_storage_router = APIRouter(prefix="/cold-storage", tags=["Cold Storage"])

@cold_storage_router.post("/request", response_model=schemas.ColdStorageRequestCreate)
def cold_storage_request(request: schemas.ColdStorageRequestCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    new_request = models.ColdStorageRequest(
        **request.dict(),
        user_id=current_user.id,
        status="Pending",
        request_date=datetime.datetime.utcnow()
    )
    db.add(new_request)
    db.commit()
    return request

# Admin Endpoints
admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.get("/users", response_model=List[schemas.User])
def list_all_users(admin: models.User = Depends(auth.check_admin), db: Session = Depends(get_db)):
    return db.query(models.User).all()

@admin_router.get("/bookings", response_model=List[schemas.Booking])
def list_all_bookings(admin: models.User = Depends(auth.check_admin), db: Session = Depends(get_db)):
    return db.query(models.Booking).all()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(service_router)
app.include_router(booking_router)
app.include_router(blood_router)
app.include_router(cold_storage_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Welcome to Healthcare Doorstep Services API"}
