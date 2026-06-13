from dotenv import load_dotenv
load_dotenv()
import os
import re
import json
import uuid
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "hireready-dev-secret-change-in-prod")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# ==================== KEYWORD EXTRACTION ====================
COMMON_TECH = [
    'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue', 'node.js',
    'express', 'django', 'flask', 'spring', 'mongodb', 'mysql', 'postgresql', 'redis',
    'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
    'machine learning', 'deep learning', 'nlp', 'natural language processing', 'computer vision',
    'sql', 'nosql', 'git', 'github', 'gitlab', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
    'api', 'rest', 'restful', 'graphql', 'firebase', 'html', 'css', 'sass', 'less',
    'agile', 'scrum', 'kanban', 'jira', 'confluence', 'ci/cd', 'jenkins', 'terraform',
    'linux', 'unix', 'bash', 'shell', 'data structures', 'algorithms', 'oop',
    'object-oriented', 'microservices', 'serverless', 'lambda', 'ec2', 's3',
    'communication', 'teamwork', 'leadership', 'problem-solving', 'analytical'
]

ACTION_VERBS = [
    'developed', 'built', 'created', 'led', 'managed', 'implemented', 'designed',
    'optimized', 'improved', 'increased', 'reduced', 'achieved', 'launched',
    'collaborated', 'engineered', 'automated', 'deployed', 'integrated', 'architected'
]


def extract_keywords_from_jd(jd):
    jd_lower = jd.lower()
    return [kw for kw in COMMON_TECH if kw in jd_lower]


def analyze_resume_sections(text):
    lower = text.lower()
    return {
        'contact':       bool(re.search(r'@', lower) and (re.search(r'phone|\+|\d{10}', lower))),
        'summary':       any(k in lower for k in ['summary', 'objective', 'profile']),
        'experience':    any(k in lower for k in ['experience', 'employment', 'work']),
        'education':     any(k in lower for k in ['education', 'university', 'college', 'degree']),
        'skills':        any(k in lower for k in ['skills', 'technologies', 'competencies']),
        'projects':      any(k in lower for k in ['project', 'portfolio']),
        'certifications': any(k in lower for k in ['certification', 'certificate']),
    }


