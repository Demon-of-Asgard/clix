### TODO

---

- [ ] Load id search from arxiv
- [ ] **Add and remove categories and sub-categories**
- [ ] **Add tagging and starring favorite entries**
- [ ] **Connect to SQL database**

### DOING

---

- [ ] The query seems to be returning all the submissions relared to sub-category, even cross referenced ones.
      Try to order them in sub-categories.

  - [ ] Show sub-category choice first.
  - [ ] categorize and show the cross-referenced submissions later.

- [ ] Refactoring the code base --> Moving to separate Classes --> on branch dev_ref
  - [ ] Create renderer.py to handle all the rendering.
    - [x] Moved render_cat_and_subcat from main.py
    - [x] Moved manage_and_render_query_and_selection from main.py
    - [ ] Move render_parsed_response from ArXapi to renderer.py
  - [ ] Created parse_kbd_cmd.py
    - [x] Move kbd instructions parsing for category renderring from main.py
    - [ ] Move kbd instructions parsing item selection

### DONE

---

### BUGS

_[12-01-2024]_

- [x] Fix current_index taking values > len(list).

### FEATURES

_[12-01-2024]_

- [x] Add authors info above abstract.
- [x] Set refresh for query with flag `-r`.
- [x] Added date info along with the title
- [x] Added buffermode capture with `:`
- [x] Put all pdf file into a single folder
