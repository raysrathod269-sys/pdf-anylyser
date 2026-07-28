import streamlit as st

st.set_page_config(page_title="AI PDF Analyzer", page_icon="📚")

st.title("🚀 AI PDF Analyzer for Students & Professionals")
st.write(
    "Upload or paste your study material or work documents to generate instant"
    " summaries or exam questions!"
)

# User Role Selection
role = st.selectbox(
    "Select Your Role:", ["-- Select Role --", "Student", "Working Professional"]
)

if role == "Student":
  st.subheader("🎓 Student Exam Prep Mode")
  text_input = st.text_area("Paste your textbook chapter or notes here:")
  if st.button("Generate Exam Questions"):
    if text_input:
      st.success("✅ Important Exam Questions Generated:")
      st.markdown(
          "1. **[MCQ]** What is the core concept of this chapter?\n2."
          " **[Short Answer]** Explain the primary mechanism described."
          "\n3. **[Essay]** Discuss the significance of this topic for exams."
      )
    else:
      st.warning("Please paste some text first!")

elif role == "Working Professional":
  st.subheader("💼 Professional Work Summary Mode")
  text_input = st.text_area("Paste your report or office document here:")
  if st.button("Generate Summary"):
    if text_input:
      st.success("✅ Executive Work Summary Generated:")
      st.markdown(
          "**Executive Summary:** This document outlines key operational"
          " metrics.\n\n**Key Takeaways:**\n- Point 1\n- Point"
          " 2\n\n**Deadlines/Action Items:** None specified."
      )
    else:
      st.warning("Please paste some text first!")
