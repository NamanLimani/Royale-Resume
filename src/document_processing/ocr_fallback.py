import pytesseract
from pdf2image import convert_from_path

def extract_text_with_ocr(file_path : str):
    """
    Converts a PDF to images and extracts text using Tesseract OCR.
    """
    exctracted_text = ""
    try :
        # Convert each page of the PDF into a PIL image
        pages = convert_from_path(file_path)

        for page_number , page_image in enumerate(pages):
            # Run Tesseract on the image
            text = pytesseract.image_to_string(page_image)
            exctracted_text += f"\n--- Page {page_number + 1} ---\n{text}"

    except Exception as e :
        print(f"[Error] OCR failed for {file_path}: {e}")

    return exctracted_text.strip()