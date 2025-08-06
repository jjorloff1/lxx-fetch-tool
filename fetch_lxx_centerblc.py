from tf.fabric import Fabric
from pathlib import Path

TF_PATH = "/Users/jesse.orloff/Library/Mobile Documents/com~apple~CloudDocs/Documents/Code/bible-tools/LXX/tf/1935"
output_path = "septuagint_from_tf.html"

features = [
    "book", "chapter", "verse",
    "g_cons_utf8",  # Canonical Greek
    "otext", "otype", "oslots"
]

TF = Fabric(locations=TF_PATH)
api = TF.load(" ".join(features))

if not api:
    print("Failed to load Text-Fabric data.")
    exit(1)

F = api.F
T = api.T
L = api.L
N = api.N

# Book name mapping: code → [English name, Greek name]
book_name_mapping = {
    "Gen": ["Genesis", "Γένεσις"],
    "Exod": ["Exodus", "Ἔξοδος"],
    "Lev": ["Leviticus", "Λευιτικόν"],
    "Num": ["Numbers", "Ἀριθμοί"],
    "Deut": ["Deuteronomy", "Δευτερονόμιον"],
    "Josh": ["Joshua", "Ἰησοῦς"],
    "Judg": ["Judges", "Κριταί"],
    "Ruth": ["Ruth", "Ῥούθ"],
    "1Sam": ["1 Samuel", "Αʹ Βασιλειῶν"],
    "2Sam": ["2 Samuel", "Βʹ Βασιλειῶν"],
    "1Kgs": ["1 Kings", "Γʹ Βασιλειῶν"],
    "2Kgs": ["2 Kings", "Δʹ Βασιλειῶν"],
    "1Chr": ["1 Chronicles", "Αʹ Παραλειπομένων"],
    "2Chr": ["2 Chronicles", "Βʹ Παραλειπομένων"],
    "1Esdr": ["1 Esdras", "Ἔσδρας Αʹ"],
    "2Esdr": ["2 Esdras", "Ἔσδρας Βʹ / Νεεμίας"],
    "Esth": ["Esther", "Ἐσθήρ"],
    "Job": ["Job", "Ἰώβ"],
    "Ps": ["Psalms", "Ψαλμοί"],
    "Prov": ["Proverbs", "Παροιμίαι"],
    "Qoh": ["Ecclesiastes", "Ἐκκλησιαστής"],
    "Cant": ["Song of Songs", "ᾎσμα ᾀσμάτων"],
    "Wis": ["Wisdom of Solomon", "Σοφία Σολομῶντος"],
    "Sir": ["Sirach", "Σοφία Σειράχ"],
    "Isa": ["Isaiah", "Ἠσαΐας"],
    "Jer": ["Jeremiah", "Ἰερεμίας"],
    "Lam": ["Lamentations", "Θρῆνοι"],
    "EpJer": ["Epistle of Jeremiah", "Ἐπιστολὴ Ἰερεμίου"],
    "Bar": ["Baruch", "Βαρούχ"],
    "Ezek": ["Ezekiel", "Ἰεζεκιήλ"],
    "Dan": ["Daniel", "Δανιήλ"],
    "DanTh": ["Daniel (Theodotion)", "Δανιήλ (Θεοδοτίων)"],
    "Hos": ["Hosea", "Ὡσηέ"],
    "Joel": ["Joel", "Ἰωήλ"],
    "Amos": ["Amos", "Ἀμώς"],
    "Obad": ["Obadiah", "Ἀβδίου"],
    "Jonah": ["Jonah", "Ἰωνᾶς"],
    "Mic": ["Micah", "Μιχαίας"],
    "Nah": ["Nahum", "Ναούμ"],
    "Hab": ["Habakkuk", "Ἀμβακοὺμ"],
    "Zeph": ["Zephaniah", "Σοφονίας"],
    "Hag": ["Haggai", "Ἀγγαῖος"],
    "Zech": ["Zechariah", "Ζαχαρίας"],
    "Mal": ["Malachi", "Μαλαχίας"],
    "TobS": ["Tobit (Short)", "Τωβίτ (shorter)"],
    "TobBA": ["Tobit (Long)", "Τωβίτ (longer)"],
    "Jdt": ["Judith", "Ἰουδίθ"],
    "1Mac": ["1 Maccabees", "Αʹ Μακκαβαίων"],
    "2Mac": ["2 Maccabees", "Βʹ Μακκαβαίων"],
    "3Mac": ["3 Maccabees", "Γʹ Μακκαβαίων"],
    "4Mac": ["4 Maccabees", "Δʹ Μακκαβαίων"],
    "Sus": ["Susanna", "Σωσάννα"],
    "SusTh": ["Susanna (Theodotion)", "Σωσάννα (Θεοδοτίων)"],
    "Bel": ["Bel and the Dragon", "Βήλ καὶ Δράκων"],
    "BelTh": ["Bel (Theodotion)", "Βήλ (Θεοδοτίων)"],
    "PsSol": ["Psalms of Solomon", "Ψαλμοὶ Σολομῶντος"],
    "Od": ["Odes", "ᾨδαί"]
}

html = ['<h1>Septuagint</h1>\n']

current_book = ""
current_chapter = ""
current_verse = ""

for word_node in F.otype.s("word"):
    book = F.book.v(word_node)
    chapter = F.chapter.v(word_node)
    verse = F.verse.v(word_node)

    # Detect new book
    if book != current_book:
        current_book = book
        if current_chapter != "":
            html.append(f"</p>\n")
        current_chapter = ""
        english_name, greek_name = book_name_mapping.get(book, [book, book])
        book_title = f"{greek_name} ({english_name})"
        html.append(f"<h2>{book_title}</h2>\n")

    # Detect new chapter
    if chapter != current_chapter:
        if current_verse != "" and current_chapter != "":
            html.append(f"</p>\n")
        current_chapter = chapter
        html.append(f"<h3>{chapter}</h3>\n")
        current_verse = ""

    # Detect new verse
    if verse != current_verse:
        if current_verse == "":
            html.append(f"<p>")
        current_verse = verse
        html.append(f" <b>{verse}</b> ")

    # Add the word
    word_text = F.word.v(word_node) or ""
    html.append(word_text + " ")

# Output the result
with open(output_path, "w", encoding="utf-8") as f:
    f.write("".join(html))

print(f"Written: {output_path}")
