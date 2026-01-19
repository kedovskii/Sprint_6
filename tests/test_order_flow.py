import allure
from conftest import DZEN_URL
from pages.main_page import MainPage
from pages.order_page import OrderPage
from pages.rent_page import RentPage


DATA_TOP = {
    "name": "Александр",
    "surname": "Тестов",
    "address": "Москва, Тверская 1",
    "metro_query": "Тверская",
    "phone": "+79990000001",
    "date": "15.01.2026",
    "rent_period": "сутки",
    "comment": "Тестовый заказ 1",
}

DATA_BOTTOM = {
    "name": "Иван",
    "surname": "Петров",
    "address": "Москва, Арбат 10",
    "metro_query": "Арбатская",
    "phone": "+79990000002",
    "date": "16.01.2026",
    "rent_period": "двое суток",
    "comment": "Тестовый заказ 2",
}


def _open_and_start_order(driver, base_url, click_entry_fn):
    main = MainPage(driver)
    main.open_main(base_url)
    main.accept_cookies_if_present()
    click_entry_fn(main)
    return main


def _create_order_until_success_modal(driver, base_url, click_entry_fn, data):
    main = _open_and_start_order(driver, base_url, click_entry_fn)

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
        comment=data["comment"],
    )
    rent.select_color_black()
    rent.submit_and_confirm()

    return main, rent


@allure.feature("Order")
class TestOrderFlow:

    @allure.title("Появляется подтверждение оформления заказа (top entry)")
    def test_order_success_modal_text_top(self, driver, base_url):
        _, rent = _create_order_until_success_modal(
            driver=driver,
            base_url=base_url,
            click_entry_fn=lambda m: m.click_order_button_top(),
            data=DATA_TOP,
        )

        success_text = rent.success_should_be_visible()
        assert "Заказ оформлен" in success_text, f"Нет подтверждения заказа. Текст: {success_text}"

    @allure.title("Кнопка 'Посмотреть статус' закрывает overlay (top entry)")
    def test_check_order_status_closes_overlay_top(self, driver, base_url):
        _, rent = _create_order_until_success_modal(
            driver=driver,
            base_url=base_url,
            click_entry_fn=lambda m: m.click_order_button_top(),
            data=DATA_TOP,
        )

        rent.click_check_order_status_modal_button()
        rent.wait_overlay_to_disappear()
        assert True

    @allure.title("Логотип Самоката ведет на главную (top entry)")
    def test_scooter_logo_returns_to_main_top(self, driver, base_url):
        main, rent = _create_order_until_success_modal(
            driver=driver,
            base_url=base_url,
            click_entry_fn=lambda m: m.click_order_button_top(),
            data=DATA_TOP,
        )

        rent.click_check_order_status_modal_button()
        rent.wait_overlay_to_disappear()

        main.click_scooter_logo()
        main.assert_current_url_is(base_url)

    @allure.title("Логотип Яндекса открывает Dzen (top entry)")
    def test_yandex_logo_opens_dzen_top(self, driver, base_url):
        main, rent = _create_order_until_success_modal(
            driver=driver,
            base_url=base_url,
            click_entry_fn=lambda m: m.click_order_button_top(),
            data=DATA_TOP,
        )

        rent.click_check_order_status_modal_button()
        rent.wait_overlay_to_disappear()

        main.wait_main_page_loaded()
        main.click_yandex_logo_and_switch_to_new_tab()
        main.wait_url_contains("dzen.ru")
        main.assert_current_url_contains("dzen.ru")
