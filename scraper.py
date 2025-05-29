import argparse
import json
import requests
from bs4 import BeautifulSoup


def fetch_wikipedia_summary(city: str) -> str | None:
    url = f"https://zh.wikipedia.org/wiki/{city}"
    r = requests.get(url)
    if r.status_code != 200:
        # Try English Wikipedia as fallback
        url = f"https://en.wikipedia.org/wiki/{city}"
        r = requests.get(url)
        if r.status_code != 200:
            return None
    soup = BeautifulSoup(r.text, "html.parser")
    p = soup.find("p")
    if p:
        return p.get_text(strip=True)
    return None


def fetch_baidu_summary(city: str) -> str | None:
    url = f"https://baike.baidu.com/item/{city}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find("div", class_="lemma-summary")
    if div:
        return div.get_text(strip=True)
    return None


def scrape_cities(cities: list[str]) -> dict[str, str]:
    results: dict[str, str] = {}
    for city in cities:
        summary = fetch_wikipedia_summary(city)
        if not summary:
            summary = fetch_baidu_summary(city)
        results[city] = summary or ""
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape city summaries from Wikipedia or Baidu Baike."
    )
    parser.add_argument("cities", nargs="*", help="City names to scrape")
    parser.add_argument(
        "-o", "--output", default="cities.json", help="Output JSON filename"
    )
    args = parser.parse_args()

    summaries = scrape_cities(args.cities)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
