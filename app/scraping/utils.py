# app/scraping/utils.py

class ScrapeUtils:
    @staticmethod
    def scroll_page(sb, scroll_step=750, max_scroll_retries=2, sleep_time=0.7):
        scroll_position = 0
        retries = 0
        while retries < max_scroll_retries:
            try:
                print("Scrolling to load more items...")
                sb.cdp.evaluate(f"window.scrollTo({scroll_position}, {scroll_position + scroll_step});")
                scroll_position += scroll_step
                sb.sleep(sleep_time)

                new_height = sb.cdp.evaluate("return document.body.scrollHeight")
                if scroll_position >= new_height:
                    retries += 1
                    print(f"No new items loaded. Retry {retries}/{max_scroll_retries}...")
                else:
                    retries = 0
            except Exception as e:
                raise RuntimeError(f"[ERROR] Error during scrolling: {e}")

    @staticmethod
    def parse_int_from_text(text, default=0):
        try:
            return int(text)
        except Exception as e:
            raise ValueError(f"[ERROR] Failed to parse integer from text '{text}': {e}")

