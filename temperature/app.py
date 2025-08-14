import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Temperature Tuning LawBot",
    page_icon="🌡️",
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
        "parts": ["How can I report cyberbullying in Nepal?"]
    },
    {
        "role": "model",
        "parts": [
            "**[Simplified Explanation]:** Cyberbullying is a crime in Nepal where electronic communication is used to harass, threaten, or intimidate someone. You can report this to the police for legal action.\n\n"
            "**[Legal Reference]:** The Electronic Transactions Act, 2063 (2008), specifically Section 47, which penalizes online harassment.\n\n"
            "**[Actionable Steps]:**\n1. Take screenshots and save URLs as evidence.\n2. Do not engage with or respond to the bully.\n3. Report the user on the social media platform.\n4. File a formal complaint with the Nepal Police Cyber Bureau."
        ]
    }
]

# --- MODEL INITIALIZATION ---
SYSTEM_PROMPT = "You are an expert legal assistant specializing in Nepalese law. Your name is LawBot. Answer the user's questions based on their specific situation. You must follow the format of the provided example precisely, using the bolded tags like **[Simplified Explanation]:**, **[Legal Reference]:**, and **[Actionable Steps]:**."

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# --- DYNAMIC USER INTERFACE (UI) ---
st.title("🌡️ Temperature Tuning LawBot")
st.caption("Control the AI's creativity")

# NEW: Add a slider to control the temperature
temp_slider = st.slider(
    "**Select Temperature:** (Low = Factual, High = Creative)",
    min_value=0.0,
    max_value=1.0,
    value=0.3,  # A good default for a legal bot
    step=0.1
)

st.write("---")
st.write("Please provide the details of your situation below:")

legal_issue = st.text_input("**What is your main legal issue?**", placeholder="e.g., Landlord not returning security deposit")
location = st.text_input("**In which city or province are you located?**", placeholder="e.g., Kathmandu, Pokhara")
extra_details = st.text_area("**Provide any other relevant details:**", placeholder="e.g., I moved out 45 days ago, the agreement is silent on the return period.")

# --- CORE LOGIC ---
if st.button("Get Legal Advice"):
    if not legal_issue or not location:
        st.warning("Please fill in at least the legal issue and your location.")
    else:
        with st.spinner("LawBot is crafting your advice..."):
            try:
                # NEW: Create a generation_config to pass the temperature
                generation_config = genai.types.GenerationConfig(
                    temperature=temp_slider
                )

                final_prompt = (
                    f"I am facing a legal issue in '{location}', Nepal. "
                    f"The main problem is: '{legal_issue}'. "
                    f"Here are some additional details: '{extra_details}'. "
                    f"Based on this specific situation, what are my rights and what should I do?"
                )
                
                response = model.generate_content(
                    EXAMPLES + [{"role": "user", "parts": [final_prompt]}],
                    generation_config=generation_config  # Pass the config here
                )

                st.subheader(f"LawBot's Advice (Temperature: {temp_slider})")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")