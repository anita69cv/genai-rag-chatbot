from pypdf import PdfReader

def load_pdf(file):
    reader = PdfReader(file)
    documents = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            documents.append({
                "text": text,
                "page": i + 1
            })

    return documents