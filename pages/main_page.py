import allure
from selenium.webdriver.support import expected_conditions as ec

from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from pages.order_page import OrderPage
from pages.rent_page import RentPage


class MainPage(BasePage):
    @allure.step("Open main page")
    def open_main(self, base_url: str):
        self.open(base_url)

    @allure.step("Accept cookies (if banner is present)")
    def accept_cookies_if_present(self):
        self.click_if_present(MainPageLocators.COOKIE_ACCEPT_BUTTON)

    @allure.step("Click 'Order' button (top entry)")
    def click_order_button_top(self):
        self.click(MainPageLocators.ORDER_BUTTON_TOP)

    @allure.step("Click 'Order' button (bottom entry)")
    def click_order_button_bottom(self):
        self.click(MainPageLocators.ORDER_BUTTON_BOTTOM)

    @allure.step("Open FAQ question #{index}")
    def open_faq_question(self, index: int):
        self.scroll_into_view(MainPageLocators.faq_question(index))
        self.safe_click(MainPageLocators.faq_question(index))

    @allure.step("Get FAQ answer text for question #{index}")
    def get_faq_answer_text(self, index: int) -> str:
        return self.text_of(MainPageLocators.faq_answer(index))

    @allure.step("Click 'Scooter' logo")
    def click_scooter_logo(self):
        self.click(MainPageLocators.SCOOTER_LOGO)

    @allure.step("Click 'Yandex' logo (opens a new window/tab)")
    def click_yandex_logo(self):
        self.click(MainPageLocators.YANDEX_LOGO)

    @allure.step("Wait until main page is loaded")
    def wait_main_page_loaded(self):
        self.wait.until(ec.element_to_be_clickable(MainPageLocators.ORDER_BUTTON_TOP))
        self.wait.until(ec.element_to_be_clickable(MainPageLocators.YANDEX_LOGO))

    @allure.step("Assert main page URL equals base_url")
    def assert_current_url_is(self, expected_url: str):
        current_url = self.get_current_url()
        assert current_url == expected_url, (
            f"Ожидали URL '{expected_url}', получили '{current_url}'"
        )

    @allure.step("Click Yandex logo and switch to newly opened tab")
    def click_yandex_logo_and_switch_to_new_tab(self, timeout: int = 10):
        old_handles = self.get_window_handles()
        self.click_yandex_logo()

        self.wait_for_number_of_windows(len(old_handles) + 1, timeout)
        new_handles = self.get_window_handles()
        new_handle = [h for h in new_handles if h not in old_handles][0]
        self.switch_to_window(new_handle)

    @allure.step("Wait until current URL contains: {substring}")
    def wait_url_contains(self, substring: str, timeout: int = 10):
        super().wait_url_contains(substring, timeout)

    @allure.step("Assert current URL contains: {substring}")
    def assert_current_url_contains(self, substring: str):
        current_url = self.get_current_url()
        assert substring in current_url, (
            f"Expected '{substring}' in URL, got '{current_url}'"
        )

    @allure.step("Открыть главную, принять куки и нажать 'Заказать'")
    def open_and_start_order(self, base_url: str, entry_position: str = "top"):
        """
        entry_position: "top" или "bottom"
        """
        self.open_main(base_url)
        self.accept_cookies_if_present()
        
        if entry_position == "top":
            self.click_order_button_top()
        elif entry_position == "bottom":
            self.click_order_button_bottom()
        else:
            raise ValueError(f"Unknown entry_position: {entry_position}")