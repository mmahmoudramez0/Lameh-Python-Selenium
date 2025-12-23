# Lameh AI - Selenium Test Automation Framework

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green.svg)](https://selenium.dev)
[![pytest](https://img.shields.io/badge/pytest-7.x-yellow.svg)](https://pytest.org)

A scalable test automation framework for Lameh AI's fintech web application, built with Selenium WebDriver and Python using the Page Object Model (POM) design pattern.

---

## 🏗️ Architecture

```
Lameh-Python-Selenium/
├── Lameh/
│   └── src/
│       ├── pages/              # Page Object classes
│       │   ├── LoginPage.py
│       │   ├── DashboardPage.py
│       │   ├── AnalysisPage.py
│       │   └── Locators/       # Element locators (separated)
│       ├── helpers/            # Reusable Selenium utilities
│       │   └── SeleniumHelpers.py
│       └── configs/            # Configuration files
├── test/
│   ├── conftest.py             # pytest fixtures & setup
│   └── test_main.py            # Test cases
├── allure_reports/             # Test execution reports
├── pytest.ini                  # pytest configuration
└── requirements.txt            # Python dependencies
```

---

## ✨ Features

- **Page Object Model (POM)** — Clean separation of test logic and page interactions
- **pytest Framework** — Powerful test execution with fixtures and markers
- **Explicit Waits** — Robust element handling with WebDriverWait
- **Custom Helpers** — Reusable Selenium utility functions
- **Allure Reporting** — Detailed HTML test reports
- **pytest Markers** — Organize tests by type (regression, smoke, etc.)
- **Cross-browser Support** — Configurable browser options

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Chrome Browser
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/mmahmoudramez0/Lameh-Python-Selenium.git
cd Lameh-Python-Selenium

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific marker
pytest -m regression

# Generate HTML report
pytest --html=my_report.html

# Generate Allure report
pytest --alluredir=allure_reports
allure serve allure_reports
```

---

## 🧪 Test Examples

### Page Object Usage

```python
from Lameh.src.pages.LoginPage import LoginPage

def test_login(driver):
    login_page = LoginPage(driver)
    login_page.input_email("user@example.com")
    login_page.input_password("password123")
    login_page.click_login()
```

### Using Fixtures

```python
@pytest.mark.usefixtures("setup_chrome")
class TestLogin:
    
    def test_valid_login(self):
        # self.driver is injected by fixture
        self.driver.get("https://app.example.com/login")
        # ... test steps
    
    @pytest.mark.regression
    def test_invalid_login(self):
        # ... test steps
```

---

## 📊 Reporting

| Report Type | Command | Output |
|-------------|---------|--------|
| Console | `pytest -v` | Terminal |
| HTML | `pytest --html=report.html` | HTML file |
| Allure | `pytest --alluredir=allure_reports` | Interactive HTML |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.10+ | Programming language |
| Selenium WebDriver 4.x | Browser automation |
| pytest 7.x | Test framework |
| pytest-html | HTML reporting |
| Allure | Advanced reporting |
| webdriver-manager | Automatic driver management |

---

## 👤 Author

**Mahmoud Ramez** — SDET | Test Automation Engineer

- LinkedIn: [mahmoud-ramez](https://linkedin.com/in/mahmoud-ramez)
- GitHub: [@mmahmoudramez0](https://github.com/mmahmoudramez0)
- Email: mahmoudramez1997@gmail.com

---

## 📄 License

This project is licensed under the MIT License.
