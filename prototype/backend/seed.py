from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, auth

def seed_services():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    services = [
        models.HealthcareService(
            id=1,
            name="Nursing at Doorstep",
            description="Professional nursing care for injections, dressing, and patient monitoring.",
            price=500.0,
            icon="medical_services"
        ),
        models.HealthcareService(
            id=2,
            name="Doctor Home Visit",
            description="General physician consultation in the comfort of your home.",
            price=1500.0,
            icon="stethoscope"
        ),
        models.HealthcareService(
            id=3,
            name="Physiotherapy",
            description="Expert physiotherapy sessions for recovery and pain management.",
            price=1000.0,
            icon="exercise"
        ),
        models.HealthcareService(
            id=4,
            name="Lab Tests at Home",
            description="Sample collection for blood tests and other diagnostic requirements.",
            price=400.0,
            icon="biotech"
        )
    ]

    try:
        if db.query(models.HealthcareService).count() == 0:
            services = [
                models.HealthcareService(id=1, name="Nursing at Doorstep", description="Care at home", price=500, icon="medical_services"),
                models.HealthcareService(id=2, name="Doctor Home Visit", description="Consultation", price=1200, icon="stethoscope"),
                models.HealthcareService(id=3, name="Physiotherapy", description="Recovery", price=800, icon="exercise"),
                models.HealthcareService(id=4, name="Lab Tests at Home", description="Diagnostics", price=300, icon="biotech")
            ]
            db.add_all(services)
            print("Seeded services.")

        # Add or update specialized professional users
        users = [
            models.User(email="doctor@carestep.in", full_name="Dr. Sarah Johnson", phone="9988776655", hashed_password=auth.get_password_hash("doctor123"), role=models.UserRole.DOCTOR),
            models.User(email="nurse@carestep.in", full_name="Nurse Emily", phone="8877665544", hashed_password=auth.get_password_hash("nurse123"), role=models.UserRole.NURSE),
            models.User(email="blood@carestep.in", full_name="Red Cross Partner", phone="7766554433", hashed_password=auth.get_password_hash("blood123"), role=models.UserRole.BLOOD_SERVICE),
            models.User(email="physio@carestep.in", full_name="Dr. Alex Reed", phone="6655443322", hashed_password=auth.get_password_hash("physio123"), role=models.UserRole.PHYSIOTHERAPIST),
            models.User(email="admin@carestep.in", full_name="System Admin", phone="1234567890", hashed_password=auth.get_password_hash("admin123"), role=models.UserRole.ADMIN)
        ]

        for u in users:
            existing = db.query(models.User).filter(models.User.email == u.email).first()
            if not existing:
                db.add(u)
                print(f"Seeded user: {u.email}")
        
        db.commit()
    except Exception as e:
        print(f"Error seeding services: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_services()
