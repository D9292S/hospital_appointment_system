# Hospital Appointment Booking API — Hack the Web

A beginner-friendly FastAPI debugging challenge designed for second-year students. The project contains intentionally broken code that participants must investigate, debug, and fix.

## 1. Technology Stack

- Python 3.10+
- FastAPI — REST API framework
- SQLAlchemy 2.x — ORM and database access
- SQLite — local database
- Pydantic — request and response validation
- Pytest and HTTPX — automated testing

## 2. Setup and Run

### Step 1: Clone the repository

```bash
git clone <repository-url>
cd hospital_booking_hackathon
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start the API server

```bash
uvicorn app.main:app --reload
```

The application will run at:

- **API Base URL:** http://127.0.0.1:8000
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **Health Check:** http://127.0.0.1:8000/

Use Swagger UI to inspect endpoints, submit requests, and examine responses.

## 3. Project Structure

```text
hospital_booking_hackathon/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       ├── doctors.py
│       └── appointments.py
├── issues/
│   └── ISSUES.md
├── organizer/
│   └── ANSWER_KEY.md
├── tests/
│   ├── conftest.py
│   ├── test_doctors.py
│   └── test_appointments.py
├── .gitignore
└── requirements.txt
```

### File descriptions

- `app/main.py`: Creates the FastAPI application, initializes database tables, and registers routers.
- `app/database.py`: Configures the SQLite database, SQLAlchemy engine, session factory, and database dependency.
- `app/models.py`: Defines the Doctor, Patient, and Appointment database models.
- `app/schemas.py`: Defines Pydantic schemas for validating incoming requests and formatting responses.
- `app/routers/doctors.py`: Handles doctor registration, doctor listing, specialization search, doctor lookup, and patient registration.
- `app/routers/appointments.py`: Handles appointment booking, listing, cancellation, rescheduling, and status updates.
- `issues/ISSUES.md`: Contains the nine debugging issues and their acceptance criteria.
- `tests/`: Contains automated tests for the expected API behavior.
- `organizer/ANSWER_KEY.md`: Contains the intended solutions for organizers. Remove this directory before distributing the challenge to participants if solutions must remain private.

## 4. API Documentation

All endpoints accept or return JSON unless otherwise specified.

### A. Root Endpoint

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks whether the API is running |

Example response:

```json
{
  "message": "Hospital Appointment Booking API is running"
}
```

### B. Doctor Endpoints

| Method | Endpoint | Description | Expected Success |
|---|---|---|---|
| POST | `/doctors` | Register a new doctor | 201 Created |
| GET | `/doctors` | Retrieve all doctors | 200 OK |
| GET | `/doctors?specialization=Cardiology` | Filter doctors by specialization | 200 OK |
| GET | `/doctors/{doctor_id}` | Retrieve a doctor by ID | 200 OK |

#### 1. Register a doctor

**Endpoint:** `POST /doctors`

Request body:

```json
{
  "name": "Dr Asha Sharma",
  "specialization": "Cardiology",
  "consultation_fee": 500
}
```

Fields:

- `name`: Doctor's name, between 2 and 100 characters.
- `specialization`: Medical specialization, between 2 and 100 characters.
- `consultation_fee`: Consultation fee. Negative values must be rejected.

Example response:

```json
{
  "id": 1,
  "name": "Dr Asha Sharma",
  "specialization": "Cardiology",
  "consultation_fee": 500.0
}
```

A successful creation should return `201 Created`.

#### 2. List and search doctors

**Endpoint:** `GET /doctors`

Retrieve all registered doctors:

```http
GET /doctors
```

Filter doctors by specialization:

```http
GET /doctors?specialization=cardiology
```

Specialization searches should be case-insensitive and ignore leading and trailing whitespace.

#### 3. Retrieve a doctor by ID

**Endpoint:** `GET /doctors/{doctor_id}`

Example:

```http
GET /doctors/1
```

Returns the requested doctor's details. If the doctor does not exist, the API should return `404 Not Found`.

### C. Patient Endpoints

| Method | Endpoint | Description | Expected Success |
|---|---|---|---|
| POST | `/patients` | Register a new patient | 201 Created |

#### Register a patient

**Endpoint:** `POST /patients`

Request body:

```json
{
  "name": "Ravi Kumar"
}
```

Example response:

```json
{
  "id": 1,
  "name": "Ravi Kumar"
}
```

The returned patient ID is required when booking an appointment.

This starter project does not implement patient login or identity verification.

### D. Appointment Endpoints

| Method | Endpoint | Description | Expected Success |
|---|---|---|---|
| POST | `/appointments` | Book an appointment | 201 Created |
| GET | `/appointments` | List appointments | 200 OK |
| PATCH | `/appointments/{appointment_id}/cancel` | Cancel an appointment | 200 OK |
| PATCH | `/appointments/{appointment_id}/reschedule` | Reschedule an appointment | 200 OK |
| PATCH | `/appointments/{appointment_id}/status` | Update appointment status | 200 OK |

#### 1. Book an appointment

**Endpoint:** `POST /appointments`

Request body:

```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_time": "2030-05-20T10:00:00"
}
```

Fields:

- `patient_id`: ID of an existing patient.
- `doctor_id`: ID of an existing doctor.
- `appointment_time`: Appointment date and time in ISO 8601 format.

The system automatically copies the doctor's consultation fee into the appointment and initially assigns the status `booked`.

Example response:

```json
{
  "id": 1,
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_time": "2030-05-20T10:00:00",
  "status": "booked",
  "fee": 500.0
}
```

The example date is illustrative. Use a future date relative to the time you run the application.

Expected behavior:

- Reject requests referencing nonexistent doctors or patients with `404 Not Found`.
- Reject appointments scheduled in the past.
- Prevent conflicting appointments for the same doctor.
- Treat each appointment as a 30-minute slot.
- Allow adjacent, non-overlapping appointments.

#### 2. List appointments

**Endpoint:** `GET /appointments`

Optional query parameters:

| Parameter | Type | Description |
|---|---|---|
| `patient_id` | Integer | Filters appointments by patient ID |
| `skip` | Integer | Number of records to skip |
| `limit` | Integer | Maximum number of records to return; default 20, range 1–100 |

Examples:

Retrieve all appointments:

```http
GET /appointments
```

Retrieve appointments for a particular patient:

```http
GET /appointments?patient_id=1
```

Retrieve the first ten appointments:

```http
GET /appointments?skip=0&limit=10
```

Pagination must not accidentally skip the first record when `skip=0`.

**Security note:** The `patient_id` query parameter is only a filter. It does not authenticate the caller or prove that the caller owns the requested appointments.

#### 3. Cancel an appointment

**Endpoint:** `PATCH /appointments/{appointment_id}/cancel`

Example:

```http
PATCH /appointments/1/cancel
```

No request body is required.

Expected behavior:

- Set the appointment status to `cancelled`.
- Persist the change in the database.
- Return the updated appointment.
- Return `404 Not Found` if the appointment does not exist.
- Reject cancellation if the appointment is already in a state that cannot be cancelled.

A cancelled appointment should no longer block its previously reserved time slot.

#### 4. Reschedule an appointment

**Endpoint:** `PATCH /appointments/{appointment_id}/reschedule`

Request body:

```json
{
  "appointment_time": "2030-05-20T11:00:00"
}
```

Expected behavior:

- Update the appointment time if the requested slot is available.
- Reject conflicting appointments for the same doctor with `409 Conflict`.
- Preserve the original appointment time if rescheduling fails.
- Apply the same overlap rules used when booking a new appointment.

#### 5. Update appointment status

**Endpoint:** `PATCH /appointments/{appointment_id}/status`

The current API accepts the requested status as a query parameter.

Example:

```http
PATCH /appointments/1/status?status=completed
```

The following transitions are permitted:

- `booked` → `cancelled`
- `booked` → `completed`

No transitions are permitted out of `cancelled` or `completed`.

Expected behavior:

- Reject unknown status values with `422 Unprocessable Entity`.
- Reject invalid transitions with `409 Conflict`.
- Persist valid status updates.
- Return `404 Not Found` for a nonexistent appointment.

This challenge does not implement authentication or authorization. Status validation and transition rules are the scope of this issue.

## 5. HTTP Status Codes

| Status Code | Meaning | Example |
|---|---|---|
| 200 | OK | Successful retrieval or update |
| 201 | Created | Doctor, patient, or appointment created |
| 400 | Bad Request | Invalid business operation |
| 404 | Not Found | Doctor, patient, or appointment does not exist |
| 409 | Conflict | Appointment slot is occupied or transition is invalid |
| 422 | Unprocessable Entity | Invalid input or unsupported status value |

The intentionally broken implementation may return incorrect status codes until the relevant issues are fixed.

## 6. Database Information

The project uses SQLite for local development.

- Database file: `hospital_booking.db`
- ORM: SQLAlchemy 2.x
- Models: Doctor, Patient, Appointment
- Table creation: Performed automatically when the application starts.

To reset local demo data:

1. Stop the server.
2. Delete `hospital_booking.db`.
3. Restart the application.

The application will create a fresh database and its tables.

The automated tests use a separate in-memory SQLite database, keeping test data isolated from local demo data.

## 7. Running Tests

Run the complete test suite:

```bash
pytest -q
```

Run doctor-related tests:

```bash
pytest tests/test_doctors.py -q
```

Run appointment-related tests:

```bash
pytest tests/test_appointments.py -q
```

Some tests are expected to fail initially because the starter code intentionally contains bugs.

Participants must fix the implementation rather than deleting tests or weakening assertions.

Add tests for edge cases discovered while fixing the issues.

## 8. Hack the Web — Issue and Marking Summary

The challenge contains nine issues worth a total of 200 marks.

| Issue | Topic | Marks |
|---|---|---:|
| HTW-01 | Incorrect doctor creation status code | 10 |
| HTW-02 | Missing doctor not-found handling | 10 |
| HTW-03 | Booking appointments in the past | 10 |
| HTW-04 | Negative consultation fee validation | 10 |
| HTW-05 | Appointment cancellation not persisted | 20 |
| HTW-06 | Case-sensitive specialization search | 20 |
| HTW-07 | Rescheduling conflicts | 20 |
| HTW-08 | Overlapping appointment bookings | 50 |
| HTW-09 | Invalid appointment status transitions | 50 |
| **Total** | **9 issues** | **200** |

### Difficulty distribution

- Easy: 4 issues × 10 marks = 40 marks
- Medium: 3 issues × 20 marks = 60 marks
- Hard: 2 issues × 50 marks = 100 marks

## 9. Participant Submission Requirements

1. Fix the implementation rather than deleting or weakening tests.
2. Add or update tests for every issue.
3. Test important edge cases, including invalid inputs and conflicting appointments.
4. Create a `FIXES.md` file explaining what changed and why.
5. Preserve the project folder structure.
6. Use clear Git commit messages.
7. Do not include real patient information in source code, commits, screenshots, or test output.

## 10. Scope and Security Disclaimer

This repository is a learning and debugging challenge for a student hackathon. It intentionally contains bugs and omits production-grade authentication, authorization, privacy controls, audit logging, database migrations, and deployment hardening.

It is not suitable for real clinical use. Do not store or process real patient information.
