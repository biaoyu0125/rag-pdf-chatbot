import streamlit as st
from pypdf import PdfReader
import tempfile
import re

st.set_page_config(
    page_title="PDF Retrieval Chatbot",
    page_icon="📄"
)

st.title("PDF Retrieval Chatbot")

st.write(
    "Upload a PDF document and ask questions about its content."
)


# ---------- PDF TEXT EXTRACTION ----------

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)

    full_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            full_text += text + "\n"

    return full_text


# ---------- TEXT SPLITTING ----------

def split_text(text, chunk_size=800):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


# ---------- SIMPLE KEYWORD SEARCH ----------

def find_best_chunks(question, chunks):

    question_words = re.findall(r"\w+", question.lower())

    scored_chunks = []

    for chunk in chunks:

        chunk_lower = chunk.lower()

        score = 0

        for word in question_words:

            if word in chunk_lower:
                score += 1

        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True, key=lambda x: x[0])

    return scored_chunks[:3]


# ---------- FILE UPLOAD ----------

uploaded_file = st.file_uploader(
    "Upload a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:

    # Save temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:

        tmp_file.write(uploaded_file.read())

        pdf_path = tmp_file.name

    st.success("PDF uploaded successfully!")

    # Extract text
    text = extract_text_from_pdf(pdf_path)

    if len(text.strip()) == 0:

        st.error("No readable text found in PDF.")

    else:

        chunks = split_text(text)

        st.info(f"PDF processed into {len(chunks)} text chunks.")

        # User question
        question = st.text_input(
            "Ask a question about the PDF:"
        )

        if question:

            best_chunks = find_best_chunks(question, chunks)

            st.subheader("Most Relevant Content")

            found_result = False

            for score, chunk in best_chunks:

                if score > 0:

                    found_result = True

                    st.write(chunk)

                    st.divider()

            if not found_result:

                st.warning(
                    "No relevant content found for this question."
                )