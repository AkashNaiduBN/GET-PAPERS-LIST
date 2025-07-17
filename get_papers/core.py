# get_papers/core.py

from typing import List, Dict, Optional
import requests
import xml.etree.ElementTree as ET
import re


def fetch_pubmed_ids(query: str, retmax: int = 15) -> List[str]:
    """
    Fetches PubMed IDs for a given query.

    Args:
        query (str): The search query.
        retmax (int): Maximum number of results to fetch.

    Returns:
        List[str]: A list of PubMed IDs.
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]


def fetch_pubmed_details(pmid: str) -> Optional[str]:
    """
    Fetches article details for a given PubMed ID in XML format.

    Args:
        pmid (str): PubMed ID.

    Returns:
        Optional[str]: Raw XML string of article data.
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    return response.text


def is_non_academic(affiliation: str) -> bool:
    """
    Checks whether the affiliation string indicates a non-academic institution.

    Args:
        affiliation (str): Affiliation string.

    Returns:
        bool: True if the affiliation is non-academic, else False.
    """
    academic_keywords = [
        "University", "College", "Institute", "Hospital", "School",
        "Academy", "Centre", "Center", "Faculty"
    ]
    return not any(word.lower() in affiliation.lower() for word in academic_keywords)


def parse_article(xml_data: str) -> Optional[Dict[str, str]]:
    """
    Parses article XML and extracts required fields.

    Args:
        xml_data (str): Raw XML data of the article.

    Returns:
        Optional[Dict[str, str]]: Extracted article information.
    """
    try:
        root = ET.fromstring(xml_data)
        article = root.find(".//PubmedArticle")
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        date = article.findtext(".//PubDate/Year")
        if not date:
            date = article.findtext(".//PubDate/MedlineDate", default="")

        authors = article.findall(".//Author")
        non_academic_authors = []
        companies = []
        email = ""

        for author in authors:
            name_parts = []
            last = author.findtext("LastName")
            first = author.findtext("ForeName")
            if last:
                name_parts.append(last)
            if first:
                name_parts.append(first)
            fullname = " ".join(name_parts)

            affiliation = author.findtext(".//AffiliationInfo/Affiliation")
            if affiliation:
                if is_non_academic(affiliation):
                    non_academic_authors.append(fullname)
                    companies.append(affiliation)
                if not email:
                    match = re.search(r"[\w\.-]+@[\w\.-]+", affiliation)
                    if match:
                        email = match.group()

        if not non_academic_authors:
            return None

        return {
            "PubmedID": pmid or "",
            "Title": title or "",
            "Publication Date": date or "",
            "Non-academic Author(s)": ", ".join(non_academic_authors),
            "Company Affiliation(s)": ", ".join(companies),
            "Corresponding Author Email": email,
        }
    except Exception:
        return None


def search_and_filter(query: str, retmax: int = 100, debug: bool = False) -> List[Dict[str, str]]:
    """
    Combines fetching, parsing, and filtering of PubMed data.

    Args:
        query (str): Search query.
        retmax (int): Maximum results to fetch.
        debug (bool): Enable debug output.

    Returns:
        List[Dict[str, str]]: Filtered article information.
    """
    pmids = fetch_pubmed_ids(query, retmax)
    if debug:
        print(f"[DEBUG] Found {len(pmids)} PMIDs.")

    articles = []
    for i, pmid in enumerate(pmids, start=1):
        if debug:
            print(f"[DEBUG] Processing PMID {i}/{len(pmids)}: {pmid}")
        xml = fetch_pubmed_details(pmid)
        if xml:
            parsed = parse_article(xml)
            if parsed:
                articles.append(parsed)
    return articles
