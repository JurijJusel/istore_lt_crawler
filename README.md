# istore_crawler

`istore_crawler` is a Scrapy-based web crawler designed to scrape product data
from [istore.lt](https://www.istore.lt) for **educational purposes**.
It extracts detailed information about products like Mac, iPhone, iPad,
accessories, and more, storing data in JSONL format in the `data/` directory
for analysis or study.

## Purpose
This project serves as a learning exercise for web scraping with Scrapy and Pydantic,
targeting product data from [istore.lt](https://www.istore.lt).

## Features
- **Scrapes multiple product categories**:
  - iMac
  - iPhone
  - iPad
  - Apple Watch
  - Accessories
  - Promotions (Akcijos)
- **Extracts product details** such as name, price, availability, URL, image URL,
and category-specific attributes (e.g., specs for iMac, params for iPad).
- **Stores data** as line-delimited JSON (`.jsonl`) in the `data` directory.

## Data Models

### IstoreItemModel (used by most spiders)
- `name`: Product name (str)
- `price`: Product price (str)
- `downloaded_date`: Date and time when the data was scraped (str)
- `availability`: Stock status (str)
- `url`: Product page URL (str)
- `image_url`: Image URL (str)

### IpadItemModel (iPad-specific)
- `name`: Product name (str)
- `params`: Technical specifications (str)
- `price`: Product price (str)
- `downloaded_date`: Date and time when the data was scraped (str)
- `availability`: Stock status (str)
- `url`: Product page URL (str)
- `image_url`: Image URL (str)

### ImacItemModel (iMac-specific)
- `name`: Product name (str)
- `proc`: Processor (str)
- `ram`: Memory (str)
- `disc`: Storage (str)
- `gpu`: Graphics processor (str)
- `system`: Operating system (str)
- `color`: Color (str)
- `price`: Product price (str)
- `downloaded_date`: Date and time when the data was scraped (str)
- `availability`: Stock status (str)
- `url`: Product page URL (str)
- `image_url`: Image URL (str)

##  Installation

### Prerequisites
- Python >= 3.12

### Dependencies include:
- pydantic>=2.11.5
- scrapy>=2.13.0
- rich>=13.0.0

## 🛠 Setup and Run with Makefile

This project includes a `Makefile` to simplify setup and management tasks.

### Makefile Commands
all commands can be show by running:
```bash
make help
```

### Setup and Run with Makefile
Create a virtual environment and install dependencies:
```bash
make venv
make setup
```
or
```bash
make all
```
View all commands:
```bash
make help
```

## Configuration
- Configuration settings can be adjusted in `crawler/settings.py`.
- The crawler respects settings like user-agents and scraping rules as defined.

## Usage
Run all spiders using:
```bash
python run_spiders.py

# or
make run
```

## Output
- Data is saved in 'data/' as .jsonl files (overwritten on each run).
- Logs are saved in 'logs/'' (see settings.py).

## License
MIT License

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open
an issue for any improvements or bug fixes.

## Acknowledgements
This project was inspired by the need to learn web scraping with Scrapy and
to gather product data from `www.istore.lt` for educational purposes.
