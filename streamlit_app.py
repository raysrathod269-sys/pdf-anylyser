import streamlit as st
import google.generativeai as genai
from PIL import Image
import tempfile
import os

# Securely fetch API key from Streamlit secrets
try:
    MASTER_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=MASTER_API_KEY)
except Exception as e:
    st.error("API Key not found in Streamlit Secrets! Please add GEMINI_API_KEY in your app settings.")

st.set_page_config(page_title="AI Study Assistant Hub", page_icon="📚", layout="centered")

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>AI Study Assistant Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Your ultimate AI companion for instant smart notes and summaries!</p>", unsafe_allow_html=True)

# Only 2 options: Student and Working Professional
user_role = st.selectbox(
    "Select Your Category",
    ("Student", "Working Professional")
)

# File Upload Option - Supports Images, PDFs AND Videos!
uploaded_file = st.file_uploader(
    "Upload Study Notes, Image, PDF, or Any Video (Lecture/Notes)", 
    type=["png", "jpg", "jpeg", "pdf", "mp4", "mov", "avi", "webm"]
)

user_input = st.text_area("Or Paste Topic / Specific Questions", placeholder="Enter specific questions, topics, or extra notes here...")

if st.button("Generate AI Short Notes & Matrix", type="primary"):
    if not user_input.strip() and not uploaded_file:
        st.warning("Please upload a file (video/image/PDF) or enter some text/topic first!")
    else:
        spinner_text = "Processing file via AI Study Assistant Hub..." if uploaded_file else "Synthesizing notes and summary..."
        with st.spinner(spinner_text):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"You are an advanced AI assistant inside the AI Study Assistant Hub. The user category is: '{user_role}'. Based on the provided file or input, generate a crisp summary, structured smart revision notes, and key takeaways tailored specifically for this category.\n\nAdditional Details: {user_input}"
                
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
                        
                    elif file_extension == "pdf":
                        content_to_send.append(user_input)
                    else:
                        image = Image.open(uploaded_file)
                        content_to_send.append(image)

                response = model.generate_content(content_to_send)
                
                st.markdown("### AI Generated Insights & Short Notes:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error occurred during processing: {e}")
