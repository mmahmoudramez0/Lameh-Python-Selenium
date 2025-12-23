import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="class")
def setup_chrome(request):
    # --- 1. SETUP ---
    print("\nSetting up Chrome Driver...")

    # --- 1. SETUP OPTIONS ---
    options = Options()

    # POINT TO YOUR CUSTOM FOLDER
    # IMPORTANT: Do not add the "\Default" at the end, Selenium adds it automatically
    options.add_argument(r"user-data-dir=C:\Users\loq\PycharmProjects\PythonProject1\SeleniumProfile")

    # Optional: Prevents "Chrome is being controlled by automated software" bar
    # options.add_argument("disable-infobars")

    # Install and setup the service
    driver_path = ChromeDriverManager().install()
    service_obj = Service(driver_path)

    # Initialize the driver
    driver = webdriver.Chrome(service=service_obj, options=options)

    # Optional: Set implicit wait or maximize
    driver.maximize_window()

    # Navigate to your base URL (if you want this for all tests in class)
    driver.get("https://frontend-dev-36462279645.me-central2.run.app/")

    # --- 2. INJECT INTO CLASS ---
    # This makes 'self.driver' available in your Test Class
    request.cls.driver = driver

    # --- 3. YIELD (Run the tests) ---
    yield driver

    # --- 4. TEARDOWN ---
    print("\nQuitting Chrome Driver...")
    driver.quit()