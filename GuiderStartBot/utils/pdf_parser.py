import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF file using PyMuPDF.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_speakers_with_links(text):
    """
    Extracts speaker names, organizations, and LinkedIn URLs from agenda text.
    """
    pattern = re.compile(
        r'Presenter: (.*?), (.*?) link\s*[:]? (https?://www\.linkedin\.com/in/[\w-]+)',
        re.IGNORECASE
    )
    matches = pattern.findall(text)

    speakers = []
    for name, org, link in matches:
        speakers.append({
            "name": name.strip(),
            "organization": org.strip(),
            "linkedin": link.strip()
        })

    return speakers

def extract_sessions(text):
    """
    Extracts session time and title from the agenda text.
    """
    session_pattern = re.findall(
        r'(\d{1,2}:\d{2}\s*(?:AM|PM)):\s+(.*?)\n',
        text
    )

    sessions = []
    for time, title in session_pattern:
        sessions.append({
            "time": time.strip(),
            "title": title.strip()
        })

    return sessions
