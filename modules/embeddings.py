import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )