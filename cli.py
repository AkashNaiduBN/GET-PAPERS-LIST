import typer
from rich import print
import pandas as pd
from get_papers.core import fetch_pubmed_ids, fetch_pubmed_details
from get_papers.utils import parse_paper

app = typer.Typer()

@app.command()
def fetch(
    query: str,
    file: str = typer.Option(None, "--file", "-f"),
    debug: bool = typer.Option(False, "--debug", "-d")
):
    ids = fetch_pubmed_ids(query)
    if debug:
        print(f"Found {len(ids)} PMIDs.")

    records = []
    for pmid in ids:
        xml = fetch_pubmed_details(pmid)
        data = parse_paper(xml)
        if data[3]:  # If any non-academic authors
            records.append({
                "PubmedID": data[0],
                "Title": data[1],
                "Publication Date": data[2],
                "Non-academic Author(s)": ", ".join(data[3]),
                "Company Affiliation(s)": ", ".join(data[4]),
                "Corresponding Author Email": data[5],
            })

    df = pd.DataFrame(records)
    if file:
        df.to_csv(file, index=False)
        print(f"[green]Saved results to {file}[/green]")
    else:
        print(df.to_string(index=False))

if __name__ == "__main__":
    app()


