import requests
import csv
import re
from typing import List, Dict

# PubMed API base URLs
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

# Keywords to identify non-academic affiliations
NON_ACADEMIC_KEYWORDS = ["Pharma", "Biotech", "Inc.", "Ltd.", "Corporation", "Company"]
# Regular expressions to identify academic email domains
ACADEMIC_EMAIL_PATTERNS = [r".*\.edu$", r".*\.ac\..*", r".*\.gov$"]


def fetch_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetches research papers from PubMed based on a query.

    Args:
        query (str): The search query to fetch papers.
        max_results (int, optional): Maximum number of results to fetch. Defaults to 100.

    Returns:
        List[Dict]: A list of dictionaries containing paper details.
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }
    response = requests.get(PUBMED_API_URL, params=params)

    if response.status_code != 200:
        raise Exception("Error fetching data from PubMed API")

    data = response.json()
    paper_ids = data.get("esearchresult", {}).get("idlist", [])

    papers = []
    for paper_id in paper_ids:
        details = fetch_paper_details(paper_id)
        if details:
            papers.append(details)

    return papers


def fetch_paper_details(paper_id: str) -> Dict:
    """Fetches details of a single paper from PubMed.

    Args:
        paper_id (str): The PubMed ID of the paper.

    Returns:
        Dict: A dictionary containing details of the paper.
    """
    params = {
        "db": "pubmed",
        "id": paper_id,
        "retmode": "json",
    }
    response = requests.get(PUBMED_SUMMARY_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"Error fetching details for paper ID {paper_id}")

    data = response.json()
    result = data.get("result", {}).get(paper_id, {})

    return {
        "PubmedID": paper_id,
        "Title": result.get("title", "N/A"),
        "Publication Date": result.get("pubdate", "N/A"),
        "Authors": result.get("authors", []),
        "Company Affiliation": [],
        "Corresponding Author Email": "",
    }


def is_non_academic_author(author_info: Dict) -> bool:
    """Determines if an author is non-academic based on email and affiliation.

    Args:
        author_info (Dict): Dictionary containing author details.

    Returns:
        bool: True if the author is non-academic, False otherwise.
    """
    academic_keywords = {"university", "institute", "college", "lab", "research center"}
    academic_domains = {".edu", ".ac.", ".gov", ".org"}

    email = author_info.get("Email", "").lower()
    affiliation = author_info.get("Affiliation", "").lower()

    # Check for academic email domains
    if any(domain in email for domain in academic_domains):
        return False  # Academic author

    # Check for academic keywords in affiliation
    if any(keyword in affiliation for keyword in academic_keywords):
        return False  # Academic author

    return True  # Non-academic author


def filter_non_academic_authors(papers: List[Dict], debug: bool = False) -> List[Dict]:
    """Filters papers to keep only those with at least one non-academic author.

    Args:
        papers (List[Dict]): A list of dictionaries containing paper details.
        debug (bool): If True, print debug information.

    Returns:
        List[Dict]: A list of filtered papers with non-academic authors.
    """
    filtered_papers = []

    for paper in papers:
        if debug:
            print(f"Checking paper: {paper['Title']}")

        authors = paper.get("Authors", [])  # List of author dictionaries
        if any(is_non_academic_author(author) for author in authors):
            filtered_papers.append(paper)

    if debug:
        print(f"Total papers after filtering: {len(filtered_papers)}")
    return filtered_papers

def save_to_csv(papers: List[Dict], filename: str = "filtered_papers.csv"):
    """Saves the filtered research papers to a CSV file.

    Args:
        papers (List[Dict]): A list of dictionaries containing paper details.
        filename (str, optional): The filename to save the results. Defaults to "filtered_papers.csv".
    """
    fieldnames = ["PubmedID", "Title", "Publication Date",
                  "Non-academic Authors", "Company Affiliation", "Corresponding Author Email"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for paper in papers:
            filtered_paper = {key: paper.get(key, "") for key in fieldnames}  # Ensure only expected fields
            writer.writerow(filtered_paper)

    print(f"Saved {len(papers)} papers to {filename}")