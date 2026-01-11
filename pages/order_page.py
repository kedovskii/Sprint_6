import allure
from pages.base_page import BasePage
from locators.order_page_locators import OrderPageLocators


class OrderPage(BasePage):
    @allure.step("Заполнить шаг 1 формы заказа: {name} {surname}")
    def fill_step_one(self, name, surname, address, metro_query, phone):
        self.type(OrderPageLocators.NAME, name)
        self.type(OrderPageLocators.SURNAME, surname)
        self.type(OrderPageLocators.ADDRESS, address)

        # Метро: ввод + клик по первому пункту
        self.type(OrderPageLocators.METRO, metro_query)
        self.click(OrderPageLocators.METRO_DROPDOWN_ITEM_FIRST)

        self.type(OrderPageLocators.PHONE, phone)

    @allure.step("Нажать 'Далее' на шаге 1")
    def click_next(self):
        self.click(OrderPageLocators.NEXT_BUTTON)
