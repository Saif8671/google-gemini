# utils/matcher.py

import openai
import numpy as np
from utils.pdf_parser import extract_text_from_pdf

EMBEDDING_MODEL = "text-embedding-ada-002"

def get_embedding(text):
    response = openai.Embedding.create(
        input=[text],
        model=EMBEDDING_MODEL
    )
    return response['data'][0]['embedding']

def cosine_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def match_resume_to_sessions(resume_text, sessions):
    resume_embedding = get_embedding(resume_text)
    scored_sessions = []

    for session in sessions:
        session_text = session["title"]
        session_embedding = get_embedding(session_text)
        score = cosine_similarity(resume_embedding, session_embedding)
        scored_sessions.append((score, session))

    # Sort by score descending
    scored_sessions.sort(reverse=True, key=lambda x: x[0])
    return scored_sessions[:3]  # top 3 matches
