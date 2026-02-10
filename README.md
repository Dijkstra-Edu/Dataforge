# 🎓 Dijkstra Main Server

**Certificate-Generator** is a FastAPI-powered backend application that generates personalized certificates based on user data. It includes API endpoints to retrieve GitHub data and download certificates — perfect for automating certificates in bulk for events, competitions, etc.

---

## 💻 Getting Started

To run this project locally, ensure you have **Python 3.10+** installed.

Clone the repository and navigate into the project folder:

```bash
git clone https://github.com/your-username/Certificate-Generator.git
cd Certificate-Generator
```

Create and activate a virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate        # On Windows
# OR
source venv/bin/activate       # On macOS/Linux
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Next add a `.env` file in the project root (outside of `app`). Inside it, add at least the following env variables:

```
GITHUB_TOKEN=<GitHub Personal Access Token (Classic)>
POSTGRES_URL=<Enter your application PostgreSQL connection string>
POSTGRES_URL_MIGRATIONS=<Enter your migrations PostgreSQL connection string (optional, usually more privileged)>
ENV=DEV
```

To get a Personal Access Token:
- Go to GitHub → Settings → Developer Settings → Personal Access Tokens.
- Click Generate new token (Classic or Fine-grained).
- Give it:
  - repo scope if you want to access private repos.
  - read:org if you want org details.
- Copy the token and put it in .env.

To get a PostgreSQL Server Connection String:
- Create an account on [Supabase](http://supabase.com/) to use a hosted PostgreSQL server or set up a local server on your PC by downloading the [PostgreSQL client](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- For Supabase, you can use:
  - `POSTGRES_URL` for the **application user** (read/write on data, minimal schema permissions)
  - `POSTGRES_URL_MIGRATIONS` for the **migrations user** (can create/alter tables, enums, etc.)
- Upload the schema present in the `Schema` folder (the latest one) to bootstrap a fresh database if you are not using Alembic migrations yet, or let Alembic create it using the steps below.

After this, Navigate to the app folder
```
cd app
```

Then, start the FastAPI server:

```bash
uvicorn main:app --reload
```

You should see:

```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 🧱 Database Migrations with Alembic

This project uses **Alembic** for database schema migrations on top of `SQLModel` and PostgreSQL (Supabase).

### Environment variables

- `POSTGRES_URL`  
  Used by the FastAPI application in `app/db.py` to create the main SQLModel engine.

- `POSTGRES_URL_MIGRATIONS` (optional but recommended)  
  Used by Alembic (in CI/CD or when running migrations manually) to connect with a more privileged database user that can create and alter schemas, tables, and enums.

You can either:
- Set only `POSTGRES_URL` and point it to a user that has both app and migration privileges, **or**
- Use **separate users**:
  - app user → `POSTGRES_URL`
  - migrations user → `POSTGRES_URL_MIGRATIONS`

### Running migrations in development (locally)

1. Ensure your virtual environment is active and dependencies are installed:

```bash
python -m venv venv
.\venv\Scripts\activate        # Windows
# or
source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
```

2. Navigate into the `app` directory:

```bash
cd app
```

If you have no need to change the schema, go to step 5.

3. Create a new migration after changing models in `Schema/SQL/Models/models.py`:

```bash
alembic revision --autogenerate -m "Describe your change"
```

4. Review the generated migration in `app/migrations/versions/` (ensure it does what you expect).

5. Apply the migration to your local database:

```bash
alembic upgrade head
```

After this, the schema will match your current models, and you can run the app with:

### First-time migration on existing QA/Prod databases

If QA or production **already have a database** (with or without tables) but **no Alembic history** (no `alembic_version` table or it’s empty), the workflow would run the baseline and fail with “table already exists”. Do a **one-time stamp** so Alembic knows the current revision, then all future pushes will only run `alembic upgrade head`.

From your machine, point your env at the target DB (e.g. use `.env.qa` or `.env.prod`), then:

```bash
cd app
# POSTGRES_URL_MIGRATIONS (or DATABASE_URL) must point at the QA or prod DB
alembic stamp head
```

If the DB only has the baseline schema (no Mig 1), use `alembic stamp 58d213ac2cce` instead. After that, push to `qa` or `main`; the workflow will run `alembic upgrade head` on every push.

**Workflows**

- **CI** (`.github/workflows/ci.yml`): runs on every push/PR; uses a fresh Postgres service and runs `alembic upgrade head` to verify migrations apply.
- **QA** (`.github/workflows/migrate-qa.yml`): runs on push to `qa`; applies migrations using `POSTGRES_URL_MIGRATIONS`.
- **Prod** (`.github/workflows/migrate-prod.yml`): runs on push to `main`; applies migrations using `POSTGRES_URL_MIGRATIONS`.

```bash
uvicorn main:app --reload
```

---

## 🧪 Using the API

Once the server is running, you can access:

- **API Root:** `http://127.0.0.1:8000`
- **Interactive Docs (Swagger UI):**  
  👉 `http://127.0.0.1:8000/docs`


### Naming Convention

The Naming Convention is specified by the PEP8 Standard.

| Entity                 | Convention                    | Example                         |
| ---------------------- | ----------------------------- | ------------------------------- |
| **Variables**          | `snake_case`                  | `user_id`, `total_count`        |
| **Functions/Methods**  | `snake_case`                  | `get_user()`, `send_email()`    |
| **Classes**            | `PascalCase`                  | `UserService`, `AuthController` |
| **Exceptions**         | `PascalCase` + `Error` suffix | `ValidationError`               |
| **Constants**          | `ALL_CAPS_WITH_UNDERSCORES`   | `MAX_RETRIES`, `DEFAULT_PORT`   |
| **Modules (files)**    | `snake_case.py`               | `user_service.py`               |
| **Packages (folders)** | `snake_case/`                 | `services/`, `models/`          |
| **Private/Internal**   | `_single_leading_underscore`  | `_cache`, `_helper_function()`  |
| **Magic methods**      | `__double_underscores__`      | `__init__`, `__str__`           |



---

## 📜 License

This project is released under the repository’s license.
