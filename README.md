# 🏥 Healthcare Backend API & Testing Platform

A secure, production-grade RESTful backend system for a healthcare application built with **Django**, **Django REST Framework (DRF)**, and **PostgreSQL**.

The system provides robust JWT authentication, patient record management with ownership-based access control, a public doctor directory with creator-restricted management, relational patient-doctor mappings, and hardened defense-in-depth security against SQL injection, XSS, IDOR, and adversarial AI prompt injections.

---

## 🌟 Key Highlights

- **JWT Authentication** (`djangorestframework-simplejwt`): Stateless access and refresh tokens with automatic token rotation, blacklist capability, and dedicated refresh endpoint.
- **Data Isolation & Ownership Control**: Patients are strictly isolated per user account. Doctors are globally viewable, but only modifiable/deletable by their creator.
- **Relational Integrity**: Patient-Doctor mappings enforce unique constraints at the database level to prevent duplicate assignments.
- **Zero-Tolerance Input Sanitization**: Centralized strict HTML tag, event handler (`onerror`, `onload`), and null byte (`\x00`) stripping to neutralize stored XSS and PostgreSQL string corruption.
- **Adversarial Jailbreak & Prompt Injection Defense**: Malicious prompt injections and template injection strings (`{{7*7}}`) are sanitized and stored as inert passive text without privilege escalation.
- **Built-in Scalability**: PostgreSQL connection pooling (`CONN_MAX_AGE = 600`), persistent connection health checks, `GZipMiddleware` HTTP response compression, and in-memory caching.
- **Two Interactive UIs for Testing**:
  - **Swagger UI** live at `/api/docs/` powered by a standard-compliant `openapi.yaml` specification.
  - **Streamlit Testing Dashboard** live at `http://localhost:8501` featuring one-click demo login, CRUD forms, and live security attack demonstrations.
- **Automated Test Suite**: 72 comprehensive tests covering authentication, CRUD, business rules, edge cases, and security exploits.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.13+ | Core runtime |
| **Framework** | Django 5.1 & DRF 3.17 | Web framework & RESTful API toolkit |
| **Database** | PostgreSQL | Relational ACID database with indexed lookups |
| **Authentication** | SimpleJWT (`PyJWT`) | Stateless Bearer JWT tokens with rotation |
| **Sanitization** | Bleach | Zero-tolerance HTML and attribute stripping |
| **Configuration** | python-decouple | 12-Factor environment variable management |
| **API Specification** | OpenAPI 3.0.3 & Swagger UI | Interactive documentation and schema |
| **Testing UI** | Streamlit | Interactive testing dashboard |

---

## 📋 System Architecture & Project Structure

```
Whatbytes_Django/
├── healthcare_backend/         # Core project configuration
│   ├── settings.py             # Hardened settings, connection pooling & cache
│   ├── urls.py                 # Root URL routing, Swagger UI & OpenAPI views
│   ├── sanitizer.py            # Centralized HTML & null byte input sanitizer
│   ├── utils.py                # Standardized custom DRF exception handler
│   ├── wsgi.py                 # Production WSGI application
│   └── asgi.py                 # ASGI application
├── authentication/             # User registration, login & JWT tokens
│   ├── serializers.py          # Input validation, password strength checks
│   ├── views.py                # RegisterView, LoginView
│   └── urls.py                 # /api/auth/ routes
├── patients/                   # Patient management & ownership control
│   ├── models.py               # Patient model with created_by FK and indexes
│   ├── serializers.py          # Serializer with date of birth & phone validation
│   ├── views.py                # PatientListCreateView, PatientDetailView
│   └── urls.py                 # /api/patients/ routes
├── doctors/                    # Doctor directory & profiles
│   ├── models.py               # Doctor model with unique license & specialization
│   ├── serializers.py          # License uniqueness & experience validators
│   ├── views.py                # DoctorListCreateView, DoctorDetailView
│   └── urls.py                 # /api/doctors/ routes
├── mappings/                   # Patient-Doctor assignments
│   ├── models.py               # PatientDoctorMapping with UniqueConstraint
│   ├── serializers.py          # Relational serializer with nested object names
│   ├── views.py                # MappingListCreateView, MappingByPatientView, MappingDeleteView
│   └── urls.py                 # /api/mappings/ routes
├── tests/                      # Comprehensive 72-test security & feature suite
│   └── test_security_and_features.py
├── openapi.yaml                # OpenAPI 3.0.3 specification file
├── streamlit_app.py            # Interactive Streamlit evaluation dashboard
├── seed_data.json              # Pre-seeded database fixture (users, doctors, patients)
├── Dockerfile                  # Container definition for Django & Streamlit
├── docker-compose.yml          # Multi-container orchestration (DB, API, Streamlit)
├── .dockerignore               # Docker build exclusions
├── requirements.txt            # Project dependencies
├── .env.example                # Template for environment variables
├── .gitignore                  # Git ignore rules
└── manage.py                   # Django CLI management script
```

