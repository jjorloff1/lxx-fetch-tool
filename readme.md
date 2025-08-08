# LXX Fetch Tool
### To Do
[] Get the the Prayer of Mannasah
[] Add NT In with similar details
    [x] SRGNT
    [] [SBLGNT](https://github.com/LogosBible/SBLGNT/tree/master/data/sblgnt/xml)
    [] [OpenGNT](https://github.com/eliranwong/OpenGNT/tree/master)
[] Style for printing
    [] superscript verses? Hide Verses alltogether for a reader edition? <-- This may be ideal
    [] Get good font style
    [] Can I style this like my ESV Reader (small chapters in margin, no verse numbers) https://static.crossway.org/excerpts/media/47640b07c065dc17557f63ddcd9605c03f0fe182/Readers_Bible_.pdf
    [] Header and Footer references
    [] Table of Contents
[] Replace English titles with Greek titles.
[x] Remove the ˚ character from SRGNT
[] use pagedjs https://pagedjs.org/en/documentation/2-getting-started-with-paged.js/
[] Variants to consider based on version
    [] Ending of Mark (probably include SBLGNT endings)
    [] Woman in adultry John 8:3-11
    [] LXX Include masoretic numbering with Psalms
[] Bugs
    [] See end of gen 1, does it have a period?  Do we need to generate periods?  Apparently there are no punctuation marks at all.
        We need a new source for punctuation. (https://github.com/LukeSmithxyz/grb/tree/master)
    [x] Match Titles between paragraph markers and LXX file:
        markers_by_book_chapter.get((current_book, current_chapter), [])
        []
        current_book
        'Γένεσις (Genesis)'
    [] index on multi paragraph verses is not matching in the insertion script.
`pagedjs-cli index.html -o result.pdf`
[] Rahlf 1935
    [] Get Paragraphing
    [] Transform by adding other styles
    [] Get Proper noun diacritical marks

To Read:
[] https://pagedjs.org/en/documentation/7-generated-content-in-margin-boxes/

Rahlf Sources:
* https://github.com/LukeSmithxyz/grb/tree/master
* https://github.com/dmartintucker/koine-greek-corpus/tree/master/koine-greek-texts # no punctuation, but has a lot of other texts too

Swete Sources:
* https://github.com/OpenGreekAndLatin/septuagint-dev/tree/master

Brenton: 
* https://github.com/mrgreekgeek/Brenton-LXX-Latex-print-project?tab=readme-ov-file
    * This may be a better base.  But note typo: ΠΑΡΟΙΜΙΑΙ ΕΑΛΩΜΩΝΤΟΣ P 558 and in TOC



# Other Resources
* https://github.com/biblenerd/awesome-bible-developer-resources?tab=readme-ov-file
* https://github.com/honza/greek-reader
* https://github.com/search?q=sblgnt+latex&type=code&p=1

