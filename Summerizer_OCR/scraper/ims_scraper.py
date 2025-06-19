import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re
import json

# Config
URL = "https://imsnsit.org/imsnsit/notifications.php"
CUTOFF_DATE = datetime.strptime("01-05-2025", "%d-%m-%Y")
HEADERS = {"User-Agent": "Mozilla/5.0"}
PDF_DIR = "./pdfs"
META_DIR = "./metadata"
META_FILE = os.path.join(META_DIR, "notices.json")

# Ensure directories exist
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

# Store all notice metadata
all_notices = []

# Fetch webpage
response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.content, "html.parser")

rows = soup.select("tr")
found = False

def slugify(text):
    """Simplifies text into safe filenames"""
    return re.sub(r'[^a-zA-Z0-9]+', '_', text.strip())[:50]

for row in rows:
    columns = row.find_all("td")
    if len(columns) < 2:
        continue

    raw_date_text = columns[0].get_text(strip=True)
    if not raw_date_text:
        continue

    try:
        raw_date = raw_date_text.split()[0]
        notice_date = datetime.strptime(raw_date, "%d-%m-%Y")
    except Exception:
        continue

    if notice_date >= CUTOFF_DATE:
        found = True
        subject = columns[1].get_text(" ", strip=True).split("Published")[0].strip()
        link_tag = columns[1].find("a")
        pdf_url = "https://imsnsit.org/imsnsit/" + link_tag["href"] if link_tag and link_tag.has_attr("href") else None

        print(f"📅 Date: {raw_date}")
        print(f"📌 Subject: {subject}")
        print(f"🔗 PDF URL: {pdf_url}" if pdf_url else "❌ No link")
        print("-" * 60)

        file_name = None

        # Download the PDF
        if pdf_url:
            try:
                file_name = f"{raw_date}_{slugify(subject)}.pdf"
                pdf_path = os.path.join(PDF_DIR, file_name)
                pdf_response = requests.get(pdf_url)
                with open(pdf_path, "wb") as f:
                    f.write(pdf_response.content)
                print(f"✅ Downloaded to {pdf_path}\n")
            except Exception as e:
                print(f"⚠️ Failed to download: {e}\n")

        # Save metadata
        notice_info = {
            "date": raw_date,
            "title": subject,
            "pdf_url": pdf_url,
            "saved_as": file_name
        }
        all_notices.append(notice_info)

# Save all metadata to JSON file
with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(all_notices, f, indent=2, ensure_ascii=False)

if not found:
    print("No notices found after", CUTOFF_DATE.strftime("%d-%m-%Y"))
else:
    print(f"\n📝 Saved {len(all_notices)} notices to {META_FILE}")
