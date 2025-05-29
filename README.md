# mychatgpt

This repository contains miscellaneous scripts.

## `scraper.py`

`scraper.py` retrieves a brief introduction for a list of cities. It attempts to
scrape Wikipedia first and falls back to Baidu Baike if the page is not found.

### Usage

```bash
python scraper.py Beijing Shanghai -o cities.json
```

The result will be written to `cities.json` with UTF-8 encoding.
