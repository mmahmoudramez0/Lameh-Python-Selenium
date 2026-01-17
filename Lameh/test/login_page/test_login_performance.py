import pytest
import time
from Lameh.src.pages.LoginPage import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("setup_chrome")
class TestLoginPerformance:
    """Performance test cases for login page"""

    @pytest.mark.tcid9
    @pytest.mark.performance
    def test_login_page_loads_within_acceptable_time(self):
        """
        Verify login page loads within acceptable time threshold.
        
        Steps:
        1. Record start time
        2. Navigate to login page
        3. Wait for critical element to be visible
        4. Record end time
        5. Assert load time is under threshold
        
        Threshold: 5 seconds (adjust based on requirements)
        """
        login_page = LoginPage(self.driver)
        
        start_time = time.time()
        
        login_page.go_to_login_page()
        
        # Wait for the email input to be visible (page is considered loaded)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
        )
        
        end_time = time.time()
        load_time = end_time - start_time
        
        # Threshold of 5 seconds for page load
        max_load_time = 5.0
        
        assert load_time < max_load_time, \
            f"Login page load time ({load_time:.2f}s) exceeded threshold ({max_load_time}s)"
        
        print(f"Login page loaded in {load_time:.2f} seconds")

    @pytest.mark.tcid10
    @pytest.mark.performance
    def test_send_code_button_response_time(self):
        """
        Verify Send Code button responds within acceptable time.
        
        Steps:
        1. Navigate to login page
        2. Enter a test email
        3. Click Send Code and measure response time
        4. Verify response is received within threshold
        
        Threshold: 3 seconds for UI feedback
        """
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        
        # Enter a test email (non-existing to avoid actual code send)
        login_page.input_email("performance_test@nonexistent.com")
        
        start_time = time.time()
        
        login_page.click_send_code()
        
        # Wait for any response (error message or success indicator)
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: 
                    len(driver.find_elements(By.XPATH, "//*[contains(text(), 'Couldn')]")) > 0 or
                    len(driver.find_elements(By.XPATH, "//*[contains(text(), 'Code')]")) > 0 or
                    len(driver.find_elements(By.CSS_SELECTOR, "[class*='error']")) > 0 or
                    len(driver.find_elements(By.CSS_SELECTOR, "[class*='success']")) > 0
            )
        except:
            pass  # Timeout is also a valid measurement
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Threshold of 3 seconds for button response
        max_response_time = 3.0
        
        assert response_time < max_response_time, \
            f"Button response time ({response_time:.2f}s) exceeded threshold ({max_response_time}s)"
        
        print(f"Send Code button responded in {response_time:.2f} seconds")

    @pytest.mark.tcid11
    @pytest.mark.performance
    def test_page_navigation_timing_api(self):
        """
        Use Navigation Timing API to measure detailed page performance.
        
        Measures:
        - DOM Content Loaded time
        - Full page load time
        - Time to First Byte (TTFB)
        """
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        
        # Wait for page to fully load
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
        )
        
        # Get performance timing data
        timing = self.driver.execute_script("""
            const timing = performance.timing;
            return {
                navigationStart: timing.navigationStart,
                responseStart: timing.responseStart,
                domContentLoadedEventEnd: timing.domContentLoadedEventEnd,
                loadEventEnd: timing.loadEventEnd
            };
        """)
        
        # Calculate metrics
        ttfb = timing['responseStart'] - timing['navigationStart']
        dom_loaded = timing['domContentLoadedEventEnd'] - timing['navigationStart']
        full_load = timing['loadEventEnd'] - timing['navigationStart']
        
        print(f"Performance Metrics:")
        print(f"  - Time to First Byte (TTFB): {ttfb}ms")
        print(f"  - DOM Content Loaded: {dom_loaded}ms")
        print(f"  - Full Page Load: {full_load}ms")
        
        # Assert reasonable thresholds
        assert ttfb < 1000, f"TTFB ({ttfb}ms) should be under 1000ms"
        assert dom_loaded < 3000, f"DOM loaded ({dom_loaded}ms) should be under 3000ms"
