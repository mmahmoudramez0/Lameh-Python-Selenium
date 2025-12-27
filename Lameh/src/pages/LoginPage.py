
from Lameh.src.pages.Locators.LoginPageLocators import LoginPageLocators
from Lameh.src.helpers.SeleniumHelpers import SeleniumHelpers
from Lameh.src.helpers.EnvHelper import get_base_url


class LoginPage(LoginPageLocators):
    endpoint = '/login'
    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumHelpers(self.driver)

    def go_to_login_page(self):
        base_url = get_base_url()
        login_url = base_url + self.endpoint
        self.driver.get(login_url)

    def input_email(self, email_address):
        self.sl.wait_and_input_text(self.INPUT_EMAIL, email_address)


    def input_password(self, password):
        self.sl.wait_and_input_text(self.INPUT_PASSWORD, password)

    def click_send_code(self):
        self.sl.wait_and_click(self.SEND_BTN_LOCATOR)