---

## 🚀 Quickstart & Setup Guide

Choose between the **1-Click Docker Setup** (fastest and zero-configuration) or the standard **Local Virtual Environment Setup**.

### 🐳 Option A: 1-Click Docker Setup (Recommended)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

```bash
# 1. Clone the repository
git clone https://github.com/Saksham0121/Whatbytes_assignment.git
cd Whatbytes_assignment

# 2. Build and launch all services with a single command
docker-compose up --build
```

> **Tip**: If you previously started Django or Streamlit locally in a terminal, stop them (`Ctrl+C`) before running `docker-compose up` so host ports `8000` and `8501` are free.

**What Docker automatically does for you:**
1. Spins up a dedicated **PostgreSQL 16** container with built-in health checks.
2. Applies all Django database migrations.
3. Automatically pre-populates initial seed data ([`seed_data.json`](seed_data.json)).
4. Starts the **Django REST API** on [http://localhost:8000](http://localhost:8000).
5. Starts the **Streamlit Interactive Testing Dashboard** on [http://localhost:8501](http://localhost:8501).

---

### 💻 Option B: Local Virtual Environment Setup

#### 1. Prerequisites
Ensure you have **Python 3.11+** and **PostgreSQL** installed and running on your system.

#### 2. Clone the Repository
```bash
git clone https://github.com/Saksham0121/Whatbytes_assignment.git
cd Whatbytes_assignment
```

#### 3. Create & Activate Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Configure Environment Variables
Create a `.env` file in the project root based on `.env.example`:
```bash
cp .env.example .env
```
Update `.env` with your PostgreSQL database credentials:
```ini
# Django Settings
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_CONN_MAX_AGE=600

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

#### 6. Create PostgreSQL Database
Ensure your PostgreSQL server is running, then create the database:
```bash
psql -U postgres -c "CREATE DATABASE healthcare_db;"
```

#### 7. Run Database Migrations & Load Seed Data
```bash
venv/bin/python manage.py makemigrations
venv/bin/python manage.py migrate

# (Recommended) Load sample users, doctors, patients, and mappings instantly:
venv/bin/python manage.py loaddata seed_data.json
```

#### 8. Run the Development Server
```bash
venv/bin/python manage.py runserver
```
*(If port 8000 is occupied, run `venv/bin/python manage.py runserver 8001`)*

The API will be live at `http://localhost:8000/` (automatically redirects to Swagger UI).

#### 9. Run the Streamlit Dashboard (In a separate terminal)
```bash
source venv/bin/activate
streamlit run streamlit_app.py
```

---

### 🔑 Pre-Seeded Test Credentials

Loading [`seed_data.json`](seed_data.json) provides pre-configured credentials for immediate testing:

| Account Role | Username / Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Superuser / Admin** | `admin` | `AdminPassword123!` | Full database inspection & management at `/admin/` and all APIs |
| **Doctor / User** | `saksham@gmail.com` | `Password123!` | Patient & Doctor CRUD, Relational Mappings, Streamlit UI |

---

## 🧪 Running the Test Suite (72 Tests)

The repository includes a comprehensive 72-test test suite covering all functional modules and security exploit scenarios:

```bash
venv/bin/python manage.py test tests
```

---

## 🖥️ Interactive Testing Interfaces

### 1. Interactive Swagger UI
Explore and execute live requests against the backend directly from your web browser:
* **Swagger UI Documentation**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
* **Raw OpenAPI Specification**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)
* **OpenAPI 3.0 File**: Located in root as [`openapi.yaml`](openapi.yaml) (ready for Postman or Insomnia import).

> **Tip for Swagger UI**: To test protected endpoints, register or login to receive an access token, click the green **Authorize** button at the top right, and enter `Bearer <your_token>`.

### 2. Streamlit Testing Dashboard
A dedicated, tester-friendly UI designed for rapid end-to-end testing and verification:
```bash
venv/bin/streamlit run streamlit_app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser to access:
* **1-Click Demo Login**: Instantly login as QA Tester without manually typing credentials.
* **Patient & Doctor Management**: Create, browse, inspect, and delete records with live tabular displays.
* **Patient-Doctor Assignment**: Seamlessly assign doctors to patients with smart auto-populated dropdowns.
* **Interactive Security Playground**: Execute live SQLi, XSS, IDOR, and AI prompt injection attacks to verify real-time neutralization.

### 3. Django Database Admin Panel
Direct visual inspection, search, and table editing:
* **Admin Panel URL**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* **Username**: `admin`
* **Password**: `AdminPassword123!`

---

## 🛡️ Security & Scalability Architecture

### 1. Security Defenses
* **SQL Injection Prevention**: Zero raw SQL queries. All interactions use Django's parameterized ORM. Parameter values are passed separately from query structure, rendering SQL injection payloads (`' OR '1'='1`, `'; DROP TABLE...`) completely ineffective.
* **Stored XSS Prevention**: All text fields across all serializers run through `healthcare_backend/sanitizer.py` powered by `bleach`. All HTML tags (`<script>`, `<iframe>`, `<img>`), dangerous attributes, and JavaScript event handlers (`onerror`, `onload`) are unconditionally stripped.
* **PostgreSQL Null Byte Protection**: Null bytes (`\x00`) are explicitly stripped and rejected by DRF `CharField` validators, preventing database corruption and string termination bypasses.
* **Insecure Direct Object Reference (IDOR)**:
  * Patients are scoped by `created_by=request.user`. Attempting to retrieve another user's patient returns `404 Not Found`.
  * Doctors are publicly viewable, but modification (`PUT`) and deletion (`DELETE`) require `doctor.created_by == request.user`, otherwise returning `403 Forbidden`.
* **Adversarial AI Prompt Injection & SSTI**: Medical notes or patient descriptions containing jailbreak instructions (`Ignore previous instructions...`, `SYSTEM OVERRIDE`, `{{7*7}}`) are sanitized and stored strictly as passive string data without evaluation.
* **JWT Integrity & Algorithm Enforcement**: Unsigned tokens using `"alg": "none"` and tampered payload signatures are rejected with `401 Unauthorized`.
* **Rate Limiting / Anti-DDoS**: Configured via DRF throttles (`AnonRateThrottle` at 30 requests/min, `UserRateThrottle` at 100 requests/min).
* **Production Security Headers**: When `DEBUG = False`, enables HSTS (1 year), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `SECURE_SSL_REDIRECT`, and cookie security flags.

### 2. Scalability Enhancements
* **Database Connection Pooling**: Configured `CONN_MAX_AGE = 600` and `CONN_HEALTH_CHECKS = True`. PostgreSQL connections remain open across requests, reducing TCP/TLS connection handshake overhead by up to 80-90% under high concurrency.
* **Query Optimization (Zero N+1 Traps)**: Relational endpoints utilize `PatientDoctorMapping.objects.select_related("patient", "doctor")` to fetch related foreign keys in a single SQL JOIN query.
* **Response Compression**: Integrated `django.middleware.gzip.GZipMiddleware` to automatically compress JSON payloads exceeding 200 bytes, maximizing network throughput.
* **In-Memory Cache**: Configured thread-safe `django.core.cache.backends.locmem.LocMemCache` for lightning-fast memory operations without extra infrastructure overhead.
* **Database Indexing**: Targeted database indexes applied to `Doctor.specialization`, `Patient.created_by`, `Doctor.created_by`, and composite indexes on `(last_name, first_name)`.

---

## 📚 RESTful API Specification

### Authentication APIs

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Register a new user | No |
| `POST` | `/api/auth/login/` | Log in user and receive JWT access & refresh tokens | No |
| `POST` | `/api/auth/token/refresh/` | Obtain fresh access token using refresh token | No |

### Patient Management APIs

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/patients/` | Add a new patient record (sanitized) | Yes |
| `GET` | `/api/patients/` | Retrieve all patients created by requesting user | Yes |
| `GET` | `/api/patients/<id>/` | Get details of a specific owned patient | Yes |
| `PUT` | `/api/patients/<id>/` | Update owned patient details | Yes |
| `DELETE` | `/api/patients/<id>/` | Permanently delete an owned patient record | Yes |

### Doctor Management APIs

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/doctors/` | Add a new doctor with unique license | Yes |
| `GET` | `/api/doctors/` | Retrieve all registered doctors | Yes |
| `GET` | `/api/doctors/<id>/` | Get details of a specific doctor | Yes |
| `PUT` | `/api/doctors/<id>/` | Update doctor details (creator only) | Yes (Creator) |
| `DELETE` | `/api/doctors/<id>/` | Delete doctor record (creator only) | Yes (Creator) |

### Patient-Doctor Mapping APIs

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/mappings/` | Assign a doctor to a patient (prevents duplicates) | Yes |
| `GET` | `/api/mappings/` | Retrieve all patient-doctor mappings | Yes |
| `GET` | `/api/mappings/<patient_id>/` | Get all doctors assigned to a specific patient | Yes |
| `DELETE` | `/api/mappings/<id>/` | Remove doctor from patient by mapping ID | Yes |
| `DELETE` | `/api/mappings/<id>/delete/` | Remove doctor from patient (URL alias) | Yes |

---

## 💡 Practical cURL Examples

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com",
    "password": "StrongPassword123!",
    "password_confirm": "StrongPassword123!"
  }'
```

### 2. User Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane.doe@example.com",
    "password": "StrongPassword123!"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful.",
  "data": {
    "user": {
      "id": 1,
      "email": "jane.doe@example.com",
      "first_name": "Jane",
      "last_name": "Doe"
    },
    "tokens": {
      "access": "eyJhbGciOiJIUzI1Ni...",
      "refresh": "eyJhbGciOiJIUzI1Ni..."
    }
  }
}
```

### 3. Create a Patient
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "first_name": "Alice",
    "last_name": "Smith",
    "date_of_birth": "1990-05-15",
    "gender": "F",
    "phone": "+1-555-0199",
    "email": "alice.smith@example.com",
    "address": "742 Evergreen Terrace",
    "medical_history": "No known allergies. Routine health checks normal."
  }'
```

