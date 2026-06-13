# 🚀 HireReady AI

An AI-powered ATS Resume Analyzer that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS), improve keyword matching, and receive intelligent AI-driven recommendations tailored to specific job descriptions.

---

## ✨ Features

### 📊 ATS Resume Scoring

* Analyze resumes against job descriptions
* Generate ATS compatibility scores (0–100)
* Detailed scoring breakdown:

  * Keyword Matching
  * Resume Sections
  * Experience
  * Action Verbs
  * Formatting

### 📄 Resume Upload & Parsing

* Upload PDF resumes
* Upload DOCX resumes
* Automatic text extraction
* Resume content processing for ATS evaluation

### 🤖 AI-Powered Resume Analysis

* Identify resume strengths
* Detect critical skill and keyword gaps
* Provide ATS optimization suggestions
* Recommend missing skills from job descriptions
* Deliver personalized improvement tips

### 📈 Keyword Analysis

* Extract keywords from job descriptions
* Identify matched keywords
* Highlight missing keywords
* Calculate keyword match percentage

### 🕒 Analysis History

* Store recent resume analyses
* Review previous ATS scores
* Track improvements over time

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* Requests

### AI Integration

* Groq API
* Llama 4 Scout Model

### Document Processing

* PyMuPDF
* Python-Docx

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

**Linux / macOS**

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
| POST   | /api/ai-analysis  | AI Resume Feedback  |
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

**Total Score: 100 Points**

---

## 🎯 Use Cases

* Students applying for internships
* Fresh graduates
* Software Engineers
* Data Scientists
* Machine Learning Engineers
* Career switchers
* Job seekers preparing ATS-friendly resumes

---

## 🌟 Future Improvements

* AI Resume Rewriter
* Cover Letter Generator
* LinkedIn Profile Analyzer
* User Authentication
* Cloud Database Integration
* Advanced ATS Analytics
