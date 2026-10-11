# Quotes Scraper

A Python web scraper that collects quotes, authors and tags from
[Quotes to Scrape](http://quotes.toscrape.com/) and saves them to CSV and Excel files.

## Features
- Scrapes all pages automatically (follows the "Next" button)
- Extracts quote text, author and tags
- Retries failed requests with exponential backoff
- Polite random delay between requests
- Optional page limit for quick testing
- Saves partial results if the script is interrupted or fails

## Tools used
Python, Requests, BeautifulSoup, pandas, openpyxl

## How to run
```bash
# 1. Install the libraries
pip install -r requirements.txt

# 2. Scrape all pages
python scraper.py

# 3. Scrape only the first 3 pages (for testing)
python scraper.py 3
```

## Output
Running the script creates `quotes.csv` and `quotes.xlsx` (100 quotes in total).
A sample is included in [`sample_output.csv`](sample_output.csv).

| text | author | tags |
|------|--------|------|
| “It is our choices, Harry, that show what we truly are...” | J.K. Rowling | abilities, choices |
| “The person, be it gentleman or lady, who has not pleasure in a good novel...” | Jane Austen | aliteracy, books, classic, humor |
| “Try not to become a man of success. Rather become a man of value.” | Albert Einstein | adulthood, success, value |

If the script is stopped early, partial data is saved as
`quotes_partial.csv` and `quotes_partial.xlsx`.

## License
MIT
