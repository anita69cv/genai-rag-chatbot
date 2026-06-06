# 🧠 Local AI RAG Chatbot

A local GenAI-powered chatbot that allows users to upload PDFs, ask questions about documents, generate summaries, search content, and chat with an AI model running locally through LM Studio.

## 🚀 Features

### Basic Features

* PDF Upload
* Question Answering on PDFs
* Chat Interface
* Local AI using LM Studio

### Intermediate Features

* Chat History
* Multiple PDF Upload Support
* Source Citations

### Advanced Features

* Explain Like I'm 5 Mode
* Notes Summarizer
* Keyword Search
* Dark Mode UI

---

## 🛠 Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & RAG

* LM Studio
* Gemma 3 1B
* LangChain
* FAISS
* HuggingFace Embeddings

### Document Processing

* PyPDF

---

## 📂 Project Structure

genai-rag-assistant/

├── app.py

├── modules/

│   ├── pdf_loader.py

│   ├── text_splitter.py

│   ├── embeddings.py

│   └── vector_store.py

├── requirements.txt

├── README.md

└── .gitignore

---

## ⚙️ Installation

Install dependencies:

pip install streamlit

pip install openai

pip install pypdf

pip install langchain

pip install langchain-community

pip install langchain-text-splitters

pip install sentence-transformers

pip install faiss-cpu

---

## ▶️ Running the Application

1. Start LM Studio
2. Load Gemma 3 1B model
3. Start Local Server
4. Run:

streamlit run app.py

5. Open:

http://localhost:8501

---

## 📖 How It Works

1. Upload one or more PDF documents.
2. Text is extracted using PyPDF.
3. Documents are split into chunks.
4. Chunks are converted into embeddings.
5. FAISS stores embeddings for semantic search.
6. Relevant chunks are retrieved during user queries.
7. Context is sent to the local LLM via LM Studio.
8. AI generates answers based on document content.

---

## 🎯 Learning Outcomes

* Retrieval-Augmented Generation (RAG)
* Vector Databases (FAISS)
* Embeddings
* Local LLM Deployment
* Streamlit UI Development
* Prompt Engineering
* Document Question Answering

---

## 🔮 Future Improvements
* SQL Database Integration
* Persistent Chat Memory
* Export Chat as PDF
* User Authentication
* Cloud Deployment
* Multi-Model Support
---

## 👨‍💻 Author
Anita Vishwakarma
Master's Student in Computer Science
Interested in Generative AI, LLMs, RAG Systems, and Machine Learning.
