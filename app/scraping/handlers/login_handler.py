# app/scraping/handlers/login_handler.py

class LoginHandler:
    """
    Handles Shopee login process.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, sb):
        print("[INFO] Logging in...")
        try:
            sb.cdp.focus("input[name='loginKey']")
            sb.cdp.press_keys("input[name='loginKey']", self.username)
            print("[INFO] Successfully entered username.")
        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to enter username: {e}")

        sb.sleep(1)

        try:
            sb.cdp.focus("input[name='password']")
            sb.cdp.press_keys("input[name='password']", self.password)
            print("[INFO] Successfully entered password.")
        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to enter password: {e}")

        sb.sleep(1)

        try:
            sb.cdp.mouse_click("button.b5aVaf")
            print("[INFO] Login button clicked. Solve CAPTCHA manually if prompted.")
        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to click login button: {e}")

        sb.sleep(2)

        try:
            sb.wait_for_element_visible(
                "shopee-banner-popup-stateful::shadow div.shopee-popup__close-btn",
                timeout=5
            )
            try: 
                sb.click("shopee-banner-popup-stateful::shadow div.shopee-popup__close-btn")
                print("[INFO] Successfully closed popup.")     
            except Exception:
                print(f"[ERROR] Failed to close popup")
               
        except Exception:
            print(f"[INFO] No banner popup detected or unable to close popup")

   




