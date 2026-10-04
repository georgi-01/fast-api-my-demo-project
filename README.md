<div align="center">

# FastAPI My Demo Project

<p>
  <strong>Учебен FastAPI backend проект с PostgreSQL, SQLAlchemy, Alembic и pytest</strong>
</p>

<p>
  <em>Без Docker — локална Python + PostgreSQL среда</em>
</p>

</div>

---

## 📌 За проекта

Този проект е учебен FastAPI backend, изграден стъпка по стъпка с цел практическо упражнение на:

- FastAPI
- Pydantic
- SQLAlchemy 2.x
- PostgreSQL
- asyncpg
- Alembic
- pytest
- repository pattern
- service layer
- API routers
- database seeding
- автоматично генериране на OpenAPI документация

Проектът използва **асинхронен SQLAlchemy** и PostgreSQL.

> **Важно:** Проектът в момента не използва Docker. Всички услуги се стартират локално.

---

## 🧱 Архитектура

```text
Client
   │
   ▼
FastAPI Router
   │
   ▼
Pydantic Schema
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
SQLAlchemy ORM
   │
   ▼
PostgreSQL
```

За миграциите:

```text
SQLAlchemy Models
       │
       ▼
     Alembic
       │
       ▼
PostgreSQL Schema
```

За начални данни:

```text
Seeder
   │
   ├── Person
   ├── Teacher
   ├── Student
   ├── Course
   ├── Enrollment
   └── Exam
```

---

## 📂 Project Structure

```text
fast_api_my_demo_project/
│
├── .venv/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │
│   ├── schemas/
│   │
│   ├── models/
│   │   ├── person.py
│   │   ├── teacher.py
│   │   ├── student.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   └── exam.py
│   │
│   ├── services/
│   │
│   ├── repositories/
│   │
│   └── database/
│       ├── database.py
│       ├── base.py
│       ├── dependencies.py
│       └── seed.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── conftest.py
│   ├── database.py
│   └── ...
│
├── alembic.ini
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🚀 Getting Started

## 1. Clone repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd fast_api_my_demo_project
```

---

## 2. Създай виртуална среда

Linux / macOS:

```bash
python3 -m venv .venv
```

Активирай:

```bash
source .venv/bin/activate
```

При активна среда терминалът трябва да показва:

```text
(.venv)
```

---

## 3. Инсталирай dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

# 🐘 PostgreSQL

Проектът използва две отделни бази:

```text
fastapi_demo_db
fastapi_demo_test_db
```

## Development database

```text
fastapi_demo_db
```

Тази база се използва при нормална работа на приложението и от seeder-а.

## Test database

```text
fastapi_demo_test_db
```

Тази база се използва от pytest.

> ⚠️ Не използвай development database за тестовете. Тестовете почистват test database след всеки тест.

---

## Създаване на базите

Ако PostgreSQL е инсталиран локално:

```bash
sudo -u postgres psql
```

В `psql`:

```sql
CREATE DATABASE fastapi_demo_db;
CREATE DATABASE fastapi_demo_test_db;
```

Изход:

```sql
\q
```

---

# 🔐 Database configuration

Преди да стартираш проекта, настрой PostgreSQL connection string-а в:

```text
app/database/database.py
```

и test connection string-а в:

```text
tests/database.py
```

Пример:

```text
postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/fastapi_demo_db
```

За test database:

```text
postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/fastapi_demo_test_db
```

> 🔒 **Не commit-вай реалната си PostgreSQL парола в GitHub.**
>
> За публичен repository е препоръчително connection string-ите да бъдат преместени в environment variables / `.env` файл, а `.env` да бъде добавен към `.gitignore`.

---

# 🗃️ Database migrations

Проектът използва Alembic.

## Проверка на текущата migration версия

```bash
alembic current
```

## Прилагане на всички migrations

За development database:

```bash
DATABASE_URL="postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/fastapi_demo_db" alembic upgrade head
```

За test database:

```bash
DATABASE_URL="postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/fastapi_demo_test_db" alembic upgrade head
```

## Проверка на migration history

```bash
alembic history
```

---

# 🌱 Database Seeder

Seeder-ът създава примерни данни за development database.

Стартиране:

```bash
python -m app.database.seed
```

При първото успешно изпълнение:

```text
Database seeding completed.
```

При следващо изпълнение:

```text
Database already seeded.
```

Seeder-ът е **idempotent** — повторното му стартиране не създава дублирани записи.

---

## 📊 Seeded data

Текущият seeder създава:

