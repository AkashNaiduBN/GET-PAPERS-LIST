# GET-PAPERS-LIST

A command-line tool to fetch and save recent research papers from **PubMed** based on a search query. Useful for researchers, students, and developers who need structured access to biomedical literature.

---

## Features

- Search PubMed using any keyword (e.g., "covid vaccine", "cancer therapy")
- Extracts:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic Author(s)
  - Company Affiliation(s)
  - Corresponding Author Email
- Saves results into a `.csv` file
- Written in **Python 3.13+**, CLI powered by `poetry`

# usage
poetry run get-papers-list "your search query" --file output.csv --debug

