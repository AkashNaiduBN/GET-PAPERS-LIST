from typing import Tuple, List
import xml.etree.ElementTree as ET
import re

def is_non_academic(affil: str) -> bool:
    academic_keywords = ["university", "college", "institute", "school", "lab", "center", "centre"]
    return not any(word in affil.lower() for word in academic_keywords)

def parse_paper(xml_data: str) -> Tuple[str, str, str, List[str], List[str], str]:
    root = ET.fromstring(xml_data)
    article = root.find(".//PubmedArticle")
    pmid = article.findtext(".//PMID")
    title = article.findtext(".//ArticleTitle")
    pub_date_elem = article.find(".//PubDate")
    pub_date = "Unknown"
    if pub_date_elem is not None:
        year = pub_date_elem.findtext("Year") or ""
        month = pub_date_elem.findtext("Month") or ""
        day = pub_date_elem.findtext("Day") or ""
        pub_date = f"{year}-{month}-{day}".strip("-")
    authors = article.findall(".//Author")
    non_acad_authors = []
    companies = []
    email = ""
    for author in authors:
        affil = author.findtext(".//AffiliationInfo/Affiliation")
        if affil and is_non_academic(affil):
            name = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()
            non_acad_authors.append(name)
            companies.append(affil)
        if affil and "@" in affil and not email:
            match = re.search(r'[\w\.-]+@[\w\.-]+', affil)
            if match:
                email = match.group(0)
    return pmid, title, pub_date, non_acad_authors, companies, email
