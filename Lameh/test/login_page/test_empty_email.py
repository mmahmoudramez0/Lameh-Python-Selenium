import pytest
from Lameh.src.pages.LoginPage import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("setup_chrome")
class TestEmptyEmail:
    """Test cases for empty email field validation"""

    @pytest.mark.tcid2
    @pytest.mark.smoke
    def test_login_with_empty_email_shows_validation(self):
        """
        Verify that submitting login form with empty email shows validation error.
        
        Steps:
        1. Navigate to login page
        2. Leave email field empty
        3. Click Send Code button
        4. Verify HTML5 validation or custom error message appears
        """
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        
        # Click send code without entering email
        login_page.click_send_code()
        
        # Check if the email input has validation error (HTML5 required attribute)
        email_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        
        # Verify the field is marked as invalid or shows validation message
        is_valid = self.driver.execute_script(
            "return arguments[0].checkValidity();", 
            email_input
        )
        
        assert is_valid is False, "Empty email should trigger validation error"
