import streamlit as st
from pathlib import Path
from utils.pdf_parser import extract_text_from_pdf, extract_speakers_with_links
from utils.linkedin_scraper import scrape_linkedin_profile
from bot import EventAssistantBot

# Page config
st.set_page_config(page_title="GuiderStartBot", layout="wide")

st.title("🤖 GuiderStartBot - Your Event Companion")

# Initialize session state for bot
if 'bot' not in st.session_state:
    st.session_state.bot = None

# Sidebar for uploads
st.sidebar.header("Upload Data")
agenda_file = st.sidebar.file_uploader("Upload Agenda (PDF)", type=["pdf"])

# Save uploaded agenda and initialize bot
if agenda_file:
    agenda_path = Path("data/agenda.pdf")
    agenda_path.parent.mkdir(parents=True, exist_ok=True)
    with open(agenda_path, "wb") as f:
        f.write(agenda_file.read())
    st.sidebar.success("✅ Agenda uploaded")
    
    # Initialize the bot with the agenda
    api_key = "YOUR_GEMINI_API_KEY"  # Replace with your actual API key
    st.session_state.bot = EventAssistantBot(api_key, str(agenda_path))

# Chat interface
st.subheader("💬 Chat with Event Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about the event!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    if st.session_state.bot:
        response = st.session_state.bot.answer_question(prompt)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        with st.chat_message("assistant"):
            st.markdown("Please upload an agenda PDF first to start the conversation!")

# Display agenda preview if uploaded
if agenda_file and st.session_state.bot:
    with st.expander("📄 View Agenda"):
        agenda_text = extract_text_from_pdf("data/agenda.pdf")
        st.text_area("Extracted Agenda Text", agenda_text[:2000], height=300)
        
        # Extract speaker info
        speaker_data = extract_speakers_with_links(agenda_text)
        if speaker_data:
            st.subheader("🔎 Speakers")
            for speaker in speaker_data:
                profile = scrape_linkedin_profile(
                    speaker["name"], speaker["organization"], speaker["linkedin"]
                )
                with st.expander(f"🗣️ {profile['name']} – {profile['title']}"):
                    st.markdown(f"**Organization:** {profile['organization']}")
                    st.markdown(f"**LinkedIn:** [View Profile]({profile['linkedin']})")
                    st.markdown(f"**Skills:** {', '.join(profile['skills'])}")