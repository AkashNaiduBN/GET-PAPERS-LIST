# GET-PAPERS-LIST

A command-line tool to fetch and filter biomedical research papers from **PubMed**, focusing on papers **authored by individuals with non-academic affiliations**. This is helpful for identifying papers involving industry collaborations or private sector research.

---

## Project Structure

get-papers-list/
│
├── get_papers/
│   ├── core.py           # Handles PubMed API fetching
│   ├── utils.py          # XML parsing, filtering, and helper functions
│   └── __init__.py
│
├── cli.py                # Command-line entry point
├── tests/
│   └── test_pubmed.py    # Pytest-based unit tests for core functionality
├── README.md             # Documentation
├── pyproject.toml        # Poetry setup
└── output.csv            # Result file


---

## Features

- Accepts any search query (e.g., `"cancer immunotherapy"`)
- Extracts:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic Author(s)
  - Company Affiliation(s)
  - Corresponding Author Email
- Filters out **purely academic** affiliations
- Optionally saves output to CSV
- Supports helpful CLI flags:
  - `-f` / `--file` to save results
  - `-d` / `--debug` for verbose output
  - `-h` / `--help` for usage instructions
- Tested using `pytest`
- Designed for automation and CI/CD (GitHub Actions ready)
- Typed and modular Python 3.13+ code

---

## Installation

Python **3.13+** and Poetry installed.

```bash
git clone https://github.com/AkashNaiduBN/GET-PAPERS-LIST
cd GET-PAPERS-LIST
poetry install

# usage

# Basic query and print results
poetry run python cli.py "cancer therapy"

# Save results to CSV
poetry run python cli.py "covid vaccine" -f covid_results.csv

# Enable debug logs
poetry run python cli.py "AI in medical imaging" -d

# Running Tests
poetry run pytest

# Tools & Libraries Used

| Tool                                                         | Purpose                                               | Link                     |
| ------------------------------------------------------------ | ----------------------------------------------------- | ------------------------ |
| [NCBI E-Utils](https://www.ncbi.nlm.nih.gov/books/NBK25501/) | Fetch PubMed data                                     | REST API                 |
| [Typer](https://typer.tiangolo.com)                          | Command-line interface                                | Python library           |
| [Rich](https://github.com/Textualize/rich)                   | Colorful terminal output                              | Python library           |
| [Pandas](https://pandas.pydata.org)                          | DataFrame operations                                  | Python library           |
| [Pytest](https://docs.pytest.org/en/stable/)                 | Unit testing                                          | Python testing framework |
| [Poetry](https://python-poetry.org/)                         | Dependency management                                 | Python tool              |
| [ChatGPT](https://chat.openai.com/)                          | Brainstorming logic, testing strategy & CLI structure | LLM                      |

