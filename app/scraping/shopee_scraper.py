from seleniumbase import SB
from datetime import datetime, timezone
import json

from .abstract_scraper import AbstractScraper
from .handlers.login_handler import LoginHandler
from .handlers.search_handler import SearchHandler
from .handlers.product_scraper import ProductScraper
from .handlers.variant_scraper import VariantScraper
from .utils import ScrapeUtils


class ShopeeScraper(AbstractScraper):
    def __init__(self, username, password, keyword, numpage, itemperpage):
        self.username = username
        self.password = password
        self.keyword = keyword
        self.numpage = numpage
        self.itemperpage = itemperpage

        # Initialize handlers
        self.login_handler = LoginHandler(self.username, self.password)
        self.search_handler = SearchHandler(self.keyword)
        self.variant_scraper = VariantScraper()
        self.product_scraper = ProductScraper(self.variant_scraper)

        # Initialize result data structure
        self.results_data = {
            "data": [],
            "keyword": self.keyword,
            "sortBy": "relevance",
            "createdAt": "",
            "updatedAt": ""
        }

        self.login_url = "https://shopee.co.th/buyer/login"

    def before_scrape(self):
        print("[INFO] Preparing environment before scraping.")

    def do_scrape(self):
        with SB(uc=True, test=True) as sb:
            print("[INFO] Opening Shopee website with undetected driver...")
            sb.activate_cdp_mode(self.login_url)

            # Wait for page load
            try:
                sb.cdp.wait_for_element_visible("body", timeout=30)
                print("[INFO] Successfully loaded the page.")
            except Exception as e:
                raise RuntimeError(f"[ERROR] Error loading page: {e}")

            sb.sleep(2)

            # Change language if applicable
            try:
                sb.cdp.wait_for_element_visible(
                    "div.language-selection__list-item button:contains('English')",
                    timeout=20
                )
                sb.cdp.mouse_click("div.language-selection__list-item button:contains('English')")
                sb.sleep(2)
                print("[INFO] Successfully changed language to English.")
            except Exception as e:
                raise RuntimeError(f"[ERROR] Language selection failed: {e}")

            # Perform login
            try:
                self.login_handler.login(sb)
                print("[INFO] Successfully logged in.")
            except Exception as e:
                raise RuntimeError(f"[ERROR] Login failed: {e}")

            # Perform search
            try:
                total_pages = self.search_handler.search(sb)
                if self.numpage is not None and self.numpage < total_pages:
                    total_pages = self.numpage
                search_url = sb.cdp.get_current_url()
                print("[INFO] Successfully performed search.")
            except Exception as e:
                raise RuntimeError(f"[ERROR] Failed during search: {e}")

            for page in range(0, total_pages):
                page_url = f"{search_url}&page={page}"
                if page != 0:
                    sb.cdp.get(page_url)
                    sb.sleep(2)

                # Scroll to load products
                ScrapeUtils.scroll_page(sb)

                # Get product URLs
                try:
                    products = sb.cdp.find_all(
                        "//li[contains(@class, 'shopee-search-item-result__item')]//a[contains(@class, 'contents')]",
                        timeout=20
                    )
                    product_urls = [f"https://shopee.co.th{link.get_attribute('href')}" for link in products]
                    item_per_page = len(product_urls)
                    if self.itemperpage is not None and self.itemperpage < item_per_page:
                        item_per_page = self.itemperpage
                    print(f"[INFO] Successfully retrieved product URLs for page {page}.")
                except Exception as e:
                    raise RuntimeError(f"[ERROR] Failed to get product URLs: {e}")
                
                # Scrape product details
                for url in product_urls[:item_per_page]:
                    try:
                        product_obj = self.product_scraper.scrape_product_details(sb, url)
                        product_dict = {
                            "id": product_obj.id,
                            "name": product_obj.name,
                            "description": product_obj.description,
                            "price": product_obj.price,
                            "totalQuantity": product_obj.totalQuantity,
                            "categoryPath": product_obj.categoryPath,
                            "url": product_obj.url,
                            "variants": product_obj.variants,
                            "rating": product_obj.rating,
                            "seller": product_obj.seller
                        }
                        self.results_data["data"].append(product_dict)
                        print(f"[INFO] Successfully scraped product details for URL: {url}")
                    except Exception as e:
                        print(f"[ERROR] Failed to scrape product details: {e}")
                        continue

            # Update timestamps
            current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            self.results_data["createdAt"] = current_time
            self.results_data["updatedAt"] = current_time

            # Logout process
            try:
                sb.cdp.evaluate("""
                    let element = document.querySelector("div.navbar__username");
                    if (element) {
                        let event = new MouseEvent('mouseover', { bubbles: true });
                        element.dispatchEvent(event);
                    }
                """)
                sb.sleep(1)
                sb.cdp.mouse_click(
                    "button.navbar-account-drawer__button.navbar-account-drawer__button--complement.navbar-user-link.reset-button-style"
                )
                print("[INFO] Successfully logged out.")
            except Exception as e:
                raise RuntimeError(f"[ERROR] Logout failed: {e}")

            sb.sleep(3)
            print("[INFO] Browser closed. Scraping process completed.")

    def after_scrape(self):
        print("[INFO] Printing results...")
        print(json.dumps(self.results_data, ensure_ascii=False, indent=4))
