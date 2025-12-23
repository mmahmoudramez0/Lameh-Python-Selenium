import re

from selenium.webdriver.common.by import By
import pytest
import time
from selenium.webdriver.common.window import WindowTypes # For Selenium 4+
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from Lameh.src.pages import LoginPage

from selenium.common.exceptions import TimeoutException




@pytest.mark.usefixtures("setup_chrome")
class Test_Login:

    def test_login_with_email_code(self):

        self.driver.delete_all_cookies()

        # 1. CLEANUP PHASE
        # Go to the app to set the domain context
        self.driver.get("https://frontend-dev-36462279645.me-central2.run.app")

        # Nuke everything (Storage + Cookies)
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")
        self.driver.delete_all_cookies()

        # 2. FORCE NAVIGATION (Crucial Step)
        # Don't just refresh; explicitly go to the login page to verify the session is gone
        self.driver.get("https://frontend-dev-36462279645.me-central2.run.app/login")

        # 3. VERIFY WE ARE LOGGED OUT
        # Wait until the Email Input is visible. If this times out, the logout failed.
        email_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_input.clear()
        email_input.send_keys("m.ramez@lameh.ai")


        success_indicator = (By.CSS_SELECTOR, "div.go2072408551")

        send_btn_loc = self.driver.find_element(By.XPATH, "//button[text()='Send Code']")
        send_btn_loc.click()



        # Run the robust clicker
        safe_click(self.driver, send_btn_loc, success_indicator)


        # Store the ID of the original tab so we can come back later
        original_tab = self.driver.current_window_handle

        # --- 2. Open New Tab & Go to Gmail ---
        # This command creates a new tab and automatically switches focus to it
        self.driver.switch_to.new_window('tab')
        self.driver.get("https://gmail.com")

        # (Assuming you are already logged into Gmail or handle login here)

        # --- 3. The "Wait & Refresh" Loop ---
        # We need a custom loop because standard waits don't press 'Refresh'

        # 1. Calculate the "Target Time" strings to look for
        # We check "Now" and "1 minute ago" to handle clock skew/delays
        now = datetime.now()
        time_signatures = [
            now.strftime("%#I:%M %p"),  # <--- Change - to #
            (now - timedelta(minutes=1)).strftime("%#I:%M %p")
        ]
        # NOTE: On Windows, use %#I instead of %-I to remove leading zeros (06:00 -> 6:00)
        # If on Linux/Mac, keep %-I.

        print(f"Looking for email arriving at: {time_signatures}")

        # --- 3. The "Wait & Refresh" Loop ---

        email_found = False
        verification_code = None
        max_retries = 10
        tolerance_minutes = 5

        for i in range(max_retries):
            now = datetime.now()

            # 1. Generate acceptable times (Standardizing on Normal Spaces)
            time_signatures = []
            for m in range(tolerance_minutes + 1):
                past_time = now - timedelta(minutes=m)
                raw_time = past_time.strftime("%I:%M %p")  # "07:12 PM"
                stripped_time = raw_time.lstrip("0")  # "7:12 PM"
                time_signatures.extend([raw_time, stripped_time])

            print(f"Attempt {i + 1}: Looking for: {time_signatures}")

            try:
                email_rows = self.driver.find_elements(By.XPATH, "//tr[contains(., '[Development]')]")

                if not email_rows:
                    print("No emails found yet. Refreshing...")
                    self.driver.refresh()
                    time.sleep(5)
                    continue

                # 2. Get text and CLEAN IT (The Fix!)
                latest_email_row = email_rows[0]
                # Replace the hidden "Narrow No-Break Space" (\u202f) with a normal space
                row_text = latest_email_row.text.replace('\u202f', ' ')

                # 3. Check Time
                is_fresh = any(ts in row_text for ts in time_signatures)

                if is_fresh:
                    print(f"Fresh email found! Row text: {row_text}")

                    # 4. Extract Code
                    match = re.search(r"\[Development\]\s+(\d+)", row_text)

                    if match:
                        verification_code = match.group(1)
                        email_found = True
                        print(f"SUCCESS: Extracted Code -> {verification_code}")
                        break
                    else:
                        print("Time matched, but Regex failed to find the digits.")
                else:
                    print(f"Top email is old/mismatch. \n   Seen: '{row_text}' \n   Wanted: {time_signatures}")
                    self.driver.refresh()
                    time.sleep(5)

            except Exception as e:
                print(f"Error: {e}")
                self.driver.refresh()
                time.sleep(5)

        # --- 4. Assertions ---
        # Fail the test properly if we didn't get the code
        assert email_found is True, "Failed to find a fresh email with the verification code."
        assert verification_code is not None, "Email was found, but code extraction returned None."

        if not email_found:
            pytest.fail(f"New verification email never arrived within {max_retries * 5} seconds.")

        print(f"FINAL CODE: {verification_code}")
        # --- 5. Switch Back & Finish ---
        self.driver.close()  # Close the Gmail tab (optional but clean)
        self.driver.switch_to.window(original_tab)  # Jump back to app

        # Input the code
        self.driver.find_element(By.CSS_SELECTOR, "input[class='disabled:cursor-not-allowed']").send_keys(verification_code)
        self.driver.find_element(By.XPATH, "//button[text()='Verify Code']").click()

    def test_invalid_login(self):
        # Notice we can use 'self.driver' now because of the request!
        title = self.driver.title
        print(f"Page Title is: {title}")



    @pytest.mark.regression
    def test_dummy_func2(self):
        print("Testing regression Function")


    @pytest.mark.regression
    def test_dummy_func3(self):
        print("Testing regression Function")