### 4. Register a Doctor
```bash
curl -X POST http://localhost:8000/api/doctors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "first_name": "Gregory",
    "last_name": "House",
    "specialization": "cardiology",
    "phone": "+1-555-0144",
    "email": "dr.house@hospital.org",
    "license_number": "MED-LIC-998811",
    "years_of_experience": 15
  }'
```

### 5. Assign Doctor to Patient
```bash
curl -X POST http://localhost:8000/api/mappings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "patient": 1,
    "doctor": 1
  }'
```

### 6. Query Doctors by Patient ID
```bash
curl -X GET http://localhost:8000/api/mappings/1/ \
  -H "Authorization: Bearer <access_token>"
```

### 7. Delete Mapping by ID
```bash
curl -X DELETE http://localhost:8000/api/mappings/1/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 🔒 Environment Variables Reference

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | *(django-insecure...)* | Cryptographic signing key for Django |
| `DEBUG` | `True` | Debug mode (`True` for local, `False` for production) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Whitelisted HTTP Host header domains |
| `DB_NAME` | `healthcare_db` | PostgreSQL database name |
| `DB_USER` | `postgres` | PostgreSQL username |
| `DB_PASSWORD` | `postgres` | PostgreSQL password |
| `DB_HOST` | `localhost` | PostgreSQL host address |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_CONN_MAX_AGE` | `600` | Connection persistence lifetime (seconds) |
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | `60` | Access token lifespan before refresh required |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | `7` | Refresh token valid lifespan |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000...` | Whitelisted cross-origin domains |
