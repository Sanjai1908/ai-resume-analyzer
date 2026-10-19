"""
utils/skill_extractor.py
--------------------------
Identifies technical & professional skills from text (resume or job description)
by matching against our comprehensive skills database and utilizing SpaCy NLP
for robust phrase and entity extraction.
"""

import re
import spacy
import sys
from data.skills_db import ALL_SKILLS

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print(
        "SpaCy model 'en_core_web_sm' not found. "
        "Run: python -m spacy download en_core_web_sm",
        file=sys.stderr,
    )
    nlp = spacy.blank("en")


def clean_text(text: str) -> str:
    """Lowercase and strip text for consistent matching."""
    return text.lower().strip()


def extract_skills(text: str) -> list:
    """
    Scans the input text and returns a sorted list of unique skills found,
    matched against ALL_SKILLS (which includes multi-word phrases and soft skills).
    """
    cleaned = clean_text(text)
    found_skills = set()

    # 1. Exact word-boundary regex matching against vocabulary
    for skill in ALL_SKILLS:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, cleaned):
            found_skills.add(skill)

    # 2. Dynamic NLP noun chunk matching for additional phrase context
    try:
        doc = nlp(cleaned)
        for chunk in doc.noun_chunks:
            chunk_str = chunk.text.strip()
            # Strip common prepositions / leading adjectives
            chunk_str = re.sub(r'^(a|an|the|our|your|strong|good|excellent|proven|ability|experience|knowledge|in|with|of|for|to)\s+', '', chunk_str)
            if chunk_str in ALL_SKILLS:
                found_skills.add(chunk_str)
    except Exception:
        pass

    return sorted(list(found_skills))


def get_resume_summary(text: str, num_sentences: int = 3) -> str:
    """
    Generates a quick extractive summary of the resume by picking the
    first few meaningful sentences.
    """
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 20]
    summary = " ".join(sentences[:num_sentences])
    return summary if summary else text[:300]
