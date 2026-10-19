"""
utils/matcher.py
------------------
Core matching logic: compares resume text against a job description using
TF-IDF Vectorization + Cosine Similarity to produce a Job Match Score.

Also computes matched vs missing skills by comparing extracted skill sets.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(resume_text: str, jd_text: str) -> float:
    """
    Calculates similarity between resume and job description text.

    Steps:
    1. Convert both texts into TF-IDF vectors (captures importance of
       words relative to both documents).
    2. Compute cosine similarity between the two vectors (measures how
       similar their direction is in vector space, range 0-1).
    3. Scale to a 0-100 percentage score.

    Returns
    -------
    float : match score rounded to 2 decimal places (0-100)
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    documents = [resume_text, jd_text]

    # TF-IDF Vectorizer converts text into numerical feature vectors,
    # weighting words by how unique/important they are across documents.
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Cosine similarity between the resume vector (row 0) and JD vector (row 1)
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    similarity_score = similarity_matrix[0][0]

    match_percentage = round(similarity_score * 100, 2)
    return match_percentage


def get_matched_and_missing_skills(resume_skills: list, jd_skills: list) -> tuple:
    """
    Compares skill sets extracted from resume and job description.

    Returns
    -------
    tuple(matched_skills: list, missing_skills: list)
        matched_skills  -> skills present in BOTH resume and JD
        missing_skills  -> skills required by JD but absent from resume
    """
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched_skills = sorted(resume_set.intersection(jd_set))
    missing_skills = sorted(jd_set.difference(resume_set))

    return matched_skills, missing_skills
