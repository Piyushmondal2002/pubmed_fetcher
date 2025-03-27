import requests
import argparse
import csv
import re
from typing import List, Dict

# PubMed API base URL
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Keywords to identify non-academic affiliations
NON_ACADEMIC_KEYWORDS = ["Pharma", "Biotech", "Inc.", "Ltd.", "Corporation", "Company"]

# Academic email domains to exclude
ACADEMIC_EMAIL_PATTERNS = [r".*\.edu$", r".*\.ac\..*", r".*\.gov$"]


def fetch_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetches research papers from PubMed based on a query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }
    response = requests.get(PUBMED_API_URL, params=params)

    if response.status_code != 200:
        print("Error fetching data from PubMed API")
        return []

    data = response.json()
    paper_ids = data.get("esearchresult", {}).get("idlist", [])

    papers = []
    for paper_id in paper_ids:
        details = fetch_paper_details(paper_id)
        if details:
            papers.append(details)

    return papers


def fetch_paper_details(paper_id: str) -> Dict:
    """Fetches details of a single paper from PubMed."""
    params = {
        "db": "pubmed",
        "id": paper_id,
        "retmode": "xml",
    }
    response = requests.get(PUBMED_DETAILS_URL, params=params)

    if response.status_code != 200:
        print(f"Error fetching details for paper ID {paper_id}")
        return {}

    # Parsing logic to extract relevant fields can go here
    # (Mocking the data for now, real implementation requires XML parsing)
    return {
        "PubmedID": paper_id,
        "Title": f"Sample Title {paper_id}",
        "Publication Date": "2024-03-27",
        "Non-academic Authors": ["Dr. John Doe"],
        "Company Affiliation": ["Pfizer"],
        "Corresponding Author Email": "johndoe@pfizer.com",
    }


def is_non_academic(email: str, affiliation: str) -> bool:
    """Checks if an author is affiliated with a non-academic institution."""
    if any(re.match(pattern, email) for pattern in ACADEMIC_EMAIL_PATTERNS):
        return False  # It's an academic email
    if any(keyword in affiliation for keyword in NON_ACADEMIC_KEYWORDS):
        return True  # Affiliation contains a non-academic keyword
    return False  # Default to academic


def filter_non_academic_authors(papers: List[Dict]) -> List[Dict]:
    """Filters papers to keep only those with at least one non-academic author."""
    filtered_papers = []
    for paper in papers:
        authors = paper.get("Non-academic Authors", [])
        affiliations = paper.get("Company Affiliation", [])

        if authors and affiliations:
            filtered_papers.append(paper)

    return filtered_papers


def save_to_csv(papers: List[Dict], filename: str = "filtered_papers.csv"):
    """Saves the filtered research papers to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "PubmedID", "Title", "Publication Date",
            "Non-academic Authors", "Company Affiliation", "Corresponding Author Email"
        ])
        writer.writeheader()
        writer.writerows(papers)


def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed papers.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the results (CSV).")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()

    if args.debug:
        print(f"Debug Mode ON: Fetching papers for query: {args.query}")

    papers = fetch_papers(args.query)

    if args.debug:
        print(f"Total papers fetched: {len(papers)}")

    filtered_papers = filter_non_academic_authors(papers)

    if args.file:
        save_to_csv(filtered_papers, args.file)
        print(f"Results saved to {args.file}")
    else:
        print("Results (CSV Format):")
        for paper in filtered_papers:
            print(paper)


if __name__ == "__main__":
    main()