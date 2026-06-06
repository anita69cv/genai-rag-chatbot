from langchain_community.vectorstores import FAISS

def create_vector_store(chunks, embeddings):
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [{"page": chunk["page"]} for chunk in chunks]

    return FAISS.from_texts(texts, embeddings, metadatas=metadatas)