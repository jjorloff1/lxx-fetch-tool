import os
import time
import requests
import re
from bs4 import BeautifulSoup

# Book metadata: (code, name, number of chapters)
BOOKS = [
    # Old Testament and Deuterocanon
    ("GEN", "Genesis", 50), ("EXO", "Exodus", 40), ("LEV", "Leviticus", 27), ("NUM", "Numbers", 36), ("DEU", "Deuteronomy", 34),
    ("JOS", "Joshua", 24), ("JDG", "Judges", 21), ("RUT", "Ruth", 4), ("1SA", "1 Samuel", 31), ("2SA", "2 Samuel", 24),
    ("1KI", "1 Kings", 22), ("2KI", "2 Kings", 25), ("1CH", "1 Chronicles", 29), ("2CH", "2 Chronicles", 36), 
    ("1ES", "1 Esdras", 9), ("EZR", "Ezra - Nehemiah", 23), ("EST", "Esther", 16), ("ESA", "Esther With Additons", 10),
    ("JDT", "Judith", 16), ("TOB", "Tobit", 14), ("1MA", "1 Maccabees", 16), ("2MA", "2 Maccabees", 15), ("3MA", "3 Maccabees", 7), 
    ("4MA", "4 Maccabees", 18), 
    ("PSA", "Psalms", 151), ("PRO", "Proverbs", 31), ("ECC", "Ecclesiastes", 12), ("SNG", "Song of Solomon", 8), ("JOB", "Job", 42), 
    ("WIS", "Wisdom", 19), ("SIR", "Sirach", 51), ("PSS", "Psalms of Solomon", 18), ("HOS", "Hosea", 14),
    ("AMO", "Amos", 9), ("MIC", "Micah", 7), ("JOL", "Joel", 3), ("OBA", "Obadiah", 1), ("JON", "Jonah", 4), ("NAM", "Nahum", 3),
    ("HAB", "Habakkuk", 3), ("ZEP", "Zephaniah", 3), ("HAG", "Haggai", 2), ("ZEC", "Zechariah", 14), ("MAL", "Malachi", 4),
    ("ISA", "Isaiah", 66), ("JER", "Jeremiah", 52), ("BAR", "Baruch", 6), ("LAM", "Lamentations", 5), ("LJE", "Epistle of Jeremiah", 1),
    ("EZK", "Ezekiel", 48), ("SUS", "Susanna", 1), ("DAN", "Daniel", 14), ("BEL", "Bel and the Dragon", 1), ("ODA", "Odes", 14)
    
    # New Testament
    # ("MAT", "Matthew", 28), ("MRK", "Mark", 16), ("LUK", "Luke", 24), ("JHN", "John", 21),
    # ("ACT", "Acts", 28), ("ROM", "Romans", 16), ("1CO", "1 Corinthians", 16), ("2CO", "2 Corinthians", 13),
    # ("GAL", "Galatians", 6), ("EPH", "Ephesians", 6), ("PHP", "Philippians", 4), ("COL", "Colossians", 4),
    # ("1TH", "1 Thessalonians", 5), ("2TH", "2 Thessalonians", 3), ("1TI", "1 Timothy", 6), ("2TI", "2 Timothy", 4),
    # ("TIT", "Titus", 3), ("PHM", "Philemon", 1), ("HEB", "Hebrews", 13), ("JAS", "James", 5),
    # ("1PE", "1 Peter", 5), ("2PE", "2 Peter", 3), ("1JN", "1 John", 5), ("2JN", "2 John", 1),
    # ("3JN", "3 John", 1), ("JUD", "Jude", 1), ("REV", "Revelation", 22)
]

BASE_URL = "https://www.die-bibel.de/en/bible/LXX/{book}.{chapter}"
SAVE_ROOT = "output_lxx"

def bold_unwrapped_numbers(text):
    pattern = re.compile(r'\s?(\d+[a-z]?)\s?')

    if isinstance(text, list):
        return [pattern.sub(r' <b>\1</b>', item) for item in text]
    elif isinstance(text, str):
        return pattern.sub(r' <b>\1</b>', text)
    else:
        raise TypeError("Expected a string or list of strings")

def fetch_chapter_html(book_code, chapter_num):
    url = BASE_URL.format(book=book_code, chapter=chapter_num)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"  ❌ HTTP {response.status_code} for {url}")
    except Exception as e:
        print(f"  ❌ Error fetching {url}: {e}")
    return None

def extract_text_cleaned(html):
    """Strips all HTML tags and whitespace from a given HTML string"""
    soup = BeautifulSoup(html, "html.parser")
    return ''.join(soup.stripped_strings)

def extract_chapter_content(html):
    soup = BeautifulSoup(html, "html.parser")
    content = []
    for bp in soup.find_all(["ibep-bible-passage"]): # ["bible-p", "bible-q", "bible-m", "bible-d", "ibep-bible-passage"]):
        content.append(f"<p>{bp.get_text(strip=True)}</p>")
    return content if content else None

#     consider checking size against ibep-render-bible-content to see if they match


def save_chapter(book_name, chapter_num, paragraphs):
    folder = os.path.join(SAVE_ROOT, book_name)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"chapter_{chapter_num}.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(paragraphs))


def already_downloaded(book_name, chapter_num):
    return os.path.exists(os.path.join(SAVE_ROOT, book_name, f"chapter_{chapter_num}.html"))


def main():
    for book_code, book_name, total_chapters in BOOKS:
        for chapter in range(1, total_chapters + 1):
            if already_downloaded(book_name, chapter):
                print(f"⏩ Skipping {book_name} {chapter} (already downloaded)")
                continue

            print(f"Fetching: {book_code} {chapter} → {BASE_URL.format(book=book_code, chapter=chapter)}")
            html = fetch_chapter_html(book_code, chapter)
            if not html:
                continue

            content = extract_chapter_content(html)

            # After fetching and parsing the page

            soup = BeautifulSoup(html, "html.parser")
            original_div = soup.find("ibep-render-bible-content")
            original_clean = extract_text_cleaned(str(original_div))
            built_clean = extract_text_cleaned(''.join(content))

            if original_clean != built_clean:
                print(f"⚠️ WARNING: Content mismatch in {book_name} {chapter}")

            content = extract_chapter_content(html)
            verse_b_content = bold_unwrapped_numbers(content)
            if verse_b_content:
                save_chapter(book_name, chapter, verse_b_content)
                print(f"  ✅ Saved {book_name} {chapter}")
            else:
                print(f"  ⚠️ No content found for {book_name} {chapter}")


if __name__ == "__main__":
    main()
