# Healthcare Doorstep Services - Prototype

A full-stack web application for professional healthcare services at home.

## Tech Stack
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Backend**: Python, FastAPI, SQLite, SQLAlchemy
- **Auth**: JWT (JSON Web Tokens)

## Setup Instructions

### 1. Backend Setup
1. Navigate to the `backend` folder.
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy python-jose passlib bcrypt python-multipart
   ```
3. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### 2. Frontend Setup
1. Simply open `frontend/index.html` in your web browser.
2. Ensure the backend server is running for full functionality.

## Features
- **User Authentication**: Secure login and registration with mock OTP verification.
- **Service Booking**: Nursing, Doctor visits, and Blood services.
- **User Dashboard**: Manage profile and view service history.
- **Admin Panel**: Monitor users and system bookings.
- **Responsive Design**: Clean medical theme optimized for all devices.
