import pytest
from Lameh.src.pages.LoginPage import LoginPage

@pytest.mark.usefixtures("setup_chrome")
class TestLoginNegative:

    @pytest.mark.tcid1
    def test_login_none_existing_user(self):
        # go to login
        # type wrong email
        # click send code
        # assert error

        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        login_page.input_email("asdasdasd")
        login_page.click_send_code()