def calculate_enhanced_score(text, jd):
    jd_keywords = extract_keywords_from_jd(jd)
    resume_lower = text.lower()

    # Keyword matching (40 pts)
    matched, missing = [], []
    for kw in jd_keywords:
        (matched if kw in resume_lower else missing).append(kw)
    keyword_score = min(40, round((len(matched) / len(jd_keywords)) * 40)) if jd_keywords else 0

    # Section completeness (20 pts)
    sections = analyze_resume_sections(text)
    section_score = round((sum(sections.values()) / 7) * 20)

    # Experience relevance (15 pts)
    year_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', resume_lower, re.IGNORECASE)
    years = int(year_match.group(1)) if year_match else 0
    if years >= 5:          experience_score = 15
    elif years >= 3:        experience_score = 12
    elif years >= 1:        experience_score = 8
    elif any(k in resume_lower for k in ['experience', 'intern']): experience_score = 5
    else:                   experience_score = 0

    # Action verbs (15 pts)
    verb_count = sum(1 for v in ACTION_VERBS if v in resume_lower)
    verb_score = min(15, round((verb_count / len(ACTION_VERBS)) * 15))

    # Formatting (10 pts)
    format_score = 0
    if len(text) > 500: format_score += 3
    if any(c in resume_lower for c in ['•', '-', '*']): format_score += 2
    if 'education' in resume_lower and 'experience' in resume_lower: format_score += 3
    if len(text.split('\n')) > 10: format_score += 2
    format_score = min(10, format_score)

    total = min(100, keyword_score + section_score + experience_score + verb_score + format_score)

    kw_percent = round((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0

    return {
        'total': total,
        'breakdown': {
            'keywords': keyword_score,
            'sections': section_score,
            'experience': experience_score,
            'actionVerbs': verb_score,
            'formatting': format_score,
        },
        'matchedKeywords': matched,
        'missingKeywords': missing[:15],
        'keywordMatchPercent': kw_percent,
        'totalKeywords': len(jd_keywords),
        'yearsExperience': years,
        'sections': sections,
    }


# ==================== ROUTES ====================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    resume_text = data.get('resumeText', '').strip()
    job_desc = data.get('jobDesc', '').strip()

    if len(resume_text) < 50:
        return jsonify({'error': 'Resume text is too short.'}), 400
    if len(job_desc) < 20:
        return jsonify({'error': 'Job description is too short.'}), 400

    score_data = calculate_enhanced_score(resume_text, job_desc)

    # Persist in session history (last 10)
    history = session.get('history', [])
    history.insert(0, {
        'id': str(uuid.uuid4()),
        'score': score_data['total'],
        'breakdown': score_data['breakdown'],
        'matchedKeywords': score_data['matchedKeywords'],
        'missingKeywords': score_data['missingKeywords'],
        'keywordMatchPercent': score_data['keywordMatchPercent'],
        'date': datetime.utcnow().isoformat(),
        'fileName': data.get('fileName', 'Resume'),
    })
    session['history'] = history[:10]

    return jsonify(score_data)


@app.route('/api/ai-analysis', methods=['POST'])
def ai_analysis():
    if not GROQ_API_KEY:
        return jsonify({'error': 'GROQ_API_KEY not configured.'}), 500

    data = request.get_json()
    resume_text = data.get('resumeText', '')[:2500]
    job_desc = data.get('jobDesc', '')[:1500]
    score_data = data.get('scoreData', {})
    bd = score_data.get('breakdown', {})

    system_prompt = """You are an expert ATS career coach and resume strategist. Analyze the resume against the job description.

Provide a structured analysis following this exact format:

SECTION 1: STRENGTHS (3 points)
List 3 specific strengths aligned with the job.

SECTION 2: CRITICAL GAPS (3 points)
Identify 3 important gaps in skills, keywords, or experience.

SECTION 3: ATS OPTIMIZATION (3 tips)
Give 3 actionable tips to improve the ATS score.

SECTION 4: SKILLS TO ADD
List specific skills from the JD that should be added.

Keep the total response under 350 words. Be specific and actionable."""

    user_msg = (
        f"RESUME:\n{resume_text}\n\n"
        f"JOB DESCRIPTION:\n{job_desc}\n\n"
        f"ATS SCORE: {score_data.get('total')}/100\n"
        f"BREAKDOWN: Keywords {bd.get('keywords')}/40, Sections {bd.get('sections')}/20, "
        f"Experience {bd.get('experience')}/15, Action Verbs {bd.get('actionVerbs')}/15, "
        f"Formatting {bd.get('formatting')}/10\n"
        f"MATCHED KEYWORDS: {', '.join(score_data.get('matchedKeywords', []))}\n"
        f"MISSING KEYWORDS: {', '.join(score_data.get('missingKeywords', []))}"
    )

    try:
        resp = requests.post(
            GROQ_API_URL,
            headers={'Authorization': f'Bearer {GROQ_API_KEY}', 'Content-Type': 'application/json'},
            json={'model': GROQ_MODEL, 'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_msg}
            ], 'temperature': 0.7, 'max_tokens': 600},
            timeout=30
        )
        resp.raise_for_status()
        text = resp.json()['choices'][0]['message']['content']
        # Clean markdown formatting
        text = re.sub(r'\*\*|__|\*|#{1,6}\s', '', text)
        text = re.sub(r'SECTION \d: (.*?)(?:\n|$)', r'<h4 class="ai-section-title">\1</h4>', text)
        text = text.replace('• ', '<br>• ').replace('\n\n', '<br><br>')
        return jsonify({'analysis': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(session.get('history', []))


@app.route('/api/history/<item_id>', methods=['DELETE'])
def delete_history(item_id):
    history = session.get('history', [])
    session['history'] = [h for h in history if h.get('id') != item_id]
    return jsonify({'ok': True})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true', port=port, host='0.0.0.0')
