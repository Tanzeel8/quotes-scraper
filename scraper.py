import requests
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com/"
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

quotes = []
for q in soup.find_all("span", class_="text"):
    quotes.append(q.text)

# Save results to a text file
with open("quotes.txt", "w", encoding="utf-8") as f:
    for quote in quotes:
        f.write(quote + "\n")

print("Quotes saved to quotes.txt ✅")
