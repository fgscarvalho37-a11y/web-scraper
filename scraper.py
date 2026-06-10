import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from datetime import datetime

# ── CONFIG ──
BASE_URL = "https://books.toscrape.com"
OUTPUT_FILE = "output/books.csv"
LOG_FILE = "output/scraper_log.json"

def scrape_page(url: str) -> list:
    """Scrapa uma página de livros."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    books = []

    for article in soup.select("article.product_pod"):
        title = article.select_one("h3 a")["title"]
        price = article.select_one("p.price_color").text.strip()
        rating = article.select_one("p.star-rating")["class"][1]
        availability = article.select_one("p.availability").text.strip()

        books.append({
            "title": title,
            "price": float(price.replace("£", "").replace("Â", "")),
            "rating": rating,
            "availability": availability
        })

    return books

def scrape_all(max_pages: int = 5) -> list:
    """Scrapa múltiplas páginas."""
    all_books = []

    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/catalogue/page-{page}.html"
        print(f"[SCRAPER] Raspando página {page}...")
        try:
            books = scrape_page(url)
            all_books.extend(books)
            print(f"[SCRAPER] {len(books)} livros encontrados na página {page}.")
        except Exception as e:
            print(f"[SCRAPER] Erro na página {page}: {e}")
            break

    return all_books

def save_csv(books: list) -> None:
    """Salva os dados em CSV."""
    os.makedirs("output", exist_ok=True)
    df = pd.DataFrame(books)

    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    df["rating_num"] = df["rating"].map(rating_map)
    df["scraped_at"] = datetime.now().isoformat()

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"\n📚 Top 5 livros mais baratos:")
    print(df.nsmallest(5, "price")[["title", "price", "rating"]].to_string(index=False))
    print(f"\n⭐ Livros com 5 estrelas:")
    print(df[df["rating"] == "Five"][["title", "price"]].head().to_string(index=False))

def save_log(status: str, records: int, error: str = None) -> None:
    log = {
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "records_scraped": records,
        "error": error
    }
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def run():
    print("=" * 40)
    print("  WEB SCRAPER - Books to Scrape")
    print("=" * 40)

    try:
        books = scrape_all(max_pages=5)
        save_csv(books)
        save_log("SUCCESS", len(books))
        print(f"\n✅ Scraping concluído! {len(books)} livros coletados.")
    except Exception as e:
        save_log("FAILED", 0, str(e))
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    run()