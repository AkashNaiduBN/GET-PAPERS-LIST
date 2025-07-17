import pytest
from get_papers.core import fetch_pubmed_ids, fetch_pubmed_details

def test_fetch_pubmed_ids_returns_ids(monkeypatch):
    mock_response = {
        "esearchresult": {
            "idlist": ["12345678", "87654321"]
        }
    }

    class MockResponse:
        def raise_for_status(self): pass
        def json(self): return mock_response

    def mock_get(url, params):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    ids = fetch_pubmed_ids("test query")
    assert ids == ["12345678", "87654321"]


def test_fetch_pubmed_details_with_valid_data(monkeypatch):
    sample_xml = """
    <PubmedArticleSet>
      <PubmedArticle>
        <MedlineCitation>
          <PMID>12345678</PMID>
          <Article>
            <ArticleTitle>Test Article Title</ArticleTitle>
            <Journal>
              <JournalIssue>
                <PubDate>
                  <Year>2024</Year>
                </PubDate>
              </JournalIssue>
            </Journal>
            <AuthorList>
              <Author>
                <LastName>Doe</LastName>
                <ForeName>John</ForeName>
                <AffiliationInfo>
                  <Affiliation>XYZ Biotech Ltd</Affiliation>
                </AffiliationInfo>
              </Author>
            </AuthorList>
          </Article>
        </MedlineCitation>
      </PubmedArticle>
    </PubmedArticleSet>
    """

    class MockResponse:
        status_code = 200
        def raise_for_status(self): pass
        @property
        def text(self):  # your fetch_pubmed_details uses .text not .content
            return sample_xml

    def mock_get(url, params):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    from get_papers.utils import parse_paper

    xml = fetch_pubmed_details("12345678")
    pmid, title, pub_date, authors, companies, email = parse_paper(xml)

    assert pmid == "12345678"
    assert "XYZ Biotech Ltd" in companies[0]
    assert "John Doe" in authors[0]
