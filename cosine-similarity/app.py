import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Cosine Similarity Explorer",
    page_icon="📐",
    layout="wide",
)

# Configure the Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("🚨 Gemini API key not found. Please create a .env file with your key.")
    st.stop()
genai.configure(api_key=api_key)

# --- FUNCTIONS ---
def get_embedding(text):
    """Generates an embedding for a given piece of text."""
    if not text or not text.strip(): return None
    try:
        return genai.embed_content(model=EMBEDDING_MODEL, content=text)['embedding']
    except Exception as e:
        st.error(f"Error generating embedding: {e}")
        return None

def calculate_cosine_similarity(vec1, vec2):
    """Calculates cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    # Avoid division by zero
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return dot_product / (norm_vec1 * norm_vec2)

# --- USER INTERFACE (UI) ---
st.title("📐 LawBot's Cosine Similarity Explorer")
st.caption("The mathematical engine behind AI search and retrieval.")

st.markdown("""
**Cosine Similarity** measures the similarity between two text passages by calculating the cosine of the angle between their embedding vectors.
- **Score ≈ 1:** The texts are very similar in meaning.
- **Score ≈ 0:** The texts are unrelated.
- **Score ≈ -1:** The texts have opposite meanings.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Text 1")
    text1 = st.text_area("Enter the first piece of text:", key="text1", height=200, placeholder="e.g., What are the fundamental duties of an Indian citizen?")

with col2:
    st.subheader("Text 2")
    text2 = st.text_area("Enter the second piece of text:", key="text2", height=200, placeholder="e.g., What are the responsibilities of a person living in India?")

if st.button("Calculate Similarity", type="primary"):
    if text1 and text2:
        with st.spinner("Generating embeddings and calculating..."):
            embedding1 = get_embedding(text1)
            embedding2 = get_embedding(text2)

            if embedding1 is not None and embedding2 is not None:
                similarity_score = calculate_cosine_similarity(embedding1, embedding2)

                st.success("Calculation Complete!")
                st.subheader("Results")

                # Interpret the score
                if similarity_score > 0.8:
                    interpretation = "Highly Similar"
                elif similarity_score > 0.6:
                    interpretation = "Moderately Similar"
                elif similarity_score > 0.3:
                    interpretation = "Somewhat Related"
                else:
                    interpretation = "Not Similar"

                st.metric(
                    label="Cosine Similarity Score",
                    value=f"{similarity_score:.4f}",
                    help=f"This score indicates the texts are **{interpretation}**."
                )
                st.info(f"**Interpretation:** The two text passages are considered **{interpretation}**. A higher score means their conceptual meanings are closer.")

    else:
        st.warning("Please enter text in both boxes.")