import typer
from rich import print
import pandas as pd

from get_papers.core import fetch_pubmed_ids, fetch_pubmed_details
from get_papers.utils import parse_paper

app = typer.Typer(help="Fetch PubMed papers with non-academic authors using a search query.")

# NO @app.command() needed
def main(
    query: str = typer.Argument(..., help="Search query for PubMed."),
    file: str = typer.Option(None, "--file", "-f", help="Output CSV file to save results."),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug logging."),
):
    try:
        ids = fetch_pubmed_ids(query)
    except Exception as e:
        print(f"[red]Error fetching PMIDs for query '{query}': {e}[/red]")
        raise typer.Exit(code=1)

    if debug:
        print(f"[yellow]Found {len(ids)} PMIDs for query: '{query}'[/yellow]")

    records = []

    for i, pmid in enumerate(ids, 1):
        try:
            xml = fetch_pubmed_details(pmid)
            data = parse_paper(xml)
            if data[3]:
                records.append({
                    "PubmedID": data[0],
                    "Title": data[1],
                    "Publication Date": data[2],
                    "Non-academic Author(s)": ", ".join(data[3]),
                    "Company Affiliation(s)": ", ".join(data[4]),
                    "Corresponding Author Email": data[5],
                })
                if debug:
                    print(f"[green]{i}. ✅ {pmid}: {data[1][:60]}...[/green]")
            elif debug:
                print(f"[grey]{i}. ❌ {pmid}: Academic authors only[/grey]")
        except Exception as e:
            print(f"[red]Error processing PMID {pmid}: {e}[/red]")

    df = pd.DataFrame(records)

    if df.empty:
        print("[bold red]No results found with non-academic authors.[/bold red]")
    elif file:
        try:
            df.to_csv(file, index=False)
            print(f"[green]Saved {len(df)} records to [bold]{file}[/bold][/green]")
        except Exception as e:
            print(f"[red]Failed to save to file '{file}': {e}[/red]")
    else:
        print(df.to_string(index=False))


if __name__ == "__main__":
    typer.run(main)
