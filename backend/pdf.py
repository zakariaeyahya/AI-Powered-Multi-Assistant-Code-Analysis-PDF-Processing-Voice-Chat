from PyPDF2 import PdfReader
import logging
import os

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path):
    if not os.path.isfile(pdf_path):
        logger.error(f"File not found: {pdf_path}")
        return ""
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            return "\n".join(page.extract_text() for page in reader.pages)
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return ""

def get_pdf_metadata(pdf_path):
    if not os.path.isfile(pdf_path):
        logger.error(f"File not found: {pdf_path}")
        return {}
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            return reader.metadata
    except Exception as e:
        logger.error(f"Error getting PDF metadata: {e}")
        return {}

def count_pages(pdf_path):
    if not os.path.isfile(pdf_path):
        logger.error(f"File not found: {pdf_path}")
        return 0
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            return len(reader.pages)
    except Exception as e:
        logger.error(f"Error counting PDF pages: {e}")
        return 0