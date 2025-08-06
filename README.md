# 🧠 LawBot — Free Legal Assistant for Everyone

LawBot is an open-source AI-powered legal assistant that provides free, accessible, and trustworthy legal guidance for all. Built using Gemini Pro, it helps users understand their rights, navigate legal issues, and access helpline resources — all for free.

---

## 🚀 Features

- 🔍 Ask any legal question in plain language
- 🧾 Get structured responses: issue, applicable law, actions to take
- 📚 Uses Retrieval-Augmented Generation (RAG) for document-based answers
- 🆘 Shows relevant government helpline info
- 💬 Built with free tools: Gemini Pro, Python, Streamlit

---

## 🛠️ Tech Stack

| Layer          | Tools Used                                                |
| -------------- | --------------------------------------------------------- |
| Frontend       | [Streamlit](https://streamlit.io/)                        |
| Backend        | Python + [Gemini Pro](https://makersuite.google.com/) SDK |
| RAG (Optional) | FAISS / Sentence Transformers                             |
| Deployment     | Streamlit Cloud / Render                                  |

---

## 💡 How It Works

1. User enters a legal query (e.g., "Can I get arrested without a warrant?")
2. LawBot optionally fetches relevant law chunks from legal documents (RAG)
3. Query + context sent to Gemini API with a structured prompt
4. Gemini returns:
   - Identified legal issue
   - Applicable Indian law
   - Recommended steps
   - Helpline or support links

---

## 📦 Installation

### 🔗 Clone the Repo

```bash
git clone https://github.com/your-username/lawbot.git
cd lawbot
```

### 🐍 Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 📥 Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔑 Setup API Keys

1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Get your Gemini API key
3. Add it in `.env` file:

```env
GEMINI_API_KEY=your-key-here
```

---

## ▶️ Run Locally

```bash
streamlit run app.py
```

---

## 🧪 Example Prompt

> "I’m being harassed at work. What should I do?"

✅ Output:

- **Legal Issue:** Workplace harassment
- **Law:** Indian Penal Code, 1860 – Sec 354A
- **Steps:** File a complaint with Internal Committee or police
- **Helpline:** National Women Helpline – 1091

---

## 🆓 Why Gemini?

- Free to use with Google account
- Supports structured responses
- No credit card required
- Easy to integrate via `google.generativeai` Python SDK

---

## 📄 File Structure

```
lawbot/
├── app.py                 # Streamlit app
├── lawbot_engine.py       # Core logic (RAG + prompt)
├── helpers.py             # Utilities & formatters
├── .env                   # API keys
├── requirements.txt       # Python deps
└── README.md              # Project docs
```

---

## 🛡️ Disclaimer

LawBot is **not a substitute for legal advice from a certified lawyer**. It is designed for **educational and informational** purposes only.

---

## 🙌 Contributing

Contributions are welcome! Feel free to:

- Create issues
- Improve prompt quality
- Add new legal datasets
- Enhance UI/UX

---

## 📬 Contact

Made with ❤️ by \[Arbin Mahato]

---

## 🏁 License

This project is licensed under the [MIT License](LICENSE).

```

---

Let me know if you want:

- `.env.example` file
- `requirements.txt` for Gemini + Streamlit
- The actual `app.py` using Gemini for LawBot

I'll provide them all — fully free + deployable.
```
