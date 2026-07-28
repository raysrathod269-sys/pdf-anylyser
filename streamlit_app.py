import google.generativeai as genai
from PIL import Image
import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="AI PDF & Image Analyzer Pro", page_icon="📚")

st.title("🚀 AI PDF, Image & Study Assistant")
st.write(
    "Upload your study notes (PDF, Image, or Text) to get instant AI-powered"
    " exam questions or summaries!"
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

  # Option to upload PDF, Image, or paste text
  upload_option = st.radio(
      "Choose input method:",
      ("Upload PDF File", "Upload Image / Screenshot", "Paste Text"),
  )

  input_data = None
  input_type = None

  if upload_option == "Upload PDF File":
    pdf_file = st.file_uploader("Upload your study PDF", type=["pdf"])
    if pdf_file is not None:
      with st.spinner("Reading PDF..."):
        input_data = extract_pdf_text(pdf_file)
        input_type = "text"
        st.success(
            f"✅ PDF Successfully Read! ({len(input_data)} characters found)"
        )

  elif upload_option == "Upload Image / Screenshot":
    image_file = st.file_uploader(
        "Upload image or screenshot of your notes/book",
        type=["png", "jpg", "jpeg"],
    )
    if image_file is not None:
      input_data = Image.open(image_file)
      input_type = "image"
      st.image(
          input_data,
          caption="Uploaded Image",
          use_container_width=True,
      )
      st.success("✅ Image Successfully Uploaded!")

  else:
    input_data = st.text_area(
        "Paste your textbook chapter or study notes here:"
    )
    input_type = "text"

  if st.button("Generate Real AI Exam Questions"):
    if not api_key:
      st.error("Please enter your Gemini API key in the sidebar first!")
    elif not input_data:
      st.warning(
          "Please upload a file, image, or paste some text first!"
      )
    else:
      with st.spinner("AI is generating high-yield exam questions..."):
        try:
          prompt = (
              "Act as an expert examiner. Based on the provided study"
              " material/image, generate important exam questions with"
              " answers:"
          )

          if input_type == "image":
            response = model.generate_content([prompt, input_data])
          else:
            response = model.generate_content(prompt + "\n\n" + input_data)

          st.success("✅ AI Generated Exam Questions:")
          st.markdown(response.text)
        except Exception as e:
          st.error(f"An error occurred: {e}")

elif role == "Working Professional":
  st.subheader("💼 Professional Work Summary Mode (Powered by AI)")

  upload_option = st.radio(
      "Choose input method:",
      ("Upload PDF File", "Upload Image / Screenshot", "Paste Text"),
      key="pro_upload",
  )

  input_data = None
  input_type = None

  if upload_option == "Upload PDF File":
    pdf_file = st.file_uploader(
        "Upload your office report PDF", type=["pdf"], key="pro_pdf"
    )
    if pdf_file is not None:
      with st.spinner("Reading PDF..."):
        input_data = extract_pdf_text(pdf_file)
        input_type = "text"
        st.success(
            f"✅ PDF Successfully Read! ({len(input_data)} characters found)"
        )

  elif upload_option == "Upload Image / Screenshot":
    image_file = st.file_uploader(
        "Upload image or screenshot of report/document",
        type=["png", "jpg", "jpeg"],
        key="pro_img",
    )
    if image_file is not None:
      input_data = Image.open(image_file)
      input_type = "image"
      st.image(
          input_data,
          caption="Uploaded Image",
          use_container_width=True,
      )
      st.success("✅ Image Successfully Uploaded!")

  else:
    input_data = st.text_area(
        "Paste your office report or document text here:", key="pro_text"
    )
    input_type = "text"

  if st.button("Generate Real AI Summary"):
    if not api_key:
      st.error("Please enter your Gemini API key in the sidebar first!")
    elif not input_data:
      st.warning(
          "Please upload a file, image, or paste some text first!"
      )
    else:
      with st.spinner("AI is analyzing the document..."):
        try:
          prompt = (
              "Act as a professional business analyst. Provide a concise"
              " executive summary, key takeaways, and insights based on this"
              " text/image:"
          )

          if input_type == "image":
            response = model.generate_content([prompt, input_data])
          else:
            response = model.generate_content(prompt + "\n\n" + input_data)

          st.success("✅ AI Executive Summary Generated:")
          st.markdown(response.text)
        except Exception as e:
          st.error(f"An error occurred: {e}")
