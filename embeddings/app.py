import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Embeddings Explorer",
    page_icon="➡️🔢",
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
    """Generates an embedding for a given piece of text."""
    if not text or not text.strip():
        return None
    try:
        # We use a specific model for embeddings
        result = genai.embed_content(
            model="models/embedding-001",
            content=text
        )
        return result['embedding']
    except Exception as e:
        st.error(f"Error generating embedding: {e}")
        return None

def calculate_similarity(vec1, vec2):
    """Calculates cosine similarity between two vectors."""
    # Cosine similarity is a measure of similarity between two non-zero vectors
    # It is the dot product of the vectors divided by the product of their magnitudes.
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2) if (norm_vec1 * norm_vec2) != 0 else 0.0

# --- USER INTERFACE (UI) ---
st.title("➡️🔢 LawBot's Embeddings Explorer")
st.caption("The first step in teaching an AI how to read and understand meaning.")

st.markdown("""
This tool demonstrates how **Embeddings** work. An embedding converts text into a list of numbers (a vector) that represents its semantic meaning.
- **Similar texts** will have similar vectors.
- **Different texts** will have different vectors.
We can measure this similarity mathematically using **Cosine Similarity** (a score from -1 to 1).
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Text 1")
    text1 = st.text_area("Enter the first piece of text:", key="text1", height=200, placeholder="e.g., What are the rights of a tenant in Nepal?")

with col2:
    st.subheader("Text 2")
    text2 = st.text_area("Enter the second piece of text:", key="text2", height=200, placeholder="e.g., What can a renter legally do if they have a problem?")

if st.button("Generate and Compare Embeddings", type="primary"):
    if text1 and text2:
        with st.spinner("Generating embeddings..."):
            embedding1 = get_embedding(text1)
            embedding2 = get_embedding(text2)

            if embedding1 is not None and embedding2 is not None:
                st.success("Embeddings generated successfully!")

                # Calculate similarity
                similarity_score = calculate_similarity(embedding1, embedding2)

                # Display results
                st.subheader("Results")
                st.metric(
                    label="Cosine Similarity Score",
                    value=f"{similarity_score:.4f}",
                    help="Closer to 1 means more similar. Closer to 0 means less similar."
                )

                with st.expander("View Embedding Vectors (Truncated)"):
                    st.write("**Embedding for Text 1:**")
                    st.code(f"[{', '.join(f'{x:.3f}' for x in embedding1[:5])}, ... , {', '.join(f'{x:.3f}' for x in embedding1[-5:])}] (Total {len(embedding1)} dimensions)")
                    st.write("**Embedding for Text 2:**")
                    st.code(f"[{', '.join(f'{x:.3f}' for x in embedding2[:5])}, ... , {', '.join(f'{x:.3f}' for x in embedding2[-5:])}] (Total {len(embedding2)} dimensions)")
    else:
        st.warning("Please enter text in both boxes.")