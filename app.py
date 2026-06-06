from modules.text_splitter import split_text
from modules.embeddings import get_embeddings
from modules.vector_store import create_vector_store
from modules.pdf_loader import load_pdf

import streamlit as st
from openai import OpenAI

# LM Studio client
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

st.title("🧠 My Local AI RAG Chatbot")

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.title("⚙️ Options")

simple_mode = st.sidebar.checkbox("Explain like I'm 5 🧠")
summarize = st.sidebar.button("Summarize Notes 📄")
dark_mode = st.sidebar.checkbox("Dark Mode 🌙")

# 🔎 Search Feature
search_query = st.sidebar.text_input("Search in documents 🔎")

# -------------------------------
# 🌙 Dark / ☀️ Light Mode (FINAL FIX)
# -------------------------------
if dark_mode:
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }

        section[data-testid="stSidebar"] {
            background-color: #111827;
        }

        /* Fix ALL text */
        label, .stMarkdown, .stText, .stSubheader, .stHeader {
            color: white !important;
        }

        section[data-testid="stSidebar"] * {
            color: white !important;
        }

        /* File uploader */
        .stFileUploader label {
            color: white !important;
        }

        /* Chat input */
        .stChatInput textarea {
            background-color: #1f2937 !important;
            color: white !important;
        }

        /* Buttons */
        button {
            background-color: #374151 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <style>
        .stApp {
            background-color: white;
            color: black;
        }

        section[data-testid="stSidebar"] {
            background-color: #f0f2f6;
        }

        .stChatInput textarea {
            background-color: white !important;
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)

# -------------------------------
# Session State Init
# -------------------------------
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Multiple PDF Upload + Processing
# -------------------------------
uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:

    new_files = [f for f in uploaded_files if f.name not in st.session_state.processed_files]

    if new_files:
        with st.spinner("Processing PDFs... please wait ⏳"):
            all_chunks = []
            embeddings = get_embeddings()

            for file in new_files:
                documents = load_pdf(file)
                chunks = split_text(documents)
                all_chunks.extend(chunks)

                st.session_state.processed_files.append(file.name)

            vector_store = create_vector_store(all_chunks, embeddings)
            st.session_state.vector_store = vector_store

        st.success("PDFs processed successfully!")

    else:
        st.info("All PDFs already processed ✅")

    st.subheader("Uploaded Files:")
    for f in uploaded_files:
        st.write(f.name)

# -------------------------------
# 🔎 Search Results
# -------------------------------
if search_query and "vector_store" in st.session_state:
    docs = st.session_state.vector_store.similarity_search(search_query, k=3)

    st.subheader("🔎 Search Results:")
    for d in docs:
        st.write(d.page_content[:200])

# -------------------------------
# 📄 Summarizer
# -------------------------------
if summarize and "vector_store" in st.session_state:

    with st.spinner("Summarizing documents... ⏳"):
        docs = st.session_state.vector_store.similarity_search("Summarize the document", k=5)

        context = "\n".join([doc.page_content for doc in docs])

        summary_prompt = f"""
        Summarize the following content clearly:

        {context}
        """

        response = client.chat.completions.create(
            model="local-model",
            messages=[{"role": "user", "content": summary_prompt}]
        )

        summary = response.choices[0].message.content

        st.subheader("📄 Summary:")
        st.write(summary)

# -------------------------------
# Chat History
# -------------------------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------------
# Chat Input
# -------------------------------
user_input = st.chat_input("Ask something about your PDFs...")

if user_input:

    if "vector_store" not in st.session_state:
        st.warning("Please upload PDFs first 📄")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})

        docs = st.session_state.vector_store.similarity_search(user_input, k=3)

        context = "\n".join([doc.page_content for doc in docs])
        sources = [doc.metadata.get("page") for doc in docs]

        style_instruction = ""
        if simple_mode:
            style_instruction = "Explain in very simple terms like teaching a 5-year-old."

        prompt = f"""
        Answer the question based on the context below.
        {style_instruction}
        If the answer is not in the context, say "I don't know".

        Context:
        {context}

        Question:
        {user_input}
        """

        response = client.chat.completions.create(
            model="local-model",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": reply})

        st.chat_message("assistant").write(reply)

        if sources:
            st.markdown("**Sources:** " + ", ".join([f"Page {p}" for p in sources]))


            ## streamlit run app.py