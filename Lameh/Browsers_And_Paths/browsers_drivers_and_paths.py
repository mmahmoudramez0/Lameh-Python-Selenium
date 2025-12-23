import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.opera import OperaDriverManager

class Setup():
    def __init__(self):
        pass
    @pytest.fixture(scope="class")
    def setup_chrome(self):
        driver_path = ChromeDriverManager().install()
        path = Service(driver_path)

        driver = webdriver.Chrome(service=path)
        driver.get("https://the-internet.herokuapp.com/")
        return driver

    def setup_oprea(self):
        driver_path = OperaDriverManager().install()
        options = Options()
        options.binary_location = r"C:\Users\loq\AppData\Local\Programs\Opera\opera.exe"
        options.add_argument("--remote-allow-origins=*")
        options.add_experimental_option('w3c', True)

        path = Service(driver_path)

        driver = webdriver.Chrome(service=path,options=options)

        driver.get("https://the-internet.herokuapp.com/")
        return driver






