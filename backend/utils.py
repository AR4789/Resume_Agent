from pypdf import PdfReader
import io

def read_pdf(bytes_data):
    reader = PdfReader(io.BytesIO(bytes_data))
    text_parts = []

    for page in reader.pages:
        if page.extract_text():
            text_parts.append(page.extract_text())

    return "\n".join(text_parts)


def read_docx(bytes_data):
    from docx import Document
    import io

    doc = Document(io.BytesIO(bytes_data))
    return "\n".join(p.text for p in doc.paragraphs)
