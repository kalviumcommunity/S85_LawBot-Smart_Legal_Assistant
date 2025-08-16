import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Top P Tuning LawBot",
    page_icon="🅿️",
    layout="centered",
)

# Configure the Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("🚨 Gemini API key not found. Please create a .env file with your key.")
    st.stop()
genai.configure(api_key=api_key)

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
st.title("🅿️ Top P Tuning LawBot")
st.caption("Control the AI's pool of word choices")

# NEW: Add a slider to control Top P
top_p_slider = st.slider(
    "**Select Top P:** (Low = Safe & Predictable, High = Diverse & Creative)",
    min_value=0.0,
    max_value=1.0,
    value=0.95,  # A standard, high-quality default
    step=0.05
)

st.write("---")
st.write("Please provide the details of your situation below:")

legal_issue = st.text_input("**What is your main legal issue?**", placeholder="e.g., What is the 'basic structure doctrine'?")
location = st.text_input("**In which country's context?**", placeholder="e.g., India")
extra_details = st.text_area("**Provide any other relevant details:**", placeholder="e.g., I'm a law student trying to understand its importance in constitutional law.")

# --- CORE LOGIC ---
if st.button("Get Legal Advice"):
    if not legal_issue or not location:
        st.warning("Please fill in at least the legal issue and country.")
    else:
        with st.spinner("LawBot is crafting your advice..."):
            try:
                # NEW: Create a generation_config to pass Top P
                # NOTE: For Gemini, you typically use either Temperature OR Top P/Top K, not all at once.
                # The model's default sampling method will use the parameter you provide.
                generation_config = genai.types.GenerationConfig(
                    top_p=top_p_slider
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

                st.subheader(f"LawBot's Advice (Top P: {top_p_slider})")
                st.markdown(response.text)

            except Exception as e:
                st.error("An unexpected error occurred while generating advice. Please try again later.")