import allure
import pytest
from conftest import DZEN_URL, driver
from pages.main_page import MainPage
from pages.order_page import OrderPage
from pages.rent_page import RentPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


ORDER_CASES = [
    # entry, data
    (
        "top",
        {
            "name": "Александр",
            "surname": "Тестов",
            "address": "Москва, Тверская 1",
            "metro_query": "Тверская",
            "phone": "+79990000001",
            "date": "15.01.2026",
            "rent_period": "сутки",
            "color": "black",
            "comment": "Тестовый заказ 1",
        },
    ),
    (
        "bottom",
        {
            "name": "Иван",
            "surname": "Петров",
            "address": "Москва, Арбат 10",
            "metro_query": "Арбатская",
            "phone": "+79990000002",
            "date": "16.01.2026",
            "rent_period": "двое суток",
            "color": "grey",
            "comment": "Тестовый заказ 2",
        },
    ),
]


@allure.feature("Order")
class TestOrderFlow:
    @pytest.mark.parametrize("entry, data", ORDER_CASES)
    @allure.title("Позитивный флоу заказа самоката (точка входа: {entry})")
    def test_order_success_flow(self, driver, base_url, entry, data):
        main = MainPage(driver)
        main.open_main(base_url)
        main.accept_cookies_if_present()

        # Точка входа
        main.click_order_button(entry)

        order = OrderPage(driver)
        order.fill_step_one(
            name=data["name"],
            surname=data["surname"],
            address=data["address"],
            metro_query=data["metro_query"],
            phone=data["phone"],
        )
        order.click_next()

        rent = RentPage(driver)
        rent.fill_step_two(
            date_str=data["date"],
            rent_period_text=data["rent_period"],
            color=data["color"],
            comment=data["comment"],
        )
        rent.submit_and_confirm()

        success_text = rent.success_should_be_visible()
        assert "Заказ оформлен" in success_text, f"Нет подтверждения заказа. Текст: {success_text}"

        rent.wait_for_order_number_in_modal_text()
        rent.click_check_order_status_modal_button()
        rent.wait_overlay_to_disappear()

        # Логотип Самоката ведёт на главную Самоката
        main.click_scooter_logo()
        assert driver.current_url == base_url, f"Ожидали главную '{base_url}', получили '{driver.current_url}'"

        main.wait_main_page_loaded()

        old_handles = driver.window_handles
        main.click_yandex_logo()

        WebDriverWait(driver, 10).until(ec.number_of_windows_to_be(len(old_handles) + 1))
        new_handle = [h for h in driver.window_handles if h not in old_handles][0]
        driver.switch_to.window(new_handle)

        WebDriverWait(driver, 10).until(ec.url_contains("dzen.ru"))
        assert "dzen.ru" in driver.current_url, f"Expected '{DZEN_URL}', got '{driver.current_url}'"
