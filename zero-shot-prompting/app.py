import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the environment variables (your API key) from the .env file
load_dotenv()

# --- CONFIGURATION ---
# Set page configuration for the Streamlit app
st.set_page_config(
    page_title="Zero-Shot LawBot",
    page_icon="🧠",
    layout="centered",
)

# Configure the Gemini API with the key from the .env file
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except AttributeError:
    st.error("🚨 Gemini API key not found. Please create a .env file with your key.")
    st.stop() # Stop the app if the key is not found

# --- MODEL INITIALIZATION ---
# This is our main instruction to the AI. This is the core of the prompt.
# It tells the AI what its personality and job are.
SYSTEM_PROMPT = "You are an expert legal assistant specializing in Indian law. Your name is LawBot. Answer the user's questions accurately, clearly, and concisely. If you don't know the answer, state that you do not have enough information."

# Initialize the Gemini Pro model with our system instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# --- USER INTERFACE (UI) ---
st.title("🧠 Zero-Shot LawBot")
st.caption("Ask a legal question, and the AI will answer without any prior examples.")

# Create a text input box for the user to ask their question
user_question = st.text_input("Enter your legal query about Indian Law:", key="user_query")

# --- CORE LOGIC ---
# This block runs when the user types something and presses Enter
if user_question:
    # Show a spinner while the AI is thinking
    with st.spinner("LawBot is analyzing your query..."):
        try:
            # This is the "Zero-Shot" part. We are sending the user's question directly.
            # We are not providing any examples of how to answer.
            # The `user_question` is the zero-shot prompt.
            response = model.generate_content(user_question)

            # Display the AI's response
            st.subheader("LawBot's Answer:")
            st.markdown(response.text)

        except Exception as e:
            # Handle potential errors from the API
            st.error(f"An error occurred: {e}")