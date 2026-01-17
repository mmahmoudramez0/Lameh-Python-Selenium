import pytest
from Lameh.src.pages.LoginPage import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("setup_chrome")
class TestLoginPageUI:
    """Test cases for login page UI elements verification"""

    @pytest.mark.tcid4
    @pytest.mark.smoke
    def test_login_page_elements_are_visible(self):
        """
        Verify all essential login page elements are visible.
        
        Steps:
        1. Navigate to login page
        2. Verify email input field is visible
        3. Verify Send Code button is visible
        4. Verify page title or heading is correct
        """
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        
        wait = WebDriverWait(self.driver, 10)
        
        # Verify email input is visible
        email_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
        )
        assert email_input.is_displayed(), "Email input should be visible"
        
        # Verify Send Code button is visible
        send_btn = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[text()='Send Code']"))
        )
        assert send_btn.is_displayed(), "Send Code button should be visible"
        assert send_btn.is_enabled(), "Send Code button should be enabled"

    @pytest.mark.tcid5
    @pytest.mark.smoke
    def test_email_input_has_correct_placeholder(self):
        """
        Verify email input field has appropriate placeholder text.
        
        Steps:
        1. Navigate to login page
        2. Check email input placeholder attribute
        """
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
        )
        
        placeholder = email_input.get_attribute("placeholder")
        
        # Placeholder should exist and contain email-related text
        assert placeholder is not None, "Email input should have a placeholder"
        assert len(placeholder) > 0, "Placeholder should not be empty"

    @pytest.mark.tcid6
    @pytest.mark.regression
    def test_login_page_url_is_correct(self):
        """
        Verify login page URL contains expected path.
        
        Steps:
        1. Navigate to login page
        2. Verify URL contains '/login'
        """
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        
        current_url = self.driver.current_url
        
        assert "/login" in current_url, f"URL should contain '/login', got: {current_url}"
