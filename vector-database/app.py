import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import numpy as np
import faiss

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Vector DB LawBot",
    page_icon="📚",
    layout="centered",
)

# Configure the Gemini API
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    st.error(f"🚨 Error configuring Gemini API. Please check your .env file. Error: {e}")
    st.stop()

# --- FUNCTIONS ---

def get_embedding(text):
    """Generates an embedding for a given piece of text."""
    if not text or not text.strip(): return None
    try:
        return genai.embed_content(model="models/embedding-001", content=text)['embedding']
    except Exception as e:
        st.error(f"Error generating embedding: {e}")
        return None

# --- KNOWLEDGE BASE & VECTOR DB SETUP ---
st.title("📚 Vector Database LawBot")
st.caption("The AI's Searchable Long-Term Memory")

try:
    # Load the knowledge base
    with open("knowledge_base.txt", "r", encoding="utf-8") as f:
        knowledge_base_text = f.read()

    # Split the text into chunks (paragraphs)
    text_chunks = [para.strip() for para in knowledge_base_text.split('\n\n') if para.strip()]

    # Generate embeddings for each chunk (this might take a moment on first run)
    with st.spinner("Building the AI's memory... Please wait."):
        if "embeddings" not in st.session_state:
            st.session_state.embeddings = [get_embedding(chunk) for chunk in text_chunks]
            # Filter out any None embeddings
            st.session_state.text_chunks = [chunk for i, chunk in enumerate(text_chunks) if st.session_state.embeddings[i] is not None]
            st.session_state.embeddings = [emb for emb in st.session_state.embeddings if emb is not None]

    # Create a FAISS index
    embeddings_np = np.array(st.session_state.embeddings).astype('float32')
    index = faiss.IndexFlatL2(embeddings_np.shape[1]) # L2 distance is a common choice
    index.add(embeddings_np)

    st.success(f"AI's memory built successfully! It has learned from {len(st.session_state.text_chunks)} legal articles.")
    st.write("---")

    # --- USER INTERFACE FOR SEARCH ---
    st.header("Ask a question about the Indian Constitution")
    user_query = st.text_input("Your query:", placeholder="e.g., How does the constitution protect my life?")

    if st.button("Search the AI's Memory"):
        if user_query:
            with st.spinner("Searching for the most relevant information..."):
                # 1. Embed the user's query
                query_embedding = get_embedding(user_query)

                if query_embedding:
                    # 2. Search the FAISS index
                    query_embedding_np = np.array([query_embedding]).astype('float32')
                    # Search for the top 2 most similar chunks
                    distances, indices = index.search(query_embedding_np, k=2)

                    # 3. Display the results
                    st.subheader("Most Relevant Information Found:")
                    for i in indices[0]:
                        st.markdown(f"> {st.session_state.text_chunks[i]}")
                        st.write("---")
                else:
                    st.error("Could not process your query.")
        else:
            st.warning("Please enter a query.")

except FileNotFoundError:
    st.error("knowledge_base.txt not found! Please create this file in the same directory.")
except Exception as e:
    st.error(f"An error occurred: {e}")