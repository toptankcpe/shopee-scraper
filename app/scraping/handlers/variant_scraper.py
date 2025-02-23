# app/scraping/handlers/variant_scraper.py

class VariantScraper:
    """
    Handles selection of product options (color, size, etc.) and collects price/stock.
    """
    def __init__(self):
        self.results = []

    def get_option_categories(self, sb):
        filtered_categories = []
        try:
            categories = sb.cdp.find_elements("section[class='flex items-center'] h3", timeout=3)
            filtered_categories = [cat.text for cat in categories]
            print(f"[INFO] Successfully retrieved {len(categories)} option categories.")
        except Exception as e:
            print(f"[ERROR] No categories found: {e}")
        return filtered_categories

    def get_option_buttons(self, sb, category_name):
        try:
            buttons = []
            sections = sb.cdp.find_elements("section[class='flex items-center']", timeout=10)
            for section in sections:
                h3 = section.query_selector("h3.Dagtcd")
                if h3 and h3.text == category_name:
                    buttons.extend(section.query_selector_all("button"))
                    break
            enabled_buttons = [b for b in buttons if b.get_attribute("aria-disabled") != "true"]
            print(f"[INFO] Successfully retrieved {len(enabled_buttons)} enabled buttons for category '{category_name}'.")
            return enabled_buttons
        except Exception as e:
            print(f"[ERROR] Error fetching buttons for category '{category_name}': {e}")
            return []

    def scrape_price_and_stock(self, sb):
        try:
            sb.cdp.wait_for_element_visible("div[class='IZPeQz B67UQ0']", timeout=10)
            price_text = sb.cdp.get_text("div[class='IZPeQz B67UQ0']")
            price = price_text.replace('฿', '').strip()
            print(f"[INFO] Successfully retrieved price: {price}")
        except Exception as e:
            price = "Price not found"
            print(f"[ERROR] Failed to retrieve price: {e}")

        try:
            sb.cdp.wait_for_element_visible("div[class='flex items-center']", timeout=10)
            stock_element = sb.cdp.get_text("div[class='flex items-center'] > div:last-child")
            print(f"[INFO] Successfully retrieved stock element: {stock_element}")
            stock = int(stock_element.split()[0])
        except Exception as e:
            stock = "Stock not found"
            print(f"[ERROR] Failed to retrieve stock: {e}")

        return price, stock

    def select_and_scrape(self, sb, option_categories, selected_options=None):
        print(option_categories)
        if selected_options is None:
            selected_options = {}

        if not option_categories: # 如果在最後一層選單
            price, stock = self.scrape_price_and_stock(sb)
            self.results.append({
                "options": selected_options,
                "price": price,
                "stock": stock
            })
            print(f"[INFO] Selected options: {selected_options}, Price: {price}, Stock: {stock}")
            return

        current_category = option_categories[0]
        buttons = self.get_option_buttons(sb, current_category)
        for idx, btn in enumerate(buttons):
            try:
                btn.save_to_dom()
                sb.sleep(1)
                btn.flash(duration=0.5, color="EE4488")
                btn.mouse_move()
                sb.sleep(1)
                btn.mouse_click()
                sb.sleep(1)
                print(f"[INFO] Successfully selected option '{btn.get_attribute('aria-label')}' for category '{current_category}'.")
            except Exception as e:
                print(f"[ERROR] Failed to select option for category '{current_category}': {e}")
                continue
            
            self.select_and_scrape(
                sb, 
                option_categories[1:], 
                {**selected_options, current_category: btn.get_attribute("aria-label")}
            )            
            
            if idx == len(buttons)-1: #deselect button if it's the end of second layer
                btn.save_to_dom()
                sb.sleep(1)
                btn.mouse_click()
                sb.sleep(1)

