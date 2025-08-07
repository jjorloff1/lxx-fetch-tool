import json
import os
from bs4 import BeautifulSoup

INPUT_FILE = "output_lxx/compiled_septuagint.html"
OUTPUT_FILE = "output_lxx/paragraph_markers.json"

def extract_paragraph_markers():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    markers = []
    current_book = None
    current_chapter = None
    last_verse_in_current_paragraph = None
    last_word_in_previous_paragraph = None
    first_paragraph_seen = False
    

    for tag in soup.find_all(["h2", "h3", "p"]):
        if tag.name == "h2":
            current_book = tag.get_text(strip=True)
        elif tag.name == "h3":
            current_chapter = tag.get_text(strip=True)
            first_paragraph_seen = False
        elif tag.name == "p":
            # Find the verse number from first <b> tag in this paragraph
            verse_tag = tag.find("b")
            verse_tags = tag.find_all("b")
            last_b_tag = verse_tags[-1] if verse_tags else None

            if verse_tag:
                verse_number = verse_tag.get_text(strip=True)
                last_verse_in_current_paragraph = last_b_tag.get_text(strip=True) if last_b_tag else None
            else:
                verse_number = last_verse_in_current_paragraph

            words = []
            for content in tag.stripped_strings:
                if not content.isdigit():
                    words.extend(content.split())

            if words:
                marker = {
                    "book": current_book,
                    "chapter": current_chapter,
                    "verse": verse_number,
                    "word_index": 0,
                    "prev_word": last_word_in_previous_paragraph,
                    "next_word": words[0] if words else None
                }
                markers.append(marker)

            last_word_in_previous_paragraph = words[-1]
            first_paragraph_seen = True

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(markers, out, ensure_ascii=False, indent=2)

    print(f"✔ Paragraph marker data written to {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_paragraph_markers()
