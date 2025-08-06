import os

# Book metadata: (code, name, number of chapters)
BOOKS = [
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
    ("DAN", "Daniel", 14), ("4MA", "4 Maccabees", 18)
]

OUTPUT_DIR = "output_patriarchal_text"
OUTPUT_FILE = "compiled_patr_septuagint.html"

def merge_chapters():
    merged = ["<h1>Septuagint</h1>"]

    for code, book_name, chapters in BOOKS:
        book_dir = os.path.join(OUTPUT_DIR, book_name)
        if not os.path.isdir(book_dir):
            print(f"⚠️ Missing directory: {book_dir}")
            continue

        merged.append(f"<h2>{book_name}</h2>")

        for chapter_num in range(1, chapters + 1):
            chapter_file = os.path.join(book_dir, f"chapter_{chapter_num}.html")
            if not os.path.exists(chapter_file):
                print(f"⚠️ Missing file: {chapter_file}")
                continue

            with open(chapter_file, "r", encoding="utf-8") as f:
                chapter_content = f.read()

            merged.append(f"<h3>{chapter_num}</h3>")
            merged.append(chapter_content.strip())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("\n".join(merged))

    print(f"✅ Merged output written to {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_chapters()
