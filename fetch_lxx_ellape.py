import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Book metadata: (code, name, number of chapters)
BOOKS = [
    # Old Testament and Deuterocanon
    ("GEN", "Genesis", 50), ("EXO", "Exodus", 40), ("LEV", "Leviticus", 27), ("NUM", "Numbers", 36), ("DEU", "Deuteronomy", 34),
    ("JOS", "Joshua", 24), ("JDG", "Judges", 21), ("RUT", "Ruth", 4), ("1SA", "1 Samuel", 31), ("2SA", "2 Samuel", 24),
    ("1KI", "1 Kings", 22), ("2KI", "2 Kings", 25), ("1CH", "1 Chronicles", 29), ("2CH", "2 Chronicles", 36),
    ("1ES", "1 Esdras", 10), ("2ES", "2 Esdras", 10), ("NEH", "Nehemiah", 13),
    ("TOB", "Tobit", 14), ("JDT", "Judith", 16), ("EST", "Esther", 16), ("1MA", "1 Maccabees", 16),
    ("2MA", "2 Maccabees", 15), ("3MA", "3 Maccabees", 7),
    ("PSA", "Psalms", 150), ("PS2", "Psalms", 151), ("JOB", "Job", 42), ("PRO", "Proverbs", 31), ("ECC", "Ecclesiastes", 12),
    ("SNG", "Song of Solomon", 8), ("WIS", "Wisdom", 19), ("SIR", "Sirach", 51),
    ("HOS", "Hosea", 14), ("AMO", "Amos", 9),
    ("MIC", "Micah", 7), ("JOL", "Joel", 3), ("OBA", "Obadiah", 1),
    ("JON", "Jonah", 4), ("NAM", "Nahum", 3),
    ("HAB", "Habakkuk", 3), ("ZEP", "Zephaniah", 3), ("HAG", "Haggai", 2), ("ZEC", "Zechariah", 14), ("MAL", "Malachi", 4),
    ("ISA", "Isaiah", 66), ("JER", "Jeremiah", 52), ("BAR", "Baruch", 6), ("LAM", "Lamentations", 5), ("EZK", "Ezekiel", 48),
    ("DAN", "Daniel", 14), ("4MA", "4 Maccabees", 18),

    # New Testament
    ("MAT", "Matthew", 28), ("MRK", "Mark", 16), ("LUK", "Luke", 24), ("JHN", "John", 21),
    ("ACT", "Acts", 28), ("ROM", "Romans", 16), ("1CO", "1 Corinthians", 16), ("2CO", "2 Corinthians", 13),
    ("GAL", "Galatians", 6), ("EPH", "Ephesians", 6), ("PHP", "Philippians", 4), ("COL", "Colossians", 4),
    ("1TH", "1 Thessalonians", 5), ("2TH", "2 Thessalonians", 3), ("1TI", "1 Timothy", 6), ("2TI", "2 Timothy", 4),
    ("TIT", "Titus", 3), ("PHM", "Philemon", 1), ("HEB", "Hebrews", 13), ("JAS", "James", 5),
    ("1PE", "1 Peter", 5), ("2PE", "2 Peter", 3), ("1JN", "1 John", 5), ("2JN", "2 John", 1),
    ("3JN", "3 John", 1), ("JUD", "Jude", 1), ("REV", "Revelation", 22)
]

BASE_URL = "https://live.bible.is/bible/ELLAPE/{book}/{chapter}"
SAVE_ROOT = "output_patriarchal_text"


def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    return driver


def fetch_chapter_html_selenium(driver, book_code, chapter_num):
    url = BASE_URL.format(book=book_code, chapter=chapter_num)
    try:
        driver.get(url)
        time.sleep(2)  # allow time for JS to render
        return driver.page_source
    except Exception as e:
        print(f"  ❌ Error fetching {book_code} {chapter_num}: {e}")
        return None


def extract_chapter_content(html):
    soup = BeautifulSoup(html, "html.parser")
    chapter_div = soup.select_one("div.chapter.section")
    if not chapter_div:
        return None

    paragraphs = []
    for p in chapter_div.find_all("p"):
        spans = []
        for span in p.find_all("span"):
            classes = span.get("class", [])
            if any("v-num" in cls for cls in classes):
                spans.append(f"<b>{span.get_text(strip=True)}</b>")
            elif any(cls.startswith("v") or cls.startswith("GEN") for cls in classes):
                spans.append(span.get_text(strip=True))
        if spans:
            paragraphs.append("<p>" + " ".join(spans) + "</p>")

    return paragraphs if paragraphs else None


def save_chapter(book_name, chapter_num, paragraphs):
    folder = os.path.join(SAVE_ROOT, book_name)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"chapter_{chapter_num}.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(paragraphs))


def already_downloaded(book_name, chapter_num):
    return os.path.exists(os.path.join(SAVE_ROOT, book_name, f"chapter_{chapter_num}.html"))


def main():
    driver = setup_driver()
    try:
        for book_code, book_name, total_chapters in BOOKS:
            for chapter in range(1, total_chapters + 1):
                if already_downloaded(book_name, chapter):
                    print(f"⏩ Skipping {book_name} {chapter} (already downloaded)")
                    continue

                print(f"Fetching: {book_code} {chapter} → {BASE_URL.format(book=book_code, chapter=chapter)}")
                html = fetch_chapter_html_selenium(driver, book_code, chapter)
                if not html:
                    continue

                content = extract_chapter_content(html)
                if content:
                    save_chapter(book_name, chapter, content)
                    print(f"  ✅ Saved {book_name} {chapter}")
                else:
                    print(f"  ⚠️ No content found for {book_name} {chapter}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
