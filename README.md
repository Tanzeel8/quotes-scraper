# Quotes Scraper

A beginner Python web scraping project that scrapes quotes from [Quotes to Scrape](http://quotes.toscrape.com/).

## Features
- Scrapes quotes from multiple pages
- Option to scrape limited number of pages (for testing)
- Saves quotes into CSV and Excel (or text if you prefer)

## Install
```bash
pip install -r requirements.txt

# Scrape all pages
python quotes_scraper.py

# Scrape first 3 pages only
python quotes_scraper.py 3
