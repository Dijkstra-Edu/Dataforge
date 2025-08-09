# 🎓 Certificate-Generator

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
```

To get a Personal Access Token:
- Go to GitHub → Settings → Developer Settings → Personal Access Tokens.
- Click Generate new token (Classic or Fine-grained).
- Give it:
  - repo scope if you want to access private repos.
  - read:org if you want org details.
- Copy the token and put it in .env.

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

### 📥 Download a Certificate

```http
POST /Dijkstra/v1/certificate/download/{userName}
```
- Generates and returns a personalized certificate for the given `{userName}`.

### 📊 Fetch GitHub Contribution Data

```http
GET /Dijkstra/v1/certificate/data/{userName}?fromDate=YYYY-MM-DD&toDate=YYYY-MM-DD
```
- Returns contribution data for the given GitHub username and optional date range.

### ❤️ Health Check

```http
GET /Dijkstra/v1/certificate/health
```
- Returns a success message to confirm the server is running.

---

## 📜 License

This project is released under the repository’s license.
