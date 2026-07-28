import google.generativeai as genai
import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="AI PDF Analyzer Pro", page_icon="📚")

st.title("🚀 AI PDF Analyzer & Study Assistant")
st.write(
    "Upload your PDF study notes, textbooks, or reports to get instant"
    " AI-powered exam questions or summaries!"
)

# Sidebar for API Key & Settings
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel("gemini-1.5-flash")
else:
  st.sidebar.warning("Please enter your Gemini API key to enable AI.")

# User Role Selection
role = st.sidebar.selectbox(
    "Select Your Role:", ["Student", "Working Professional"]
)


# Function to extract text from PDF
def extract_pdf_text(uploaded_file):
  reader = PdfReader(uploaded_file)
  text = ""
  for page in reader.pages:
    text += page.extract_text() or ""
  return text


if role == "Student":
  st.subheader("🎓 Student Exam Prep Mode (Powered by AI)")

  # Option to upload PDF or paste text
  upload_option = st.radio(
      "Choose input method:", ("Upload PDF File", "Paste Text")
  )

  text_input = ""
  if upload_option == "Upload PDF File":
    pdf_file = st.file_uploader("Upload your study PDF", type=["pdf"])
    if pdf_file is not None:
      with st.spinner("Reading PDF..."):
        text_input = extract_pdf_text(pdf_file)
        st.success(
            f"✅ PDF Successfully Read! ({len(text_input)} characters found)"
        )
  else:
    text_input = st.text_area(
        "Paste your textbook chapter or study notes here:"
    )

  if st.button("Generate Real AI Exam Questions"):
    if not api_key:
      st.error("Please enter your Gemini API key in the sidebar first!")
    elif not text_input:
      st.warning(
          "Please upload a PDF or paste some text first!"
      )
    else:
      with st.spinner("AI is generating high-yield exam questions..."):
        try:
          prompt = (
              "Act as an expert examiner. Based on the following study"
              " material, generate 3 important exam questions (1 MCQ, 1 Short"
              " Answer, and 1 Long Answer question) with answers:\n\n"
              + text_input
          )
          response = model.generate_content(prompt)
          st.success("✅ AI Generated Exam Questions:")
          st.markdown(response.text)
        except Exception as e:
          st.error(f"An error occurred: {e}")

elif role == "Working Professional":
  st.subheader("💼 Professional Work Summary Mode (Powered by AI)")

  upload_option = st.radio(
      "Choose input method:", ("Upload PDF File", "Paste Text"), key="pro_upload"
  )

  text_input = ""
  if upload_option == "Upload PDF File":
    pdf_file = st.file_uploader(
        "Upload your office report PDF", type=["pdf"], key="pro_pdf"
    )
    if pdf_file is not None:
      with st.spinner("Reading PDF..."):
        text_input = extract_pdf_text(pdf_file)
        st.success(
            f"✅ PDF Successfully Read! ({len(text_input)} characters found)"
        )
  else:
    text_input = st.text_area("Paste your office report or document text here:")

  if st.button("Generate Real AI Summary"):
    if not api_key:
      st.error("Please enter your Gemini API key in the sidebar first!")
    elif not text_input:
      st.warning(
          "Please upload a PDF or paste some text first!"
      )
    else:
      with st.spinner("AI is analyzing the document..."):
        try:
          prompt = (
              "Act as a professional business analyst. Provide a concise"
              " executive summary, 3 key takeaways, and action items based on"
              " this text:\n\n"
              + text_input
          )
          response = model.generate_content(prompt)
          st.success("✅ AI Executive Summary Generated:")
          st.markdown(response.text)
        except Exception as e:
          st.error(f"An error occurred: {e}")
