# 🚀 HireReady AI

An AI-powered ATS Resume Analyzer that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS), improve keyword matching, and receive intelligent career recommendations using LLM-powered analysis.

## ✨ Features

### 📊 ATS Resume Scoring

* Analyze resumes against job descriptions
* Generate ATS compatibility scores (0-100)
* Detailed score breakdown:

  * Keyword Match
  * Resume Sections
  * Experience
  * Action Verbs
  * Formatting

### 🤖 AI-Powered Resume Analysis

* Resume strengths identification
* Critical gap detection
* ATS optimization suggestions
* Skills recommendation engine
* Personalized improvement tips

### 📈 Keyword Analysis

* Extract keywords from job descriptions
* Identify matched keywords
* Highlight missing keywords
* Calculate keyword match percentage

### 📝 Professional CV Generation

* Generate ATS-friendly PDF resumes
* Clean professional formatting
* Multiple resume sections supported
* Download-ready PDF output

### 🕒 Analysis History

* Store previous resume analyses
* View score history
* Track resume improvements over time

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* Groq API
* Requests

### AI & NLP

* Llama 4 Scout Model
* Keyword Extraction
* Resume Optimization Logic

### Document Processing

* ReportLab
* Python-Docx
* PyMuPDF

### Deployment

* Gunicorn
* Render
* Railway
* Heroku

---

## 📂 Project Structure

```bash
HireReady-AI/
│
├── app.py
├── cv_generator.py
├── requirements.txt
├── Procfile
├── .env
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── assets/
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/HireReady-AI.git
cd HireReady-AI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
FLASK_SECRET_KEY=your_secret_key
FLASK_DEBUG=true
PORT=5000
```

### 5. Run Application

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

## 🔌 API Endpoints

| Method | Endpoint          | Description         |
| ------ | ----------------- | ------------------- |
| GET    | /                 | Home Page           |
| POST   | /api/analyze      | ATS Resume Analysis |
| POST   | /api/ai-analysis  | AI Career Feedback  |
| GET    | /api/history      | Analysis History    |
| DELETE | /api/history/<id> | Delete History Item |

---

## 📊 ATS Scoring Criteria

| Category         | Weight |
| ---------------- | ------ |
| Keyword Matching | 40%    |
| Resume Sections  | 20%    |
| Experience       | 15%    |
| Action Verbs     | 15%    |
| Formatting       | 10%    |

Total Score: **100 Points**

---

## 🌟 Future Improvements

* Resume Upload (PDF/DOCX)
* AI Resume Rewriter
* Cover Letter Generator
* LinkedIn Profile Analyzer
* Multi-language Support
* User Authentication
* Cloud Database Integration

---

## 🎯 Use Cases

* Students applying for internships
* Fresh graduates
* Software Engineers
* Data Scientists
* Machine Learning Engineers
* Job seekers preparing ATS-friendly resumes

---
