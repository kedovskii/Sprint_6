import allure
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from locators.order_page_locators import OrderPageLocators


class RentPage(BasePage):
    def rent_period_option(self, text: str):
        return ("xpath", f"//div[contains(@class,'Dropdown-menu')]//div[text()='{text}']")

    @allure.step("Заполнить шаг 2 формы заказа")
    def fill_step_two(self, date_str, rent_period_text, color, comment):
        # Дата
        self.type(OrderPageLocators.DATE, date_str)
        self.find(OrderPageLocators.DATE).send_keys(Keys.ENTER)

        # Срок аренды
        self.click(OrderPageLocators.RENT_PERIOD_DROPDOWN)
        self.click(self.rent_period_option(rent_period_text))

        # Цвет
        if color == "black":
            self.click(OrderPageLocators.COLOR_BLACK)
        elif color == "grey":
            self.click(OrderPageLocators.COLOR_GREY)
        elif color == "both":
            self.click(OrderPageLocators.COLOR_BLACK)
            self.click(OrderPageLocators.COLOR_GREY)

        # Комментарий
        if comment:
            self.type(OrderPageLocators.COMMENT, comment)

    @allure.step("Оформить заказ и подтвердить")
    def submit_and_confirm(self):
        self.click(OrderPageLocators.ORDER_BUTTON)
        self.click(OrderPageLocators.CONFIRM_YES_BUTTON)

    @allure.step("Проверить, что заказ успешно создан (есть модалка)")
    def success_should_be_visible(self) -> str:
        self.is_visible(OrderPageLocators.SUCCESS_MODAL)
        return self.text_of(OrderPageLocators.SUCCESS_TEXT)
    
    @allure.step("Click 'Check order status' button in success modal")
    def click_check_order_status_modal_button(self):
        # убеждаемся, что модалка появилась
        self.wait.until(ec.visibility_of_element_located(OrderPageLocators.SUCCESS_MODAL))

        # кликаем надёжно
        self.safe_click(OrderPageLocators.CHECK_ORDER_STATUS_MODAL_BUTTON)

        # ждём, что overlay исчезнет и перестанет перекрывать страницу 
        self.wait.until(ec.invisibility_of_element_located(OrderPageLocators.ORDER_OVERLAY))

        try:
            self.wait.until(ec.invisibility_of_element_located(OrderPageLocators.SUCCESS_MODAL))
        except Exception:
            pass


    @allure.step("Wait until success modal text contains order number")
    def wait_until_order_number_text_present(self):
        # ждём появления модалки
        self.wait.until(ec.visibility_of_element_located(OrderPageLocators.SUCCESS_MODAL))

        # ждём, что в текстовом блоке появится "Номер заказа"
        self.wait.until(ec.text_to_be_present_in_element(
            OrderPageLocators.SUCCESS_MODAL_TEXT_BLOCK,
            "Номер заказа"
        ))

    @allure.step("Click 'View status' button in success modal")
    def click_check_order_status_modal_button(self):
        self.safe_click(OrderPageLocators.CHECK_ORDER_STATUS_MODAL_BUTTON)

    @allure.step("Wait overlay to disappear")
    def wait_overlay_to_disappear(self):
        self.wait.until(ec.invisibility_of_element_located(OrderPageLocators.ORDER_OVERLAY))


    @allure.step("Wait until order number appears in success modal")
    def wait_for_order_number_in_modal_text(self):
        # ждём появления модалки
        self.wait.until(ec.visibility_of_element_located(OrderPageLocators.SUCCESS_MODAL))

        # ждём, что в текстовом блоке есть хоть одна цифра (это и есть номер)
        def _has_digits(driver):
            text = driver.find_element(*OrderPageLocators.SUCCESS_MODAL_TEXT_BLOCK).text
            return any(ch.isdigit() for ch in text)

        self.wait.until(_has_digits)