| Table        | Records |
|--------------|---------|
| `person`     | 8       |
| `teacher`    | 3       |
| `student`    | 5       |
| `course`     | 3       |
| `enrollment` | 7       |
| `exam`       | 3       |

Може да провериш данните директно през PostgreSQL:

```bash
sudo -u postgres psql -d fastapi_demo_db
```

След това:

```sql
SELECT
    (SELECT COUNT(*) FROM person) AS persons,
    (SELECT COUNT(*) FROM teacher) AS teachers,
    (SELECT COUNT(*) FROM student) AS students,
    (SELECT COUNT(*) FROM course) AS courses,
    (SELECT COUNT(*) FROM enrollment) AS enrollments,
    (SELECT COUNT(*) FROM exam) AS exams;
```

Очакван резултат:

```text
 persons | teachers | students | courses | enrollments | exams
---------+----------+----------+---------+-------------+-------
    8    |    3     |    5     |    3    |      7      |  3
```

---

# 🧪 Testing

Тестовете използват отделна PostgreSQL database:

```text
fastapi_demo_test_db
```

Стартирай всички тестове:

```bash
pytest -v
```

Очакваният резултат за текущия repository layer е:

```text
6 passed
```

## Защо има отделна test database?

Тестовете извършват реални database операции.

След всеки тест test fixture-ът почиства таблиците:

```text
enrollment
exam
course
student
teacher
person
```

Това позволява тестовете да се изпълняват многократно, без да се натрупват тестови записи.

---

# ▶️ Стартиране на FastAPI

От root директорията на проекта:

```bash
python -m uvicorn app.main:app --reload
```

При успешно стартиране ще видиш адрес подобен на:

```text
http://127.0.0.1:8000
```

---

# 📖 API Documentation

FastAPI автоматично генерира OpenAPI документация.

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

## OpenAPI JSON

```text
http://127.0.0.1:8000/openapi.json
```

Swagger UI е особено удобен за development, защото позволява директно изпълнение на API requests.

---

# 🔄 Typical Development Workflow

Препоръчителният workflow е:

```text
1. Activate .venv
        ↓
2. Start / check PostgreSQL
        ↓
3. Run Alembic migrations
        ↓
4. Run pytest
        ↓
5. Run database seeder
        ↓
6. Start FastAPI
        ↓
7. Test API through /docs
```

Командите:

```bash
source .venv/bin/activate
```

```bash
alembic upgrade head
```

```bash
python -m app.database.seed
```

```bash
pytest -v
```

```bash
python -m uvicorn app.main:app --reload
```

---

# 🛠️ Useful Commands

## Проверка на Python

```bash
python --version
```

## Проверка на pip

```bash
python -m pip --version
```

## Инсталиране на нов package

```bash
python -m pip install PACKAGE_NAME
```

След това обнови:

```bash
python -m pip freeze > requirements.txt
```

## Инсталиране от requirements

```bash
python -m pip install -r requirements.txt
```

---

# 🌿 Git / GitHub

Преди първия commit провери:

```bash
git status
```

Добави файловете:

```bash
git add .
```

Направи commit:

```bash
git commit -m "Initial FastAPI project"
```

Свържи repository-то:

```bash
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
```

И качи:

```bash
git push -u origin main
```

---

# 🔒 Important before publishing to GitHub

Преди repository-то да стане публично, провери за:

- PostgreSQL passwords
- API keys
- tokens
- secret keys
- `.env` files
- локални credentials

Провери например:

```bash
git status
```

и:

```bash
git ls-files
```

`.venv/` **не трябва** да бъде commit-ван.

`.env` също **не трябва** да бъде commit-ван.

---

# 🧭 Current project status

| Component        | Status             |
|------------------|--------------------|
| FastAPI          | ✅                 |
| PostgreSQL       | ✅                 |
| SQLAlchemy 2.x   | ✅                 |
| asyncpg          | ✅                 |
| Alembic          | ✅                 |
| Models           | ✅                 |
| Repositories     | ✅                 |
| Repository tests | ✅                 |
| Test database    | ✅                 |
| Database seeder  | ✅                 |
| Seed data        | ✅                 |
| API routers      | 🚧 In progress     |
| Services         | 🚧 In progress     |
| Pydantic schemas | 🚧 In progress     |
| Full API CRUD    | 🚧 In progress     |
| Docker           | ⏸️ Not planned yet |

---

<div align="center">

### 📚 Learning Project

Built step by step while learning backend development with Python, FastAPI and PostgreSQL.

</div>
