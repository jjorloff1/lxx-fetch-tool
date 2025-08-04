from collections import defaultdict
import os

input_path = "SRGNT - greekcntr.txt"
output_path = "output_nt/compiled_srgnt_nt.html"

# Book code to book name mapping (BB -> Name)
BOOKS = {
    "40": "Matthew", "41": "Mark", "42": "Luke", "43": "John",
    "44": "Acts", "45": "Romans", "46": "1 Corinthians", "47": "2 Corinthians",
    "48": "Galatians", "49": "Ephesians", "50": "Philippians", "51": "Colossians",
    "52": "1 Thessalonians", "53": "2 Thessalonians", "54": "1 Timothy", "55": "2 Timothy",
    "56": "Titus", "57": "Philemon", "58": "Hebrews", "59": "James",
    "60": "1 Peter", "61": "2 Peter", "62": "1 John", "63": "2 John",
    "64": "3 John", "65": "Jude", "66": "Revelation"
}

# Read and parse the file
with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

bible_structure = defaultdict(lambda: defaultdict(list))
current_paragraph = []
last_book, last_chapter = None, None

for line in lines:
    if len(line.strip()) < 9:
        continue
    ref = line[:8]
    text = line[9:].strip()
    book_code = ref[:2]
    chapter_num = int(ref[2:5])
    verse_num = int(ref[5:])

    if "¶" in text or (book_code != last_book or chapter_num != last_chapter):
        if current_paragraph and last_book and last_chapter:
            bible_structure[last_book][last_chapter].append(current_paragraph)
        current_paragraph = []

    text = text.replace("\u00b6", "").strip()
    verse_html = f"<b>{verse_num}</b> {text}"
    current_paragraph.append(verse_html)
    last_book, last_chapter = book_code, chapter_num

# Don't forget the last paragraph
if current_paragraph and last_book and last_chapter:
    bible_structure[last_book][last_chapter].append(current_paragraph)

# Create HTML content
html_parts = ['<h1>New Testament</h1>']
for book_code in sorted(bible_structure.keys(), key=lambda x: int(x)):
    book_name = BOOKS.get(book_code, f"Book {book_code}")
    html_parts.append(f"<h2>{book_name}</h2>")
    for chapter in sorted(bible_structure[book_code].keys()):
        html_parts.append(f"<h3>{chapter}</h3>")
        for paragraph in bible_structure[book_code][chapter]:
            paragraph_text = " ".join(paragraph)
            html_parts.append(f"<p>{paragraph_text}</p>")

# Make sure the output folder exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save the final HTML
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))
