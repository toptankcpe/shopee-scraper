# app/scraping/handlers/product_scraper.py

import re
from ..models import ProductData
from ..utils import ScrapeUtils

class ProductScraper:
    """
    Handles for collecting main product details, such as name, price, description, rating, and seller.
    """
    def __init__(self, variant_scraper):
        self.variant_scraper = variant_scraper

    def scrape_product_details(self, sb, url):
        sb.cdp.get(url)
        sb.sleep(3)

        # Extract seller_id, product_id
        match = re.search(r"i\.(\d+)\.(\d+)", url)
        if match:
            seller_id = match.group(1)
            product_id = match.group(2)
            print(f"Seller ID: {seller_id}")
            print(f"Product ID: {product_id}")
        else:
            seller_id = None
            product_id = None
            print("Seller ID and Product ID not found in URL.")

        # Name
        try:
            sb.cdp.wait_for_element_visible("//div[@class='WBVL_7']//span", timeout=10)
            product_name = sb.cdp.get_text("//div[@class='WBVL_7']//span")
        except Exception as e:
            print(f"Error getting product name: {e}")
            product_name = ""

        # Description
        try:
            description_elements = sb.cdp.find_elements("//div[@class='e8lZp3']//p[@class='QN2lPu']", timeout=10)
            product_description = "\n".join([elem.text for elem in description_elements])
        except Exception as e:
            print(f"Error during description: {e}")
            product_description = ""

        # Price
        min_price = max_price = "0"
        try:
            sb.cdp.wait_for_element_visible("//div[@class='IZPeQz B67UQ0']", timeout=10)
            product_price = sb.cdp.get_text("//div[@class='IZPeQz B67UQ0']")
            price_text_clean = product_price.replace('฿', '').strip()
            if '-' in price_text_clean:
                min_price, max_price = price_text_clean.split('-')
                min_price = min_price.strip()
                max_price = max_price.strip()
            else:
                min_price = max_price = price_text_clean
        except Exception as e:
            print(f"Error during price: {e}")

        # Stock
        product_quantity = 0
        try:
            sb.cdp.wait_for_element_visible("//div[@class='flex items-center']//div[contains(text(), 'pieces')]", timeout=10)
            available_quantity = sb.cdp.get_text("//div[@class='flex items-center']//div[contains(text(), 'pieces')]")
            product_quantity = ScrapeUtils.parse_int_from_text(available_quantity.split()[0], default=0)
        except Exception as e:
            print(f"Error during quantity: {e}")

        # Category
        category_path = []
        try:
            cat_elements = sb.cdp.find_elements("//div[contains(@class, 'idLK2l')]//a[@class='EtYbJs R7vGdX']", timeout=10)
            category_path = [el.text for el in cat_elements]
        except Exception as e:
            print(f"Error during category path: {e}")

        # Variants
        self.variant_scraper.results.clear()
        option_categories = self.variant_scraper.get_option_categories(sb)
        self.variant_scraper.select_and_scrape(sb, option_categories)
        
        all_variants = []
        for res in self.variant_scraper.results:
            variant_dict = {
                "options": {},
                "price": res["price"],
                "stock": res["stock"]
            }
            for cat in option_categories:
                variant_dict["options"][cat] = res["options"].get(cat, "")
            all_variants.append(variant_dict)

        # Rating
        average = None
        review_count = 0
        sold_element = 0
        star_counts = {"1": "0", "2": "0", "3": "0", "4": "0", "5": "0"}

        try:
            sb.cdp.wait_for_element_visible("button[class='flex e2p50f'] div[class='F9RHbS dQEiAI jMXp4d']", timeout=3)
            rating_element_2 = sb.cdp.get_text("button[class='flex e2p50f'] div[class='F9RHbS dQEiAI jMXp4d']")
            average = float(rating_element_2)

            sb.cdp.wait_for_element_visible("button[class='flex e2p50f'] div[class='F9RHbS']", timeout=3)
            rating_element_3 = sb.cdp.get_text("button[class='flex e2p50f'] div[class='F9RHbS']")
            review_count = rating_element_3
        except Exception as e:
            print(f"Error fetching rating/review: {e}")

        # Sold
        try:
            sb.cdp.wait_for_element_visible("div[class='flex mnzVGI'] span[class='AcmPRb']", timeout=10)
            sold_element = sb.cdp.get_text("div[class='flex mnzVGI'] span[class='AcmPRb']")
        except Exception as e:
            print(f"Error fetching sold element: {e}")

        # Star breakdown
        for star_text in ["1 star", "2 star", "3 star", "4 star", "5 star"]:
            try:
                sb.cdp.wait_for_element_visible(
                    f"div[class='product-rating-overview__filters'] div:contains('{star_text}')",
                    timeout=3
                )
                star_element = sb.cdp.get_text(f"div[class='product-rating-overview__filters'] div:contains('{star_text}')")
                star_num = star_element.split('(')[-1].split(')')[0]
                star_counts[star_text.split()[0]] = star_num
            except Exception as e:
                star_counts[star_text.split()[0]] = "0"

        rating_data = {
            "average": average,
            "reviewCount": review_count,
            "sold": sold_element,
            "starRating": star_counts
        }

        # Seller
        seller_name = "Unknown"
        seller_rating = "N/A"
        seller_response_rate = "N/A"
        seller_joined = "N/A"
        seller_products = "N/A"
        seller_response_time = "N/A"
        seller_follower = "N/A"

        try:
            sb.cdp.wait_for_element_visible("div[class='fV3TIn']", timeout=10)
            seller_name = sb.cdp.get_text("div[class='fV3TIn']")

            sb.cdp.wait_for_element_visible("a[class='YnZi6x aArpoe']", timeout=10)
            seller_products = sb.cdp.get_text("a[class='YnZi6x aArpoe'] span")

            seller_element = sb.cdp.find_elements("div[class='YnZi6x']", timeout=10)
            for sel in seller_element:
                label = sel.query_selector("label.ffHYws")
                span = sel.query_selector("span.Cs6w3G")
                if label and span:
                    if label.text == "Ratings":
                        seller_rating = span.text
                    elif label.text == "response rate":
                        seller_response_rate = span.text
                    elif label.text == "joined":
                        seller_joined = span.text
                    elif label.text == "response time":
                        seller_response_time = span.text
                    elif label.text == "follower":
                        seller_follower = span.text
        except Exception as e:
            print(f"Error fetching seller info: {e}")

        seller_data = {
            "id": seller_id,
            "name": seller_name,
            "rating": seller_rating,
            "responseRate": seller_response_rate,
            "joined": seller_joined,
            "product": seller_products,
            "responseTime": seller_response_time,
            "follower": seller_follower,
        }

        product_obj = ProductData(
            product_id=product_id,
            product_name=product_name,
            product_description=product_description,
            price_range=(min_price, max_price),
            total_quantity=product_quantity,
            category_path=category_path,
            url=url,
            variants=all_variants,
            rating=rating_data,
            seller=seller_data
        )

        return product_obj
