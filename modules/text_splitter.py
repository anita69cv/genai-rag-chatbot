from langchain_text_splitters import CharacterTextSplitter

def split_text(documents):
    splitter = CharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = []
    for doc in documents:
        split_chunks = splitter.split_text(doc["text"])
        for chunk in split_chunks:
            chunks.append({
                "text": chunk,
                "page": doc["page"]
            })

    return chunks