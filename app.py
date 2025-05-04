import streamlit as st
import re
import pdfplumber
import docx2txt
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import clean_text  # Assuming your cleaning function is in preprocess.py

# Initialize Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight BERT model for sentence embeddings

# Function to extract text from the uploaded resume file
def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        return ""

# Set up Streamlit UI
st.set_page_config(page_title="AI Resume Evaluator", layout="wide")
st.title("📄 AI Resume Evaluator using Llama")

# Upload resume
uploaded_file = st.file_uploader("Upload your resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

# Extract and clean the resume if uploaded
if uploaded_file:
    raw_text = extract_text(uploaded_file)
    cleaned_text = clean_text(raw_text)  # Cleaning the text
    
    st.subheader("📄 Cleaned Resume Preview")
    st.write(cleaned_text[:1000])  # Show partial resume

    # New: Input Job Description manually
    st.subheader("📝 Enter a Job Description")
    user_jd = st.text_area("Paste your desired Job Description here")

    # Match and show suitability
    if st.button("📊 Match Resume with JD"):
        with st.spinner("Calculating suitability..."):

            # Encode the cleaned resume and job description into sentence embeddings
            embeddings = model.encode([cleaned_text, user_jd])

            # Calculate Cosine Similarity between the embeddings
            similarity_score = cosine_similarity([embeddings[0]], [embeddings[1]]).flatten()[0]
            score = similarity_score * 100

            st.subheader("✅ Suitability Score")
            st.progress(int(score))
            st.markdown(f"**{score:.2f}% match** based on semantic similarity between JD and Resume.")

            # Extract matching and missing keywords based on simple text match for reference
            resume_keywords = set(cleaned_text.split())
            jd_keywords = set(user_jd.split())
            
            matched_keywords = resume_keywords.intersection(jd_keywords)
            missing_keywords = jd_keywords - resume_keywords

            st.markdown("### ✅ Matched Keywords")
            st.write(", ".join(matched_keywords) if matched_keywords else "No matches found.")

            st.markdown("### ❌ Missing Keywords")
            st.write(", ".join(missing_keywords) if missing_keywords else "None, great match!")

            # Further Improvements: Displaying a visualization of the match
            st.subheader("📊 Match Breakdown")
            # st.bar_chart([score, 100 - score], width=300, height=150, use_container_width=True)
            st.write(f"Resume and Job Description Match: {score:.2f}%")
            st.write(f"Remaining Gap: {100 - score:.2f}%")
