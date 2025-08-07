# LXX Fetch Tool
### To Do
[] Get the the Prayer of Mannasah
[] Add NT In with similar details
    [x] SRGNT
    [] SBLGNT
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
        We need a new source for punctuation.
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

To Read:
[] https://pagedjs.org/en/documentation/7-generated-content-in-margin-boxes/

