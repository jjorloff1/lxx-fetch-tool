import json
import os
import re
import sys
from datetime import datetime

PARAGRAPH_JSON = "output_lxx/paragraph_markers.json"
INPUT_HTML = "output_lxx_1935/septuagint_from_tf.html"
OUTPUT_HTML = "output_lxx_1935/septuagint_with_paragraphs.html"
LOG_DIR = "output_lxx_1935/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"paragraph_warnings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def log_warning(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def load_paragraph_markers():
    with open(PARAGRAPH_JSON, encoding="utf-8") as f:
        return json.load(f)

def load_html():
    with open(INPUT_HTML, encoding="utf-8") as f:
        return f.read()

def save_html(html):
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

def insert_paragraphs(html, markers):
    title_re = re.compile(r'<h1[^>]*>(.*?)</h1>', re.UNICODE)
    book_re = re.compile(r'<h2[^>]*>(.*?)</h2>', re.UNICODE)
    chapter_re = re.compile(r'<h3[^>]*>(.*?)</h3>', re.UNICODE)
    p_re = re.compile(r'<p>(.*?)</p>', re.UNICODE | re.DOTALL)
    verse_re = re.compile(r'<b[^>]*>([\dA-Za-z]+)</b>', re.UNICODE)

    # Organize markers for quick lookup
    markers_by_book_chapter = {}
    for marker in markers:
        book = marker['book']
        chapter = str(marker['chapter'])
        markers_by_book_chapter.setdefault((book, chapter), []).append(marker)

    output_lines = []
    idx = 0
    lines = html.split('\n')
    while idx < len(lines):
        line = lines[idx]
        title_match = title_re.match(line)
        if title_match:
            output_lines.append(line)
            idx += 1
            continue
        
        book_match = book_re.match(line)
        if book_match:
            current_book = book_match.group(1).strip()
            output_lines.append(line)
            idx += 1
            continue
        
        chapter_match = chapter_re.match(line)
        if chapter_match:
            current_chapter = chapter_match.group(1).strip()
            output_lines.append(line)
            # Next line should be the <p> with chapter content
            idx += 1
            chapter_content_line = lines[idx]
            p_match = p_re.match(chapter_content_line)
            if not p_match:
                output_lines.append(chapter_content_line)
                idx += 1
                continue
            chapter_content = p_match.group(1)
            # Find all verse positions
            verse_spans = [m for m in verse_re.finditer(chapter_content)]
            # Build paragraph break positions from markers
            markers = markers_by_book_chapter.get((current_book, current_chapter), [])
            # Each marker: {'verse', 'word_index', ...}
            # Build a list of (start_idx, marker) for paragraph breaks
            paragraph_positions = []
            for marker in markers:
                verse = str(marker['verse'])
                word_index = int(marker['word_index'])
                # Find the verse position
                if verse == "0":
                    # Paragraph at start of chapter
                    paragraph_positions.append((0, marker))
                else:
                    # Find the corresponding <b> tag for the verse
                    verse_idx = None
                    for v_idx, v_match in enumerate(verse_spans):
                        if v_match.group(1) == verse:
                            verse_idx = v_match.start()
                            break
                    if verse_idx is None:
                        log_warning(f"Verse not found in chapter: {(current_book, current_chapter, verse)}")
                        continue
                    # Now, find the word position after the <b> tag
                    after_b = chapter_content[v_match.end():]
                    # Find all words (split by whitespace or tags)
                    word_matches = list(re.finditer(r'[^\s<]+', after_b))
                    if word_index == 0:
                        # Paragraph break before <b> tag
                        paragraph_positions.append((verse_idx, marker))
                    elif word_index <= len(word_matches):
                        # Paragraph break after the Nth word after the <b> tag
                        word_pos = word_matches[word_index].start() + v_match.end()
                        paragraph_positions.append((word_pos, marker))
                    else:
                        log_warning(f"word_index out of range in chapter: {(current_book, current_chapter, verse)} {marker}")
            # # Sort paragraph positions
            # paragraph_positions.sort()
            # Split chapter_content into paragraphs
            last_idx = 0
            paragraphs = []
            for pos, marker in paragraph_positions:
                if pos > last_idx:
                    para_text = chapter_content[last_idx:pos].strip()
                    if para_text:
                        paragraphs.append(para_text)
                last_idx = pos
            # Add the last paragraph
            para_text = chapter_content[last_idx:].strip()
            if para_text:
                paragraphs.append(para_text)
            # Output each paragraph as its own <p> block
            for para in paragraphs:
                output_lines.append(f"<p>{para}</p>")
            idx += 1
            continue
        # Default: copy line
        output_lines.append(line)
        idx += 1
    return '\n'.join(output_lines)

def main():
    markers = load_paragraph_markers()
    html = load_html()
    new_html = insert_paragraphs(html, markers)
    save_html(new_html)
    print(f"Done. Output written to {OUTPUT_HTML}")
    print(f"Warnings logged to {LOG_FILE}")

if __name__ == "__main__":
    main()