from pdf2image import convert_from_path
import pytesseract
import pdfplumber

from summarizer import summarize_text  # ✅ Make sure file is named summarizer.py

def extract_text_from_pdf(pdf_path):
    text = ""

    # Step 1: Try normal PDF text extraction
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Step 2: If nothing was extracted, try OCR
    if not text.strip():
        print("No text found — using OCR...")
        images = convert_from_path(pdf_path)
        for img in images:
            ocr_text = pytesseract.image_to_string(img, lang='eng')
            text += ocr_text + "\n"

    return text

if __name__ == "__main__":
    path = "Seema_devi.pdf"  
    full_text = extract_text_from_pdf(path)   # ✅ use full_text now

    print("📄 Full Text:\n", full_text)

    summary = summarize_text(full_text)

    print("\n🧠 Summary:\n", summary)

