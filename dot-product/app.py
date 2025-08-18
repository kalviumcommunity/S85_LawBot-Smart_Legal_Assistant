import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Similarity Metrics Explorer",
    page_icon="✨",
    layout="wide",
)

# Configure the Gemini API
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except AttributeError:
    st.error("🚨 Gemini API key not found. Please create a .env file with your key.")
    st.stop()

# --- FUNCTIONS ---
def get_embedding(text):
    if not text or not text.strip(): return None
    try:
        return genai.embed_content(model="models/embedding-001", content=text)['embedding']
    except Exception as e:
        st.error(f"Error generating embedding: {e}")
        return None

def calculate_cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0: return 0.0
    return dot_product / (norm_vec1 * norm_vec2)

def calculate_l2_distance(vec1, vec2):
    return np.linalg.norm(np.array(vec1) - np.array(vec2))

def calculate_dot_product(vec1, vec2):
    # The raw dot product of the two vectors.
    return np.dot(vec1, vec2)

# --- USER INTERFACE (UI) ---
st.title("✨ LawBot's Complete Similarity Explorer")
st.caption("Comparing Cosine Similarity vs. L2 Distance vs. Dot Product")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Text 1")
    text1 = st.text_area("Enter the first piece of text:", key="text1", height=200, placeholder="e.g., What are the powers of the Supreme Court of India?")
with col2:
    st.subheader("Text 2")
    text2 = st.text_area("Enter the second piece of text:", key="text2", height=200, placeholder="e.g., What is the jurisdiction of India's highest court?")

if st.button("Calculate All Similarity Metrics", type="primary"):
    if text1 and text2:
        with st.spinner("Generating embeddings and calculating..."):
            embedding1 = get_embedding(text1)
            embedding2 = get_embedding(text2)

            if embedding1 is not None and embedding2 is not None:
                st.success("Calculation Complete!")
                st.subheader("Results")

                cosine_score = calculate_cosine_similarity(embedding1, embedding2)
                l2_score = calculate_l2_distance(embedding1, embedding2)
                dot_product_score = calculate_dot_product(embedding1, embedding2)

                res_col1, res_col2, res_col3 = st.columns(3)
                with res_col1:
                    st.metric(label="Cosine Similarity", value=f"{cosine_score:.4f}", help="Measures angle. Higher (≈1) is more similar.")
                with res_col2:
                    st.metric(label="L2 Distance", value=f"{l2_score:.4f}", help="Measures distance. Lower (≈0) is more similar.")
                with res_col3:
                    st.metric(label="Dot Product", value=f"{dot_product_score:.4f}", help="Measures overlap & magnitude. Higher is more similar.")
    else:
        st.warning("Please enter text in both boxes.")