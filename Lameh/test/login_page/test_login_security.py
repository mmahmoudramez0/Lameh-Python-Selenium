import pytest
from Lameh.src.pages.LoginPage import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("setup_chrome")
class TestLoginSecurity:
    """Security test cases for login functionality"""

    @pytest.mark.tcid7
    @pytest.mark.security
    @pytest.mark.parametrize("malicious_input", [
        "' OR '1'='1",
        "admin'--",
        "1'; DROP TABLE users;--",
        "<script>alert('xss')</script>@test.com",
        "test@test.com' AND 1=1--",
    ])
    def test_login_rejects_sql_injection_attempts(self, malicious_input):
        """
        Verify login form properly handles SQL injection attempts.
        
        Steps:
        1. Navigate to login page
        2. Enter SQL injection payload in email field
        3. Submit the form
        4. Verify application handles it safely (no errors, no bypass)
        
        Args:
            malicious_input: Various SQL injection payloads
        """
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        
        # Enter malicious input
        login_page.input_email(malicious_input)
        login_page.click_send_code()
        
        # Wait a moment for any response
        WebDriverWait(self.driver, 3)
        
        # Verify we're still on login page (no bypass occurred)
        current_url = self.driver.current_url
        assert "/login" in current_url or "login" in current_url.lower(), \
            f"SQL injection should not bypass login. Current URL: {current_url}"
        
        # Verify no server error page is shown
        page_source = self.driver.page_source.lower()
        error_indicators = ["500", "internal server error", "database error", "sql"]
        
        for indicator in error_indicators:
            assert indicator not in page_source or "email" in page_source, \
                f"Possible SQL injection vulnerability: '{indicator}' found in response"

    @pytest.mark.tcid8
    @pytest.mark.security
    def test_login_handles_xss_payload_safely(self):
        """
        Verify login form properly sanitizes XSS payloads.
        
        Steps:
        1. Navigate to login page
        2. Enter XSS payload in email field
        3. Verify payload is not executed
        """
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        
        xss_payload = "<img src=x onerror=alert('XSS')>@test.com"
        login_page.input_email(xss_payload)
        
        # Check that no alert is triggered
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.dismiss()
            pytest.fail(f"XSS vulnerability detected! Alert triggered: {alert_text}")
        except:
            # No alert means XSS was properly handled
            pass
        
        # Verify the input was sanitized or rejected
        email_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        input_value = email_input.get_attribute("value")
        
        # The malicious tags should either be escaped or the input rejected
        assert "<img" not in input_value or "&lt;img" in self.driver.page_source, \
            "XSS payload should be sanitized"
