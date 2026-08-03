# 🤖 PragyanAI Intelligent Assistant

An AI-powered RAG (Retrieval-Augmented Generation) chatbot built with **Streamlit**, **LangChain**, **Groq Llama 3.3**, **FAISS**, and **HuggingFace Embeddings**. The chatbot answers questions about the PragyanAI AI/GenAI program using information retrieved from uploaded PDF and Excel documents.

---

## 🚀 Features

* 🤖 AI-powered conversational assistant
* 📚 Retrieval-Augmented Generation (RAG)
* 📄 Upload PDF documents
* 📊 Upload Excel (.xlsx/.xls) files
* 🧠 Conversation memory using LangChain
* 🎭 Multiple AI personas
* ⚡ Groq Llama 3.3 70B integration
* 🔍 FAISS Vector Database
* 📈 HuggingFace Embeddings (MiniLM)
* 💬 ChatGPT-style Streamlit interface
* ☁️ Ready for Streamlit Community Cloud deployment

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* LangChain Groq
* FAISS
* HuggingFace Embeddings
* PyPDF
* Pandas

---

## 📂 Project Structure

```
pragyan-ai-chatbot/
│
├── app.py
├── requirements.txt
├── pragyan_faq_prices.xlsx
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/pragyan-ai-chatbot.git
```

Move into the project folder:

```bash
cd pragyan-ai-chatbot
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure Groq API Key

Create the following file:

```
.streamlit/secrets.toml
```

Add your Groq API key:

```toml
GROQ_API="YOUR_GROQ_API_KEY"
```

> **Do not commit your actual API key to GitHub.** The repository includes only `secrets.toml.example` as a template.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## 📄 Supported File Types

* PDF
* Excel (.xlsx)
* Excel (.xls)

Uploaded documents are indexed into a FAISS vector database for semantic search and retrieval.

---

## 🎭 Available Personas

* PragyanAI Student Counselor
* PragyanAI Institutional Advisor
* PragyanAI Enterprise Lead

Each persona uses a different system prompt while answering questions from the same knowledge base.

---

## 📚 Knowledge Base

The chatbot automatically loads:

* `pragyan_faq_prices.xlsx`

Users can also upload additional PDF and Excel files to extend the knowledge base dynamically.

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push the project to GitHub.
2. Create a new app on Streamlit Community Cloud.
3. Select your GitHub repository.
4. Set `app.py` as the main file.
5. Add your Groq API key in **App Settings → Secrets**:

```toml
GROQ_API="YOUR_GROQ_API_KEY"
```

6. Deploy the application.

---

## 📌 Future Improvements

* Source citations for retrieved answers
* Multi-document chunking
* Hybrid Search (BM25 + FAISS)
* Conversation export
* Admin dashboard
* Authentication
* Usage analytics

---

## 👨‍💻 Author

Developed as an AI-powered conversational assistant for the PragyanAI AI/GenAI Program using Streamlit, LangChain, Groq, and FAISS.
