from bs4 import BeautifulSoup

input_path = "bible.html"
output_path = "bible_styled.html"

with open(input_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

body = soup.body or soup
all_elements = list(body.children)

new_body = []
i = 0
found_first_p_of_book = False

while i < len(all_elements):
    el = all_elements[i]

    # Append anything that's not a tag (e.g., newlines)
    if not getattr(el, 'name', None):
        new_body.append(el)
        i += 1
        continue

    # Directly append <h1> or <h2>
    if el.name in ["h1", "h2"]:
        new_body.append(el)
        found_first_p_of_book = False
        i += 1
        continue

    # Handle each chapter block starting at <h3>
    if el.name == "h3":
        chapter_block = soup.new_tag("div", **{"class": "chapter-block"})
        chapter_block.append(el)

        chapter_content = soup.new_tag("div", **{"class": "chapter-content"})

        i += 1
        paragraph_index = 0
        while i < len(all_elements):
            next_el = all_elements[i]
            if getattr(next_el, 'name', None) in ["h2", "h3", "h1"]:
                break
            if getattr(next_el, 'name', None) == "p":
                if paragraph_index == 0 and found_first_p_of_book == False:
                    next_el['class'] = next_el.get('class', []) + ['dropcap']
                    found_first_p_of_book = True
                chapter_content.append(next_el)
                paragraph_index += 1
            else:
                chapter_content.append(next_el)
            i += 1

        chapter_block.append(chapter_content)
        new_body.append(chapter_block)
        continue

    # Append any unexpected tags
    new_body.append(el)
    i += 1

# Replace body with new structured content
body.clear()
for el in new_body:
    body.append(el)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(str(soup))
