# Dura Itihas ra Sanskriti website

Files
- `index.html`  the website (do not put book content here)
- `data.json`   THE ONE FILE YOU EDIT: all book content
- `data.js`     generated from data.json; index.html loads this
- `images/`     photos used in the gallery
- `build.py` / `build.js`  convert data.json -> data.js (use either)

Workflow
1. Edit `data.json`
2. Run `python3 build.py`  (or `node build.js`). Add `--watch` to rebuild on every save.
3. Refresh `index.html` in the browser. No server needed.

If the build fails, it tells you the line or the missing field. The old data.js is kept.

data.json structure
- `book`: list of chapters `{n, title, pages, sections:[{title, page, paras:[{t:"text"} or {c:"caption"}]}]}`
- `extra.glossary`: `{w:"word", d:"meaning"}`; glossary words become tap-for-meaning links inside the text
- `extra.people`: `["name", "place", "contribution"]`
- `extra.genealogy`: list of text lines
- `gal`: photos `{p: book page, i: "images/photo-01.jpg", c: "caption"}`; add a photo by putting the file in images/ and adding an entry

Tips
- Keep it valid JSON: text in double quotes, commas between items, no comma after the last item.
- To add a topic, copy an existing section block inside a chapter.
