import allure
from selenium.webdriver.support import expected_conditions as ec

from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    @allure.step("Open main page")
    def open_main(self, base_url: str):
        self.open(base_url)

    @allure.step("Accept cookies (if banner is present)")
    def accept_cookies_if_present(self):
        try:
            self.driver.find_element(*MainPageLocators.COOKIE_ACCEPT_BUTTON).click()
        except Exception:
            pass

    @allure.step("Click 'Order' button (entry point: {entry})")
    def click_order_button(self, entry: str):
        if entry == "top":
            self.click(MainPageLocators.ORDER_BUTTON_TOP)
            return

        if entry == "bottom":
            self.scroll_into_view(MainPageLocators.ORDER_BUTTON_BOTTOM)
            self.click(MainPageLocators.ORDER_BUTTON_BOTTOM)
            return

        raise ValueError("entry must be 'top' or 'bottom'")

    @allure.step("Open FAQ question #{index}")
    def open_faq_question(self, index: int):
        self.scroll_into_view(MainPageLocators.faq_question(index))
        self.click(MainPageLocators.faq_question(index))

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
