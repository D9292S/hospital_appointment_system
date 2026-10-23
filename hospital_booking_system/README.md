# Hospital Appointment Booking API — Hack the Web

A beginner-friendly FastAPI debugging challenge for second-year students.

## Stack
- Python 3.10+
- FastAPI
- SQLAlchemy 2.x
- SQLite
- Pydantic
- Pytest

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger UI at http://127.0.0.1:8000/docs.

## Run tests

```bash
pytest -q
```

Some tests are expected to fail at the beginning because this repository intentionally contains bugs. Read `issues/ISSUES.md`, reproduce each issue, fix the implementation, and run the tests again.

## Project structure

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

## Important
This is a learning/demo project, not a production healthcare system. It intentionally omits production-grade authentication, privacy controls, audit logging, and deployment hardening. Do not use real patient information.
