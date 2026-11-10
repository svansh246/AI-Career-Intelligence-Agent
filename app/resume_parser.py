import io
from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file):
    pdf_reader = PdfReader(io.BytesIO(file.read()))

    text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_docx(file):
    document = Document(io.BytesIO(file.read()))

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_text_from_txt(file):
    return file.read().decode("utf-8")


def extract_resume_text(file):

    file_type = file.name.lower()

    if file_type.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif file_type.endswith(".docx"):
        return extract_text_from_docx(file)

    elif file_type.endswith(".txt"):
        return extract_text_from_txt(file)

    else:
        return "Unsupported file format."