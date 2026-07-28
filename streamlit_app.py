import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="AI PDF Analyzer Pro", page_icon="📚")

st.title("🚀 AI PDF Analyzer & Study Assistant")
st.write(
    "Upload notes, textbooks, or work reports to get real AI-powered exam"
    " questions or executive summaries!"
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

if role == "Student":
  st.subheader("🎓 Student Exam Prep Mode (Powered by AI)")
  text_input = st.text_area(
      "Paste your textbook chapter or study notes here:"
  )

  if st.button("Generate Real AI Exam Questions"):
    if not api_key:
      st.error("Please enter your Gemini API key in the sidebar first!")
    elif not text_input:
      st.warning("Please paste some text first!")
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
  text_input = st.text_area("Paste your office report or document text here:")

  if st.button("Generate Real AI Summary"):
    if not api_key:
      st.error("Please enter your Gemini API key in the sidebar first!")
    elif not text_input:
      st.warning("Please paste some text first!")
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
