import pytest
from Lameh.src.pages.LoginPage import LoginPage
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures("setup_chrome")
class TestInvalidEmailFormat:
    """Test cases for invalid email format validation"""

    @pytest.mark.tcid3
    @pytest.mark.regression
    @pytest.mark.parametrize("invalid_email", [
        "plainaddress",
        "@missingusername.com",
        "username@.com",
        "username@domain",
        "user name@domain.com",
        "username@domain..com",
    ])
    def test_login_with_invalid_email_format(self, invalid_email):
        """
        Verify that login form rejects various invalid email formats.
        
        Steps:
        1. Navigate to login page
        2. Enter invalid email format
        3. Click Send Code button
        4. Verify validation error appears
        
        Args:
            invalid_email: Various malformed email addresses
        """
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        
        # Enter invalid email
        login_page.input_email(invalid_email)
        
        # Attempt to submit
        login_page.click_send_code()
        
        # Check HTML5 email validation
        email_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        
        is_valid = self.driver.execute_script(
            "return arguments[0].checkValidity();", 
            email_input
        )
        
        # Either HTML5 validation catches it, or we stay on login page
        current_url = self.driver.current_url
        
        assert is_valid is False or "/login" in current_url, \
            f"Invalid email '{invalid_email}' should not be accepted"
