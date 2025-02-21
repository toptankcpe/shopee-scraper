# app/scraping/handlers/search_handler.py

class SearchHandler:
    """
    Handles product search in Shopee based on the provided keyword.
    """
    def __init__(self, keyword):
        self.keyword = keyword

    def search(self, sb):
        print(f"[INFO] Searching for keyword: {self.keyword}")
        try:
            sb.cdp.focus("input.shopee-searchbar-input__input")
            sb.sleep(0.5)
            sb.cdp.press_keys("input.shopee-searchbar-input__input", self.keyword)
            sb.sleep(1)
            print("[INFO] Successfully entered search keyword.")
        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to enter search keyword: {e}")

        try:
            sb.cdp.mouse_click("button.btn.btn-solid-primary.btn--s.btn--inline.shopee-searchbar__search-button")
            sb.sleep(2)
            print("[INFO] Successfully clicked search button.")
        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to click search button: {e}")

        total_pages = 1
        try:
            sb.cdp.wait_for_element_visible("span.shopee-mini-page-controller__total", timeout=10)
            total_pages = int(sb.cdp.get_text("span.shopee-mini-page-controller__total"))
            print(f"[INFO] Successfully retrieved total pages: {total_pages}")
        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to retrieve total pages: {e}")

        return total_pages



