# 🧠 AI Resume Analyzer & Job Matcher

A portfolio-ready mini project that analyzes a resume (PDF) against a job
description and produces a **Job Match Score**, **skill gap analysis**,
**career path recommendations**, and a **personalized learning roadmap** —
all powered by NLP and Machine Learning techniques.

Built to demonstrate practical, end-to-end NLP/ML problem-solving skills
for **Data Analyst**, **Data Science**, **AI/ML Engineer**, and
**Python Developer** roles.

---

## ✨ Features

- 📄 Upload a PDF resume — text is extracted using **pdfplumber**
- 🛠️ Automatic technical skill extraction (20+ skill keyword/phrase database)
- 📋 Paste any Job Description for comparison
- 📊 **TF-IDF Vectorization + Cosine Similarity** for a 0–100% Job Match Score
- ✅ Matched skills vs ❌ Missing skills breakdown
- 💼 Rule-based career path recommendations (Data Analyst, Data Scientist,
  AI/ML Engineer, Python Developer)
- 📚 Auto-generated learning roadmap for missing skills
- 🎨 Clean, card-based Streamlit dashboard with sidebar navigation and
  progress bars

---

## 🧰 Tech Stack

| Category        | Tools |
|-----------------|-------|
| Language        | Python |
| UI Framework    | Streamlit |
| NLP             | spaCy |
| ML / Matching   | scikit-learn (TF-IDF, Cosine Similarity) |
| PDF Parsing     | pdfplumber |
| Data Handling   | pandas |

---

## 📁 Project Structure

```
project/
│
├── app.py                     # Main Streamlit app (dashboard UI + logic flow)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── assets/                    # (Optional) images/screenshots for README
│
├── data/
│   ├── __init__.py
│   ├── skills_db.py            # Predefined skills database (20+ skills)
│   ├── sample_resume.txt       # Sample resume text for testing
│   └── sample_job_description.txt  # Sample JD text for testing
│
├── utils/
│   ├── __init__.py
│   ├── pdf_parser.py           # Extracts text from PDF resumes
│   ├── skill_extractor.py      # Matches text against skills database
│   ├── matcher.py              # TF-IDF + Cosine Similarity matching logic
│   └── roadmap.py              # Career recommendations + learning roadmap
│
└── models/                     # (Reserved for future ML model artifacts)
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the spaCy English model
```bash
python -m spacy download en_core_web_sm
```

### 5. Run the app
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🧪 Testing with Sample Data

This repo includes sample data under `data/`:
- `sample_resume.txt` — convert to PDF (e.g. via Word/Google Docs "Export as PDF",
  or any free text-to-PDF tool) and upload it in the app.
- `sample_job_description.txt` — copy-paste its contents into the Job
  Description box.

Expected behavior: the app should report a moderate-to-high match score,
list overlapping skills (e.g. Python, SQL, Pandas, Machine Learning), and
flag missing skills (e.g. TensorFlow, Tableau, Docker) with a learning
roadmap for each.

---

## 🧠 How It Works

1. **PDF Text Extraction** — `pdfplumber` reads each page of the uploaded
   resume and concatenates the text.
2. **Skill Extraction** — Resume and JD text are scanned against a
   predefined skills database (`data/skills_db.py`) using word-boundary
   regex matching to avoid false positives.
3. **Resume–JD Matching** — Both texts are converted into **TF-IDF**
   vectors, and **Cosine Similarity** between them produces a 0–100% match
   score.
4. **Skill Gap Analysis** — Set operations (intersection/difference)
   between resume skills and JD skills produce matched vs missing skills.
5. **Career Recommendation** — A rule-based scoring system checks how many
   of each career path's "core skills" are present in the resume.
6. **Learning Roadmap** — Each missing skill is mapped to a concrete,
   beginner-friendly learning resource/suggestion.

---

## 🚀 Possible Future Enhancements

- Replace rule-based career recommendation with a trained classifier
- Add support for `.docx` resumes
- Use sentence-transformers/embeddings for more accurate semantic matching
- Add a database to track multiple resume/JD comparisons over time
- Deploy on Streamlit Community Cloud for a live demo link

---

## 📜 License

This project is open-source and free to use for learning and portfolio purposes.
