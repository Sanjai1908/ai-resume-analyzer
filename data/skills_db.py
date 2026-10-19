"""
data/skills_db.py
------------------
A predefined database of common technical & professional skills used for skill extraction.
Organized into 6 distinct Skill Spheres to enable domain-by-domain skill comparison.
"""

SKILLS_DB = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "c", "javascript", "typescript",
        "sql", "r", "go", "rust", "php", "ruby", "swift", "kotlin", "scala",
        "html", "css", "bash", "shell"
    ],
    "AI, ML & Data Science": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "pandas", "numpy", "scikit-learn", "tensorflow",
        "pytorch", "keras", "data analysis", "statistics", "data science",
        "neural networks", "generative ai", "llms", "spacy", "huggingface", "transformers"
    ],
    "Frameworks & Developer Tools": [
        "streamlit", "flask", "django", "fastapi", "react", "next.js",
        "vue", "angular", "node.js", "express", "rest api", "graphql",
        "git", "github", "gitlab", "jira", "postman"
    ],
    "Databases & Cloud Infrastructure": [
        "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle",
        "snowflake", "aws", "azure", "gcp", "docker", "kubernetes",
        "ci/cd", "terraform", "linux", "spark", "hadoop", "kafka"
    ],
    "Visualization & Analytics": [
        "tableau", "power bi", "matplotlib", "seaborn", "plotly",
        "excel", "advanced excel", "google analytics", "looker"
    ],
    "Soft Skills & Professional Competencies": [
        "communication", "leadership", "problem solving", "teamwork",
        "collaboration", "time management", "critical thinking",
        "project management", "agile", "scrum", "analytical skills"
    ]
}

# Flatten into a single list for easy lookup during extraction
ALL_SKILLS = [skill for category in SKILLS_DB.values() for skill in category]
