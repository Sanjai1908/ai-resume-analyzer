"""
utils/roadmap.py
------------------
Rule-based logic for:
1. Recommending suitable career paths based on detected skills.
2. Generating a simple learning roadmap for missing skills.

This is intentionally rule-based (no ML model) to keep the project simple
and explainable — a great talking point in interviews about trade-offs
between rule-based and ML-based recommendation systems.
"""

# Career path definitions: each career has a set of "core" skills.
# If a resume contains a good overlap with a career's core skills,
# we recommend that path.
CAREER_PATHS = {
    "Data Analyst": [
        "sql", "excel", "tableau", "power bi", "pandas", "statistics",
        "data visualization", "data analysis"
    ],
    "Data Scientist": [
        "python", "machine learning", "statistics", "pandas", "numpy",
        "scikit-learn", "data analysis", "nlp"
    ],
    "AI/ML Engineer": [
        "python", "machine learning", "deep learning", "tensorflow",
        "pytorch", "nlp", "scikit-learn"
    ],
    "Python Developer": [
        "python", "flask", "django", "rest api", "git", "sql", "docker"
    ],
}

# Simple learning resource suggestions per skill (used to build the roadmap)
LEARNING_RESOURCES = {
    "python": "Complete a Python fundamentals course (e.g. CS50P, freeCodeCamp).",
    "machine learning": "Take Andrew Ng's Machine Learning Specialization (Coursera).",
    "deep learning": "Study the Deep Learning Specialization or fast.ai course.",
    "sql": "Practice SQL on platforms like LeetCode, HackerRank, or Mode Analytics.",
    "tableau": "Complete Tableau Public's free training videos and build 2-3 dashboards.",
    "power bi": "Follow Microsoft's free Power BI learning path on MS Learn.",
    "pandas": "Work through the official Pandas 'Getting Started' tutorials.",
    "numpy": "Practice NumPy basics via the official NumPy quickstart guide.",
    "scikit-learn": "Build 2-3 small ML projects using scikit-learn's official examples.",
    "tensorflow": "Complete TensorFlow's 'Basics' tutorials on tensorflow.org.",
    "pytorch": "Go through PyTorch's official 60-minute beginner tutorial.",
    "nlp": "Take a short NLP course (e.g. spaCy 101 course, Hugging Face NLP course).",
    "flask": "Build a small REST API project using Flask's official quickstart.",
    "django": "Follow the official Django tutorial and build a small CRUD app.",
    "git": "Practice Git basics with 'Learn Git Branching' (interactive site).",
    "docker": "Complete Docker's official 'Get Started' tutorial.",
    "statistics": "Review core stats concepts via Khan Academy's Statistics course.",
    "data visualization": "Practice with Matplotlib/Seaborn on real datasets (Kaggle).",
    "rest api": "Learn REST principles and build/test APIs using Postman + Flask.",
    "mongodb": "Complete MongoDB University's free M001 course.",
    "mysql": "Practice MySQL using W3Schools SQL exercises or SQLZoo.",
}


def recommend_careers(skills: list, top_n: int = 2) -> list:
    """
    Suggests the most suitable career path(s) based on how many of a
    career's core skills appear in the candidate's extracted skills.

    Returns
    -------
    list[tuple(career_name, match_count, total_required)]
        sorted by best match first
    """
    skill_set = set(skills)
    scored_careers = []

    for career, required_skills in CAREER_PATHS.items():
        required_set = set(required_skills)
        overlap = skill_set.intersection(required_set)
        if overlap:  # only consider careers with at least one matching skill
            scored_careers.append((career, len(overlap), len(required_set)))

    # Sort by number of matched skills (descending)
    scored_careers.sort(key=lambda x: x[1], reverse=True)
    return scored_careers[:top_n] if scored_careers else [("General Tech Role", 0, 0)]


def generate_roadmap(missing_skills: list) -> dict:
    """
    Builds a simple learning roadmap: for each missing skill, suggest a
    concrete next step / resource. Falls back to a generic message for
    skills not in our resource dictionary.

    Returns
    -------
    dict {skill: recommendation_text}
    """
    roadmap = {}
    for skill in missing_skills:
        roadmap[skill] = LEARNING_RESOURCES.get(
            skill,
            f"Learn the fundamentals of '{skill}' through official docs or a beginner course."
        )
    return roadmap
