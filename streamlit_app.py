import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from PIL import Image
import tempfile
import os

st.set_page_config(page_title="AI Study Assistant Hub", page_icon="📚", layout="centered")

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>AI Study Assistant Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Your ultimate AI companion for instant smart notes and summaries!</p>", unsafe_allow_html=True)

# Fetch API key/token from Streamlit secrets safely
try:
    MASTER_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception as e:
    st.error("API Key not found in Streamlit Secrets! Please add GEMINI_API_KEY in your app settings.")
    MASTER_API_KEY = None

# User Role Category
user_role = st.selectbox(
    "Select Your Category",
    ("Student", "Working Professional")
)

# File Upload Option
uploaded_file = st.file_uploader(
    "Upload Document (PDF), Image, or Video File", 
    type=["pdf", "png", "jpg", "jpeg", "mp4", "mov", "avi", "webm", "txt", "docx"]
)

# Link/URL input field
user_link = st.text_input("Or Paste Link / URL (YouTube, Website, etc.)", placeholder="https://...")

user_input = st.text_area("Or Paste Topic / Specific Questions", placeholder="Enter specific questions, topics, or extra notes here...")

if st.button("Generate AI Short Notes & Matrix", type="primary"):
    if not MASTER_API_KEY:
        st.error("Master API Key is missing in app settings.")
    elif not user_input.strip() and not uploaded_file and not user_link.strip():
        st.warning("Please upload a file, paste a link, or enter some text/topic first!")
    else:
        try:
            spinner_text = "Processing via Vertex AI Engine..."
            with st.spinner(spinner_text):
                # Initialize Vertex AI using project credentials from the token key
                # Note: For Vertex tokens, ensure project is set if required, or let SDK parse it
                model = GenerativeModel("gemini-1.5-flash")
                
                link_context = f"\nUser Provided Link/URL: {user_link}" if user_link.strip() else ""
                prompt = f"You are an advanced AI assistant inside the AI Study Assistant Hub. The user category is: '{user_role}'. Based on the provided file, link, or input, generate a crisp summary, structured smart revision notes, and key takeaways tailored specifically for this category.\n\nAdditional Details: {user_input}{link_context}"
                
                content_to_send = [prompt]
                
                if uploaded_file is not None:
                    file_extension = uploaded_file.name.split('.')[-1].lower()
                    
                    if file_extension in ["pdf", "txt", "docx"]:
                        content_to_send.append(user_input)
                    else:
                        image = Image.open(uploaded_file)
                        content_to_send.append(image)

                response = model.generate_content(content_to_send)
                
                st.markdown("### AI Generated Insights & Short Notes:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error occurred: {e}")
            
