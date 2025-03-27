import argparse
import traceback
from fetch_papers import fetch_papers, filter_non_academic_authors, save_to_csv

def main():
    """Main function to parse arguments and execute the script."""
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed papers.")
    parser.add_argument("-f", "--file", type=str, default=None,
                        help="Filename to save the results (CSV). If not provided, print to console.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()

    if args.debug:
        print(f"Debug Mode ON: Fetching papers for query: '{args.query}'")

    try:
        papers = fetch_papers(args.query)
        if args.debug:
            print(f"Total papers fetched: {len(papers)}")

        filtered_papers = filter_non_academic_authors(papers)
        if args.debug:
            print(f"Total papers after filtering: {len(filtered_papers)}")

        if args.file:
            save_to_csv(filtered_papers, args.file)
            print(f"Results saved to '{args.file}'")
        else:
            print(filtered_papers)

    except Exception as e:
        print(f"An error occurred: {e}")
        if args.debug:
            traceback.print_exc()

if __name__ == "__main__":
    main()