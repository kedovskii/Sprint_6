import allure
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from locators.order_page_locators import OrderPageLocators


class RentPage(BasePage):
    def rent_period_option(self, text: str):
        return ("xpath", f"//div[contains(@class,'Dropdown-menu')]//div[text()='{text}']")

    @allure.step("Select scooter color: black")
    def select_color_black(self):
        self.click(OrderPageLocators.COLOR_BLACK)

    @allure.step("Select scooter color: grey")
    def select_color_grey(self):
        self.click(OrderPageLocators.COLOR_GREY)

    @allure.step("Select scooter color: both")
    def select_color_both(self):
        self.click(OrderPageLocators.COLOR_BLACK)
        self.click(OrderPageLocators.COLOR_GREY)

    @allure.step("Заполнить шаг 2 формы заказа (без выбора цвета)")
    def fill_step_two(self, date_str, rent_period_text, comment):
        self.type(OrderPageLocators.DATE, date_str)
        self.find(OrderPageLocators.DATE).send_keys(Keys.ENTER)

        self.click(OrderPageLocators.RENT_PERIOD_DROPDOWN)
        self.click(self.rent_period_option(rent_period_text))

        if comment:
            self.type(OrderPageLocators.COMMENT, comment)

    @allure.step("Оформить заказ и подтвердить")
    def submit_and_confirm(self):
        self.click(OrderPageLocators.ORDER_BUTTON)
        self.click(OrderPageLocators.CONFIRM_YES_BUTTON)
        # Ждём, пока модалка подтверждения закроется
        self.wait.until(ec.invisibility_of_element_located(OrderPageLocators.CONFIRM_YES_BUTTON))

    @allure.step("Проверить, что заказ успешно создан (есть модалка)")
    def success_should_be_visible(self) -> str:
        # Явное ожидание видимости SUCCESS_MODAL
        self.wait.until(ec.visibility_of_element_located(OrderPageLocators.SUCCESS_MODAL))
        return self.text_of(OrderPageLocators.SUCCESS_TEXT)

    @allure.step("Click 'Check order status' button in success modal")
    def click_check_order_status_modal_button(self):
        self.wait.until(ec.visibility_of_element_located(OrderPageLocators.SUCCESS_MODAL))
        self.safe_click(OrderPageLocators.CHECK_ORDER_STATUS_MODAL_BUTTON)
        self.wait.until(ec.invisibility_of_element_located(OrderPageLocators.ORDER_OVERLAY))
        self.wait.until(ec.invisibility_of_element_located(OrderPageLocators.SUCCESS_MODAL))

    @allure.step("Wait overlay to disappear")
    def wait_overlay_to_disappear(self):
        self.wait.until(ec.invisibility_of_element_located(OrderPageLocators.ORDER_OVERLAY))

    @allure.step("Wait until success modal text contains order number")
    def wait_until_order_number_text_present(self):
        self.wait.until(ec.visibility_of_element_located(OrderPageLocators.SUCCESS_MODAL))
        self.wait.until(
            ec.text_to_be_present_in_element(
                OrderPageLocators.SUCCESS_MODAL_TEXT_BLOCK,
                "Номер заказа"
            )
        )

    @allure.step("Wait until order number appears in success modal")
    def wait_for_order_number_in_modal_text(self):
        self.wait.until(ec.visibility_of_element_located(OrderPageLocators.SUCCESS_MODAL))

        def _has_digits(driver):
            text = self.get_element_text(OrderPageLocators.SUCCESS_MODAL_TEXT_BLOCK)
            return any(ch.isdigit() for ch in text)

        self.wait.until(_has_digits)
