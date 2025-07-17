# get_papers/utils.py

from typing import Tuple, List
import xml.etree.ElementTree as ET
import re


def is_non_academic(affil: str) -> bool:
    """
    Determines if the affiliation appears to be non-academic.

    Args:
        affil (str): The affiliation string.

    Returns:
        bool: True if the affiliation is non-academic, False otherwise.
    """
    academic_keywords = [
        "university", "college", "institute", "school",
        "lab", "center", "centre", "faculty", "hospital"
    ]
    return not any(keyword in affil.lower() for keyword in academic_keywords)


def parse_paper(xml_data: str) -> Tuple[str, str, str, List[str], List[str], str]:
    """
    Parses raw XML data of a PubMed article and extracts key metadata.

    Args:
        xml_data (str): The raw XML data string of a single PubMed article.

    Returns:
        Tuple containing:
            - PubMed ID (str)
            - Title (str)
            - Publication Date (str)
            - Non-academic author names (List[str])
            - Company affiliations (List[str])
            - Corresponding author email (str)
    """
    root = ET.fromstring(xml_data)
    article = root.find(".//PubmedArticle")
    if article is None:
        return "", "", "Unknown", [], [], ""

    pmid = article.findtext(".//PMID") or ""
    title = article.findtext(".//ArticleTitle") or ""

    pub_date_elem = article.find(".//PubDate")
    pub_date = "Unknown"
    if pub_date_elem is not None:
        year = pub_date_elem.findtext("Year") or ""
        month = pub_date_elem.findtext("Month") or ""
        day = pub_date_elem.findtext("Day") or ""
        pub_date = f"{year}-{month}-{day}".strip("-")

    non_acad_authors: List[str] = []
    companies: List[str] = []
    email = ""

    authors = article.findall(".//Author")
    for author in authors:
        fore = author.findtext("ForeName", "")
        last = author.findtext("LastName", "")
        full_name = f"{fore} {last}".strip()

        affil = author.findtext(".//AffiliationInfo/Affiliation")
        if affil:
            if is_non_academic(affil):
                non_acad_authors.append(full_name)
                companies.append(affil)

            if "@" in affil and not email:
                match = re.search(r'[\w\.-]+@[\w\.-]+', affil)
                if match:
                    email = match.group(0)

    return pmid, title, pub_date, non_acad_authors, companies, email
