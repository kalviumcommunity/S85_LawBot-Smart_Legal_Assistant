# 🧠 LawBot — Free Legal Assistant for Everyone

LawBot is an open-source AI-powered legal assistant that provides free, accessible, and trustworthy legal guidance for all. Built using Gemini Pro, it helps users understand their rights, navigate legal issues, and access helpline resources — all for free.

---

## 🚀 Features

- 🔍 Ask any legal question in plain language
- 🧾 Get structured responses: issue, applicable law, actions to take
- 📚 Uses Retrieval-Augmented Generation (RAG) for document-based answers
- ☎️ Shows relevant government helpline info by state
- 💬 Built with free tools: Gemini Pro, Python, Streamlit

---

## ✅ GenAI Concepts Covered

| Feature                  | How LawBot Implements It                                                             |
| ------------------------ | ------------------------------------------------------------------------------------ |
| **✅ Prompting**         | Interprets natural language legal queries using structured **system + user prompts** |
| **✅ Structured Output** | Outputs clean sections like: **Issue, Law, Actionable Steps, Helpline**              |
| **✅ Function Calling**  | Dynamically fetches **state-wise legal helplines** via custom Python functions       |
| **✅ RAG**               | Retrieves law sections from real legal PDFs using **FAISS + sentence embeddings**    |

> ✔ This makes LawBot a complete GenAI project, demonstrating real-world application of advanced AI concepts.

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

1. **User enters a legal query** (e.g., _"Can I get arrested without a warrant?"_)
2. **Optional RAG step:** Bot fetches relevant laws from real legal PDFs using FAISS
3. **Gemini Prompt:** The question + retrieved context is sent with structured prompts
4. **Gemini Output:** Returns:
   - Identified legal issue
   - Applicable Indian law
   - Recommended action steps
   - Related government helpline or contact

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

> **"I’m being harassed at work. What should I do?"**

✅ **Bot Output:**

- **Legal Issue:** Workplace harassment
- **Law:** Indian Penal Code, 1860 – Sec 354A
- **Steps:** File a complaint with Internal Committee or police
- **Helpline:** National Women Helpline – 1091

---

## 🆓 Why Gemini?

- ✅ Free to use with Google account
- ✅ Supports structured, JSON-style output
- ✅ No credit card required
- ✅ Easy to integrate with `google.generativeai` Python SDK

---

## 📄 File Structure

```
lawbot/
├── app.py                 # Streamlit app
├── lawbot_engine.py       # Core logic (RAG + prompt + function calling)
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
- Improve prompt design
- Add new legal document datasets
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

- `app.py` code that includes RAG + Gemini + function calling
- `.env.example` file
- Deployment instructions for **Streamlit Cloud** (for free hosting)

I'm happy to provide everything next.
```
