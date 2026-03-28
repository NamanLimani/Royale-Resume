import fitz
from src.document_processing.ocr_fallback import extract_text_with_ocr

def process_pdf(file_path : str , min_char : int = 100) -> str:
    """
    Attempts native text extraction. Falls back to OCR if text yield is too low.
    """
    text = ""
    try :
        # Open the document using PyMuPDF
        doc = fitz.open(file_path)

        for page in doc:
            text += page.get_text()

        doc.close()

        # Check if the extracted text is suspiciously short
        if len(text.strip()) < min_char :
            print(f"[Info] Low text yield in {file_path}. Triggering OCR Fallback")
            text = extract_text_with_ocr(file_path)
        else :
            print(f"[Info] Native Exctraction Successful for {file_path}")

    except Exception as e :
        print(f"[Error] Failed to process {file_path}")
    
    return text.strip()