from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_FORM = (By.XPATH, '//*[@id="loginForm"]')

    INPUT_EMAIL = (By.CSS_SELECTOR, 'input[type="email"]')
    INPUT_PASSWORD = (By.CSS_SELECTOR, 'input[type="password"]')
    SUCCESS_INDICATOR = (By.CSS_SELECTOR, "div.go2072408551")
    SEND_BTN_LOCATOR = (By.XPATH, "//button[text()='Send Code']")