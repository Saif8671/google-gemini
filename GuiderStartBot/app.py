import streamlit as st
from pathlib import Path
from utils.pdf_parser import extract_text_from_pdf, extract_speakers_with_links
from utils.linkedin_scraper import scrape_linkedin_profile

# Page config
st.set_page_config(page_title="GuiderStartBot", layout="wide")

st.title("🤖 GuiderStartBot - Your Event Companion")

# Sidebar for uploads
st.sidebar.header("Upload Data")
agenda_file = st.sidebar.file_uploader("Upload Agenda (PDF)", type=["pdf"])
resume_files = st.sidebar.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

# Save uploaded agenda
if agenda_file:
    agenda_path = Path("data/agenda.pdf")
    agenda_path.parent.mkdir(parents=True, exist_ok=True)
    with open(agenda_path, "wb") as f:
        f.write(agenda_file.read())
    st.sidebar.success("✅ Agenda uploaded")

# Save uploaded resumes
if resume_files:
    resumes_dir = Path("data/resumes")
    resumes_dir.mkdir(parents=True, exist_ok=True)
    for resume in resume_files:
        resume_path = resumes_dir / resume.name
        with open(resume_path, "wb") as f:
            f.write(resume.read())
    st.sidebar.success(f"✅ Uploaded {len(resume_files)} resumes")

# Parse and display agenda
if agenda_file:
    st.subheader("🗓️ Agenda Preview")
    agenda_text = extract_text_from_pdf("data/agenda.pdf")
    st.text_area("Extracted Agenda Text", agenda_text[:2000], height=300)

    # Extract speaker info
    st.subheader("🔎 Extracted Speaker Details")
    speaker_data = extract_speakers_with_links(agenda_text)

    if speaker_data:
        for speaker in speaker_data:
            profile = scrape_linkedin_profile(
                speaker["name"], speaker["organization"], speaker["linkedin"]
            )
            with st.expander(f"🗣️ {profile['name']} – {profile['title']}"):
                st.markdown(f"**Organization:** {profile['organization']}")
                st.markdown(f"**LinkedIn:** [View Profile]({profile['linkedin']})")
                st.markdown(f"**Skills:** {', '.join(profile['skills'])}")
    else:
        st.info("No speaker LinkedIn links found in the agenda.")

# Resume preview
if resume_files:
    st.subheader("👤 Resume Sample Preview")
    first_resume_path = f"data/resumes/{resume_files[0].name}"
    resume_text = extract_text_from_pdf(first_resume_path)
    st.text_area("Extracted Resume Text", resume_text[:2000], height=300)
