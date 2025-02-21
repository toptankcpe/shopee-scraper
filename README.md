# Shopee Scraper

A Python-based scraper for collecting product information from Shopee Thailand.

## Overview
This project automates the following steps:
- Login with your Shopee credentials
- Search for a specific keyword
- Extract product details (name, price, variants, stock, category, seller info, ratings, etc.)
- Logout to end the session cleanly

## Features
### Object-Oriented Structure
Organized into classes such as:
- `LoginHandler`
- `SearchHandler`
- `ProductScraper`
- `VariantScraper`

All are orchestrated by a `ShopeeScraper` facade.

### Template Method and Facade Patterns
- `AbstractScraper` defines a template method (`scrape()`) with `before_scrape()`, `do_scrape()`, and `after_scrape()`.
- `ShopeeScraper` provides a unified interface (facade) to simplify the scraping workflow.

### SeleniumBase
Utilizes SeleniumBase under the hood for browser automation, including support for undetected drivers and extra convenience methods.

### Modular Design
- Handlers for login, search, product details, and variant selection reside in `handlers/` folder.
- Utilities such as scrolling and parsing are in `utils.py`.
- Data models like `ProductData` (and `ScrapeParams` for parameter validation) are defined in `models.py`.

## Key Files
- **`main.py`**: Entry point that initializes and runs the scraper.
- **`abstract_scraper.py`**: Defines the `AbstractScraper` base class with a template method.
- **`shopee_scraper.py`**: The main `ShopeeScraper` facade that orchestrates the scraping process.

### Handlers:
- **`login_handler.py`**: Handles the login flow.
- **`search_handler.py`**: Handles keyword search.
- **`product_scraper.py`**: Extracts product info (price, description, rating, etc.).
- **`variant_scraper.py`**: Extracts variant options (e.g., sizes, colors) and stock per variant.

- **`models.py`**: Contains data model classes (`ProductData`) and a Pydantic model (`ScrapeParams`) for validating parameters.
- **`utils.py`**: Contains common utility functions (scrolling, parsing, etc.).

## Getting Started

### Clone the Repository
```sh
git clone https://github.com/your-username/my_shopee_scraper.git
cd my_shopee_scraper
```

### Install Dependencies
```sh
pip install -r requirements.txt
```
Ensure you have Python 3.7+ and a supported WebDriver environment.

### Configure Your Credentials & Parameters
This project accepts parameters via the command-line.

#### Required Parameters:
- `--username`: Your Shopee username.
- `--password`: Your Shopee password.
- `--keyword`: The search keyword.

#### Optional Parameters:
- `--numpage`: The number of pages to scrape (must be > 0 if provided). Defaults to `None`.
- `--itemperpage`: The number of items per page to scrape (must be > 0 if provided). Defaults to `None`.

#### Example Command:
```sh
python main.py --username your_username --password your_password --keyword "iphone" --numpage 2 --itemperpage 5
```

A browser window should open, navigate to Shopee, log in with your credentials, perform the search, scrape the product data, and then log out.

### Review Output
By default, the scraper prints the resulting JSON output to the console in the `after_scrape()` method. You can modify `shopee_scraper.py` or `main.py` if you wish to store the output in a file or database.

## Notes
### CAPTCHA Handling
Shopee may occasionally require manual CAPTCHA solving. When this occurs, you may need to solve it for the scraper to continue.

### Rate Limits & Anti-Bot Measures
Use the scraper responsibly to avoid IP blocking or violations of Shopee's terms of service.

## Disclaimer
This project is for educational purposes. Please ensure compliance with Shopee's policies before scraping.

## Contributing
Contributions are welcome! Feel free to submit issues for bugs or suggestions, or open a pull request with improvements. Please follow existing coding styles and add tests where appropriate.

## License
This project is released under the MIT License. You can freely use or modify this software under the terms of the license.

