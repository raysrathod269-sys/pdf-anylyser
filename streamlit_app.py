import streamlit as st
import google.generativeai as genai
from PIL import Image

# MASTER API KEY - Yahan apni original Gemini API key daal dena
MASTER_API_KEY = "TU_APNI_GEMINI_API_KEY_YAHAN_DAL_DENA"

# Configure Gemini API
genai.configure(api_key=MASTER_API_KEY)

st.set_page_config(page_title="AI Study & Summary Matrix", page_icon="📚", layout="centered")

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>Neural Study Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Select your role, upload notes or type text, and get instant AI insights.</p>", unsafe_allow_html=True)

# Role Selection
user_role = st.selectbox(
    "Select Your Role",
    ("Student (PCB / NEET Aspirant)", "UPSC / Civil Services Aspirant", "Working Professional")
)

# File Upload Option
uploaded_file = st.file_uploader("Upload Study Image or Document (Optional)", type=["png", "jpg", "jpeg", "pdf"])

# Text Input
user_input = st.text_area("Or Paste Topic / Notes Details", placeholder="Enter text or video topic details here...")

if st.button("Generate AI Matrix & Notes", type="primary"):
    if not user_input.strip() and not uploaded_file:
        st.warning("Please enter some text or upload a file first!")
    else:
        with st.spinner("Processing via Neural AI..."):
            try:
                # Select Gemini Model (Flash handles text and images seamlessly)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"You are an advanced AI study assistant. The user is a {user_role}. Based on the provided input/file, generate a crisp summary, structured smart notes, and key takeaways.\n\nAdditional Notes: {user_input}"
                
                content_to_send = [prompt]
                
                if uploaded_file is not None:
                    if uploaded_file.type == "application/pdf":
                        st.info("PDF processing note: Ensure text can be read or use image upload for best results.")
                        content_to_send.append(user_input)
                    else:
                        image = Image.open(uploaded_file)
                        content_to_send.append(image)

                response = model.generate_content(content_to_send)
                
                st.markdown("### AI Generated Insights:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error occurred: {e}")
