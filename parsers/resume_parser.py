import os
import pdfplumber
from docx import Document

def extract_text_from_pdf(file_path):
    """
    Opens a PDF and returns all its text as a single string.
    """
    full_text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
            else:
                pass
    if not full_text:
        return "No text found in the PDF."

    return full_text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = ""
    for paragraph in doc.paragraphs:
        if paragraph.text:
            full_text += paragraph.text + "\n"
    if full_text == "":
        return "No text found in the DOCX file."
    return full_text

def extract_resume_text(file_path):
    # check the file extension
    _, ext = os.path.splitext(file_path)
    if ext.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext.lower() == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")
    
if __name__ == "__main__":
    text = extract_resume_text(r"C:\Users\basil\OneDrive\Documents\personal docs\BasilAnil_Resume.docx")
    print(text)