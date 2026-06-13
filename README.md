# ✨ HireReady AI 

Smart ATS Resume Analyzer & Optimizer, converted from a single HTML file to a proper **Flask** web app.

---

## 🗂 Project Structure

```
hireready/
├── app.py              # Flask backend — scoring logic + Groq API routes
├── templates/
│   └── index.html      # Frontend (same design as original)
├── requirements.txt
├── Procfile            # For Render / Railway / Heroku
├── .env.example
└── README.md
```

---

## ⚡ Local Setup

```bash
# 1. Clone / unzip the project
cd hireready

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 5. Run
python app.py
```

Open http://localhost:5000

---

## 🔑 Environment Variables

| Variable          | Required | Description                                      |
|-------------------|----------|--------------------------------------------------|
| `GROQ_API_KEY`    | ✅       | Your Groq API key (https://console.groq.com)     |
| `FLASK_SECRET_KEY`| ✅       | Random string for session encryption             |
| `FLASK_DEBUG`     | ❌       | `true` for dev, `false` for prod (default)       |
| `PORT`            | ❌       | Port to listen on (default: 5000)                |

---

## 🚀 Deploy to Render (Free)

1. Push to a GitHub repo
2. Go to https://render.com → **New Web Service**
3. Connect your repo
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `gunicorn app:app`
6. Add environment variables in the Render dashboard
7. Deploy!

---

## 🔄 What Changed vs the HTML Version

| Feature              | Original (HTML)           | Python Edition              |
|----------------------|---------------------------|-----------------------------|
| Hosting              | Netlify + build.js        | Any Python host (Render etc)|
| API key security     | Build-time injection      | Server-side env vars ✅     |
| Firebase auth        | Google Auth + Firestore   | Removed (session-based) *   |
| History storage      | Firestore + localStorage  | Flask sessions (last 10)    |
| Scoring logic        | Client-side JS            | Server-side Python          |
| Groq AI calls        | Browser fetch             | Server-side requests        |
| PDF/DOCX extraction  | pdf.js + mammoth (browser)| pdf.js + mammoth (browser)  |
| PDF export           | html2pdf.js (browser)     | html2pdf.js (browser)       |

*Firebase auth can be re-added if needed — the backend is straightforward to extend.

---

## 📡 API Endpoints

| Method | Path                   | Description                  |
|--------|------------------------|------------------------------|
| GET    | `/`                    | Main app                     |
| POST   | `/api/analyze`         | Score resume vs job desc     |
| POST   | `/api/ai-analysis`     | Groq AI career coach         |
| POST   | `/api/improve-resume`  | Groq AI resume rewriter      |
| GET    | `/api/history`         | Session history (last 10)    |
| DELETE | `/api/history/<id>`    | Delete a history entry       |
