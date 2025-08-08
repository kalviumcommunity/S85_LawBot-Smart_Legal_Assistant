import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Dynamic LawBot",
    page_icon="⚡",
    layout="centered",
)

# Configure the Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("🚨 Gemini API key not found. Please create a .env file with your key.")
    st.stop()
genai.configure(api_key=api_key)

# --- MULTI-SHOT EXAMPLES (We keep these to control the *output format*) ---
# The examples teach the AI HOW to answer. The dynamic part changes WHAT we ask.
EXAMPLES = [
    # ... (You can copy the same EXAMPLES list from your multi-shot assignment)
    {
        "role": "user",
        "parts": ["In Punjab, what are the steps to file an FIR?"]
    },
    {
        "role": "model",
        "parts": [
            "**[Simplified Explanation]:** An FIR (First Information Report) is the first step to initiate a criminal proceeding. It is a document prepared by the police when they receive information about a cognizable offense.\n\n"
            "**[Legal Reference]:** Section 154 of the Code of Criminal Procedure, 1973.\n\n"
            "**[Actionable Steps]:**\n1. Visit the nearest police station in your jurisdiction in Punjab.\n2. Narrate the incident clearly to the officer.\n3. The officer will write it down, read it back to you, and you must sign it.\n4. You are entitled to a free copy of the FIR."
        ]
    }
]

# --- MODEL INITIALIZATION ---
SYSTEM_PROMPT = "You are an expert legal assistant specializing in Indian law. Your name is LawBot. Answer the user's questions based on their specific situation and location. You must follow the format of the examples precisely, using the bolded tags like **[Simplified Explanation]:**, **[Legal Reference]:**, and **[Actionable Steps]:**."

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# --- DYNAMIC USER INTERFACE (UI) ---
st.title("⚡ Dynamic Shot Prompting")
st.caption("Your Personal AI Legal Consultant")

st.write("Please provide the details of your situation below:")

# New UI elements to capture dynamic inputs
legal_issue = st.text_input("**What is your main legal issue?**", placeholder="e.g., Landlord not returning security deposit")
location = st.text_input("**In which State or UT are you located?**", placeholder="e.g., Chandigarh, Punjab, Haryana")
extra_details = st.text_area("**Provide any other relevant details:**", placeholder="e.g., I moved out 45 days ago, the agreement is silent on the return period.")

# --- CORE LOGIC ---
if st.button("Get Legal Advice"):
    if not legal_issue or not location:
        st.warning("Please fill in at least the legal issue and your location.")
    else:
        with st.spinner("LawBot is crafting your personalized advice..."):
            try:
                # This is the DYNAMIC PROMPT creation, structured to reduce injection risk.
                details_part = f" Here are some additional details: '{extra_details}'." if extra_details else ""
                final_prompt = (
                    f"A user is facing a legal issue in '{location}', India. "
                    f"The main problem is: '{legal_issue}'.{details_part} "
                    f"Based on this specific situation, what are their rights and what should they do?"
                )

                # We still use the examples to guide the output format
                response = model.generate_content(
                    EXAMPLES + [{"role": "user", "parts": [final_prompt]}]
                )

                st.subheader("LawBot's Personalized Advice:")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")