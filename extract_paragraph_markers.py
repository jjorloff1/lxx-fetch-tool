import json
import os
import re
from bs4 import BeautifulSoup

INPUT_FILE = "output_lxx/compiled_septuagint.html"
OUTPUT_FILE = "output_lxx/paragraph_markers.json"

def clean_greek_word(word):
    # Keep only Greek letters and combining marks (Unicode range)
    return ''.join(re.findall(r'[\u0370-\u03FF\u1F00-\u1FFF]+', word))

def extract_paragraph_markers():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    markers = []
    current_book = None
    current_chapter = None
    last_verse_seen = 0
    last_word_in_previous_paragraph = None
    index_from_last_verse = 0
    previous_paragraph_tag = None
    first_paragraph_seen = False
    

    for tag in soup.find_all(["h2", "h3", "p"]):
        if tag.name == "h2":
            current_book = tag.get_text(strip=True)
        elif tag.name == "h3":
            current_chapter = tag.get_text(strip=True)

            # Reset counters at beginning of a new chapter
            first_paragraph_seen = False
            previous_paragraph_tag = None
            index_from_last_verse = 0
            last_verse_seen = 0
        elif tag.name == "p":
            # Find the verse number from first <b> tag in this paragraph
            verse_tag = tag.find("b")
            verse_tags = tag.find_all("b")
            last_b_tag = verse_tags[-1] if verse_tags else None

            if verse_tag:
                verse_number_string = verse_tag.get_text(strip=True)
                last_verse_seen = last_b_tag.get_text(strip=True) if last_b_tag else None
                index_from_last_verse = 0
            else:
                verse_number_string = str(last_verse_seen)
                last_verse_word_count = extract_last_verse_word_count(previous_paragraph_tag)
                index_from_last_verse = index_from_last_verse + last_verse_word_count

            words = []
            for content in tag.stripped_strings:
                if not content.isdigit():
                    words.extend(content.split())

            if words:
                marker = {
                    "book": current_book,
                    "chapter": current_chapter,
                    "verse": str(verse_number_string), # Verse numbers sometimes have letters
                    "word_index": str(index_from_last_verse),
                    "prev_word": clean_greek_word(last_word_in_previous_paragraph) if last_word_in_previous_paragraph else None,
                    "next_word": clean_greek_word(words[0]) if words else None
                }
                markers.append(marker)

            last_word_in_previous_paragraph = words[-1]
            previous_paragraph_tag = tag
            first_paragraph_seen = True

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(markers, out, ensure_ascii=False, indent=2)

    print(f"✔ Paragraph marker data written to {OUTPUT_FILE}")

def extract_last_verse_word_count(tag):
    if not tag:
        return 0
    
    raw = str(tag)
    parts = raw.split("</b>")
    last_verse_raw = parts[-1].strip()
    last_verse_text = BeautifulSoup(last_verse_raw, "html.parser").get_text(strip=True)
    word_count = len(last_verse_text.split())
    return word_count

if __name__ == "__main__":
    extract_paragraph_markers()
