import os
import json
from ocr_extractor import extract_text_from_pdf
from summarizer import summarize_text

PDF_DIR = "./scraper/pdfs"
META_INPUT = "./scraper/metadata/notices.json"
META_OUTPUT = "./scraper/metadata/processed_notices.json"

# Load metadata
with open(META_INPUT, "r", encoding="utf-8") as f:
    notices = json.load(f)

processed = []

for notice in notices:
    pdf_file = notice.get("saved_as")
    if not pdf_file:
        continue

    pdf_path = os.path.join(PDF_DIR, pdf_file)
    if not os.path.exists(pdf_path):
        print(f"❌ Missing file: {pdf_path}")
        continue

    print(f"📄 Processing: {pdf_file}")
    full_text = extract_text_from_pdf(pdf_path)

    if not full_text.strip():
        print("⚠️ No text extracted.")
        continue

    summary = summarize_text(full_text)
    notice["full_text"] = full_text
    notice["summary"] = summary

    processed.append(notice)
    print(f"✅ Summary added for: {pdf_file}")
    print("-" * 60)

# Save new JSON
with open(META_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(processed, f, indent=2, ensure_ascii=False)

print(f"\n🎉 Processing complete. Saved {len(processed)} notices to {META_OUTPUT}")
