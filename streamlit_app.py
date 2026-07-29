import streamlit as st
import google.generativeai as genai
from PIL import Image
import tempfile
import os

st.set_page_config(page_title="AI Study Assistant Hub", page_icon="📚", layout="centered")

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>AI Study Assistant Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Your ultimate AI companion for instant smart notes and summaries!</p>", unsafe_allow_html=True)

# API Key Input Box
user_api_key = st.text_input("Enter your Gemini API Key", type="password", placeholder="Paste your AI Studio API key here...")

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
    if not user_api_key.strip():
        st.warning("Please enter your Gemini API Key in the box above first!")
    elif not user_input.strip() and not uploaded_file and not user_link.strip():
        st.warning("Please upload a file, paste a link, or enter some text/topic first!")
    else:
        try:
            clean_key = user_api_key.strip()
            genai.configure(api_key=clean_key)
            
            spinner_text = "Processing via AI Study Assistant Hub..."
            with st.spinner(spinner_text):
                # Using the standard active model for API keys
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                link_context = f"\nUser Provided Link/URL: {user_link}" if user_link.strip() else ""
                prompt = f"You are an advanced AI assistant inside the AI Study Assistant Hub. The user category is: '{user_role}'. Based on the provided file, link, or input, generate a crisp summary, structured smart revision notes, and key takeaways tailored specifically for this category.\n\nAdditional Details: {user_input}{link_context}"
                
                content_to_send = [prompt]
                
                if uploaded_file is not None:
                    file_extension = uploaded_file.name.split('.')[-1].lower()
                    
                    if file_extension in ["mp4", "mov", "avi", "webm"]:
                        st.info("Uploading and processing video... This might take a few moments.")
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
                            tmp_file.write(uploaded_file.read())
                            tmp_file_path = tmp_file.name
                        
                        video_file = genai.upload_file(path=tmp_file_path)
                        st.info("Video uploaded to AI engine successfully. Analyzing content...")
                        
                        content_to_send.append(video_file)
                        os.unlink(tmp_file_path)
                        
                    elif file_extension in ["pdf", "txt", "docx"]:
                        content_to_send.append(user_input)
                    else:
                        image = Image.open(uploaded_file)
                        content_to_send.append(image)

                response = model.generate_content(content_to_send)
                
                st.markdown("### AI Generated Insights & Short Notes:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error occurred: {e}")
