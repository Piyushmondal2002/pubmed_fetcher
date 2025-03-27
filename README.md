# PubMed Fetcher

A Python command-line tool to fetch research papers from PubMed based on user queries, filtering for those with at least one author affiliated with pharmaceutical or biotech companies.


## Features

- Fetches research papers using the PubMed API.
- Filters papers to include only those with non-academic authors.
- Outputs results in a CSV format.
- Supports command-line arguments for flexibility.

## Here are the steps about how to install and use the product 
## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/pijushmondal-2002/pubmed-fetcher.git

2. **Navigate to the project directory:**
   Write cmd to the location and press enter , or press shift + cntrl + rightclick and choose cmd and run it as an adminitrator(!important) 

3. **Install dependencies using Poetry:**
   poetry install

4. ```markdown
## Usage

To fetch papers related to a specific query:

```bash
poetry run get-papers-list "your search query" -f output.csv -d
eg:  poetry run python fetch_papers.py "cancer treatment" -f cancer2.csv

** Definitions of the command**

"your search query": The term you want to search for in PubMed.

-f output.csv: (Optional) Specify the filename to save the results.

-d: (Optional) Enable debug mode for detailed execution logs.


## License

This project is licensed under the MIT License. See the LICENSE file for details.

