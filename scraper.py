# quotes_scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
import pandas as pd
import sys

# Config
START_URL = "http://quotes.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}
REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
DELAY_MIN, DELAY_MAX = 1.0, 2.0  # polite delay between requests
MAX_PAGES = None  # set to an integer to limit pages for testing, else None

def fetch_with_retries(session, url, max_retries=MAX_RETRIES, timeout=REQUEST_TIMEOUT):
    """Requests GET with retries and exponential backoff."""
    backoff = 1
    for attempt in range(1, max_retries + 1):
        try:
            resp = session.get(url, headers=HEADERS, timeout=timeout)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            print(f"[!] Request failed (attempt {attempt}/{max_retries}): {e}")
            if attempt == max_retries:
                raise
            time.sleep(backoff)
            backoff *= 2
    raise RuntimeError("Unreachable code in fetch_with_retries")

def parse_quotes_from_page(html):
    """Return list of dicts: [{'text':..., 'author':..., 'tags':[...]}]"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    quote_blocks = soup.find_all("div", class_="quote")
    for block in quote_blocks:
        text_tag = block.find("span", class_="text")
        author_tag = block.find("small", class_="author")
        tag_elements = block.find_all("a", class_="tag")

        text = text_tag.get_text(strip=True) if text_tag else ""
        author = author_tag.get_text(strip=True) if author_tag else ""
        tags = [t.get_text(strip=True) for t in tag_elements] if tag_elements else []

        items.append({"text": text, "author": author, "tags": ", ".join(tags)})
    return items, soup

def find_next_page(soup, base_url):
    """Return absolute URL of next page or None."""
    next_li = soup.find("li", class_="next")
    if next_li and next_li.find("a"):
        href = next_li.find("a").get("href")
        return urljoin(base_url, href)
    return None

def save_data(data_list, csv_path="quotes.csv", excel_path="quotes.xlsx"):
    df = pd.DataFrame(data_list)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(excel_path, index=False)
    print(f"[✓] Saved {len(df)} records to {csv_path} and {excel_path}")

def main(start_url=START_URL, max_pages=MAX_PAGES):
    session = requests.Session()
    url = start_url
    all_data = []
    page_count = 0

    try:
        while url:
            page_count += 1
            if max_pages and page_count > max_pages:
                print("[i] Reached max_pages limit. Stopping.")
                break

            print(f"[i] Fetching page {page_count}: {url}")
            resp = fetch_with_retries(session, url)
            items, soup = parse_quotes_from_page(resp.text)
            print(f"[i] Found {len(items)} quotes on this page.")
            all_data.extend(items)

            # polite delay
            time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

            url = find_next_page(soup, start_url)  # next page absolute URL or None

        # after loop, save results
        if all_data:
            save_data(all_data)
        else:
            print("[!] No data scraped.")

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Saving partial results...")
        if all_data:
            save_data(all_data, csv_path="quotes_partial.csv", excel_path="quotes_partial.xlsx")
        sys.exit(1)

    except Exception as e:
        print(f"[!] Fatal error: {e}")
        if all_data:
            print("[i] Saving partial results before exit...")
            save_data(all_data, csv_path="quotes_partial.csv", excel_path="quotes_partial.xlsx")
        else:
            print("[i] No data to save.")
        sys.exit(1)

if __name__ == "__main__":
    # optional: pass number of pages to scrape from CLI e.g. python quotes_scraper.py 3
    if len(sys.argv) > 1:
        try:
            max_p = int(sys.argv[1])
        except ValueError:
            max_p = None
        main(max_pages=max_p)
    else:
        main()
