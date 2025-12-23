from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Lameh.src.pages.Locators.LoginPageLocators import LoginPageLocators
from selenium.webdriver.support.wait import WebDriverWait
from Lameh.src.helpers.SeleniumHelpers import SeleniumHelpers


class LoginPage(LoginPageLocators):

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumHelpers(self.driver)

    def input_email(self, email_address):
        self.sl.wait_and_input_text(self.INPUT_EMAIL, email_address)


    def input_password(self, password):
        self.sl.wait_and_input_text(self.INPUT_PASSWORD, password)

    def click_login(self):
        self.sl.wait_and_click(self.SEND_BTN_LOCATOR)









    def safe_click(driver, button_locator, success_locator):
        """
        Clicks a button and waits for a 'success' element to appear.
        If it fails, it retries the click.
        """
        max_retries = 10
        for attempt in range(max_retries):
            try:
                print(f"Click Attempt {attempt + 1}...")

                # 1. Find the button and Click
                btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(button_locator))

                # Try JS Click if standard click is flaky
                driver.execute_script("arguments[0].click();", btn)

                # 2. WAIT for the consequence (The "Proof" it worked)
                # We wait 3 seconds for the "success indicator" to appear
                WebDriverWait(driver, 3).until(EC.visibility_of_element_located(success_locator))

                print("Click successful! UI responded.")
                return  # Exit function, we are done

            except TimeoutException:
                print("UI did not respond. Clicking again...")

        raise Exception(f"Failed to click button {button_locator} after {max_retries} attempts")
