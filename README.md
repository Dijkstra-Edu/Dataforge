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

Next add a .env folder in the root folder (outside of app). Inside of the app, add the following env variables:

```
GITHUB_TOKEN=<GitHub Personal Access Token (Classic)>
POSTGRES_URL=<Enter your personal PsotgreSQL Server Connection String>
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
- Create an account on [Supabase](http://supabase.com/) to use a hosted PostgreSQL server or setup a local server on your PC by donwloading the [PostgreSQL client](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- Upload the Schema present in the Schema folder (The latest one) for your server
- Add the test data that is available for local testing

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
