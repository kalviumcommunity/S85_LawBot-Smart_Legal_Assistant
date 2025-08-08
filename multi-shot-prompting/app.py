import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Multi-Shot LawBot",
    page_icon="⚖️",
    layout="centered",
)

# Configure the Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("🚨 Gemini API key not found. Please create a .env file with your key.")
    st.stop()
genai.configure(api_key=api_key)

# --- MULTI-SHOT EXAMPLES (FINAL VERSION WITH BOLD HEADERS) ---
# This version has bolding for the headers.
EXAMPLES = [
    {
        "role": "user",
        "parts": ["What are the steps to file an FIR in India?"]
    },
    {
        "role": "model",
        "parts": [
            "**[Simplified Explanation]:** An FIR (First Information Report) is the first step to initiate a criminal proceeding. It is a document prepared by the police when they receive information about a cognizable offense.\n\n"
            "**[Legal Reference]:** Section 154 of the Code of Criminal Procedure, 1973.\n\n"
            "**[Actionable Steps]:**\n1. Visit the nearest police station.\n2. Narrate the incident clearly to the officer.\n3. The officer will write it down, read it back to you, and you must sign it.\n4. You are entitled to a free copy of the FIR."
        ]
    },
    {
        "role": "user",
        "parts": ["What is the Right to Information (RTI)?"]
    },
    {
        "role": "model",
        "parts": [
            "**[Simplified Explanation]:** The Right to Information gives every Indian citizen the right to get information from any public authority or government body, promoting transparency and accountability.\n\n" # <-- BOLD MARKDOWN ADDED
            "**[Legal Reference]:** The Right to Information Act, 2005.\n\n" # <-- BOLD MARKDOWN ADDED
            "**[Actionable Steps]:**\n1. Identify the Public Information Officer (PIO) of the concerned department.\n2. Write a clear application specifying the information you need.\n3. Pay the nominal application fee.\n4. The PIO is legally bound to provide the information within 30 days." # <-- BOLD MARKDOWN ADDED
        ]
    }
]

# --- MODEL INITIALIZATION ---
SYSTEM_PROMPT = "You are an expert legal assistant specializing in Indian law. Your name is LawBot. Answer the user's questions based on the provided examples. You must follow the format of the examples precisely, using the bolded tags like **[Simplified Explanation]:**, **[Legal Reference]:**, and **[Actionable Steps]:**, including all line breaks between sections and within lists."

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# --- USER INTERFACE (UI) ---
st.title("⚖️ Multi-Shot Prompting")
st.caption("This bot uses multi-shot prompting to provide structured legal answers.")

user_question = st.text_input("Enter your legal query about Indian Law:", key="user_query")

# --- CORE LOGIC ---
if user_question:
    with st.spinner("LawBot is analyzing your query..."):
        try:
            response = model.generate_content(
                EXAMPLES + [{"role": "user", "parts": [user_question]}]
            )
            st.subheader("LawBot's Structured Answer:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")