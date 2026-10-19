"""
utils/pdf_parser.py
--------------------
Handles extracting raw text from an uploaded PDF resume using pdfplumber.
"""

import pdfplumber


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extracts and returns all text content from a PDF file.

    Parameters
    ----------
    uploaded_file : UploadedFile (from Streamlit's file_uploader)

    Returns
    -------
    str : concatenated text from all pages of the PDF
    """
    full_text = ""
    try:
        # pdfplumber can read directly from a file-like object
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # some pages might be empty/images
                    full_text += page_text + "\n"
    except Exception as e:
        # Return an error message so the UI can display it gracefully
        return f"ERROR: Could not read PDF. Details: {e}"

    return full_text.strip()
