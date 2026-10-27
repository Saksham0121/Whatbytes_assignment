# Healthcare Backend API

A secure RESTful backend system for a healthcare application built with **Django**, **Django REST Framework**, and **PostgreSQL**. Supports user authentication (JWT), patient management, doctor management, and patient-doctor assignment mappings.

---

## Tech Stack

- **Python 3.13+**
- **Django 5.1**
- **Django REST Framework 3.17**
- **PostgreSQL**
- **JWT Authentication** (`djangorestframework-simplejwt`)
- **Bleach** (input sanitization)
- **python-decouple** (environment variable management)

---

## Security Features

- **JWT Authentication** — stateless, token-based auth with access/refresh token rotation
- **SQL Injection Prevention** — Django ORM uses parameterized queries exclusively
- **XSS Protection** — all text inputs sanitized with `bleach` before storage
- **Input Validation** — serializer-level validation on all fields
- **Password Security** — Django's PBKDF2 hasher with password strength validation
- **Rate Limiting** — 30 req/min for anonymous, 100 req/min for authenticated users
- **CORS Protection** — whitelisted origins only
- **Security Headers** — HSTS, XSS filter, content type sniffing prevention (production)
- **Environment Variables** — secrets never hardcoded in source code
- **Ownership-based Access Control** — users can only modify their own records

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd Whatbytes_Django
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials and secret key
```

### 5. Create PostgreSQL database

```bash
psql -U postgres
CREATE DATABASE healthcare_db;
\q
```

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`.

---

## API Endpoints

### Authentication

| Method | Endpoint               | Description                    | Auth Required |
|--------|------------------------|--------------------------------|---------------|
| POST   | `/api/auth/register/`  | Register a new user            | No            |
| POST   | `/api/auth/login/`     | Login and get JWT tokens       | No            |

### Patients

| Method | Endpoint               | Description                          | Auth Required |
|--------|------------------------|--------------------------------------|---------------|
| POST   | `/api/patients/`       | Create a new patient                 | Yes           |
| GET    | `/api/patients/`       | List all patients (own records only) | Yes           |
| GET    | `/api/patients/<id>/`  | Get patient details                  | Yes           |
| PUT    | `/api/patients/<id>/`  | Update patient details               | Yes           |
| DELETE | `/api/patients/<id>/`  | Delete a patient record              | Yes           |

### Doctors

| Method | Endpoint               | Description              | Auth Required |
|--------|------------------------|--------------------------|---------------|
| POST   | `/api/doctors/`        | Create a new doctor      | Yes           |
| GET    | `/api/doctors/`        | List all doctors         | Yes           |
| GET    | `/api/doctors/<id>/`   | Get doctor details       | Yes           |
| PUT    | `/api/doctors/<id>/`   | Update doctor details    | Yes (creator) |
| DELETE | `/api/doctors/<id>/`   | Delete a doctor record   | Yes (creator) |

### Patient-Doctor Mappings

| Method | Endpoint                        | Description                             | Auth Required |
|--------|---------------------------------|-----------------------------------------|---------------|
| POST   | `/api/mappings/`                | Assign a doctor to a patient            | Yes           |
| GET    | `/api/mappings/`                | List all mappings                       | Yes           |
| GET    | `/api/mappings/<patient_id>/`   | Get all doctors for a specific patient  | Yes           |
| DELETE | `/api/mappings/<id>/delete/`    | Remove a doctor from a patient          | Yes           |

---

## Request/Response Examples

### Register a User

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Create a Patient (with JWT token)

```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "date_of_birth": "1990-05-15",
    "gender": "F",
    "phone": "+1-555-0123"
  }'
```

---

## Project Structure

```
Whatbytes_Django/
├── healthcare_backend/     # Main project configuration
│   ├── settings.py         # Security-hardened settings
│   ├── urls.py             # Root URL routing
│   ├── utils.py            # Custom exception handler
│   └── wsgi.py
├── authentication/         # User registration & login
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── patients/               # Patient CRUD
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── doctors/                # Doctor CRUD
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── mappings/               # Patient-Doctor assignments
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── .env.example            # Environment variable template
├── .gitignore
├── requirements.txt
└── manage.py
```
