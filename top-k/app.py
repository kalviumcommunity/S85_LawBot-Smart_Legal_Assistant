import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Top K Tuning LawBot",
    page_icon="🇰",
    layout="centered",
)

# Configure the Gemini API
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except AttributeError:
    st.error("🚨 Gemini API key not found. Please create a .env file with your key.")
    st.stop()

# --- ONE-SHOT EXAMPLE (To maintain our structured output) ---
EXAMPLES = [
    {
        "role": "user",
        "parts": ["How can I report cyberbullying in India?"]
    },
    {
        "role": "model",
        "parts": [
            "**[Simplified Explanation]:** Cyberbullying is a crime in India where electronic communication is used to harass, threaten, or intimidate someone. You can report this to the police for legal action.\n\n"
            "**[Legal Reference]:** The Information Technology Act, 2000, and various sections of the Indian Penal Code (IPC) can be applied depending on the nature of the harassment.\n\n"
            "**[Actionable Steps]:**\n1. Take screenshots and save URLs as evidence.\n2. Do not engage with or respond to the bully.\n3. Report the user on the social media platform.\n4. File a formal complaint with the National Cyber Crime Reporting Portal (cybercrime.gov.in) or the nearest police station."
        ]
    }
]

# --- MODEL INITIALIZATION ---
SYSTEM_PROMPT = "You are an expert legal assistant specializing in Indian law. Your name is LawBot. Answer the user's questions based on their specific situation. You must follow the format of the provided example precisely, using the bolded tags like **[Simplified Explanation]:**, **[Legal Reference]:**, and **[Actionable Steps]:**."

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# --- DYNAMIC USER INTERFACE (UI) ---
st.title("🇰 Top K Tuning LawBot")
st.caption("Control the AI's vocabulary size")

# NEW: Add a slider to control Top K
top_k_slider = st.slider(
    "**Select Top K:** (Low = Safe & Repetitive, High = Natural & Diverse)",
    min_value=1,
    max_value=100,
    value=40,  # A standard, high-quality default
    step=1
)

st.write("---")
st.write("Please provide the details of your situation below:")

legal_issue = st.text_input("**What is your main legal issue?**", placeholder="e.g., Explain 'judicial review'")
location = st.text_input("**In which country's context?**", placeholder="e.g., India")
extra_details = st.text_area("**Provide any other relevant details:**", placeholder="e.g., I'm a student trying to understand its role in protecting fundamental rights.")

# --- CORE LOGIC ---
if st.button("Get Legal Advice"):
    if not legal_issue or not location:
        st.warning("Please fill in at least the legal issue and country.")
    else:
        with st.spinner("LawBot is crafting your advice..."):
            try:
                # NEW: Create a generation_config to pass Top K
                generation_config = genai.types.GenerationConfig(
                    top_k=top_k_slider
                )

                final_prompt = (
                    f"In the context of '{location}', "
                    f"the main question is: '{legal_issue}'. "
                    f"Here are some additional details: '{extra_details}'. "
                    f"Based on this specific situation, what is the answer?"
                )
                
                response = model.generate_content(
                    EXAMPLES + [{"role": "user", "parts": [final_prompt]}],
                    generation_config=generation_config
                )

                st.subheader(f"LawBot's Advice (Top K: {top_k_slider})")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")