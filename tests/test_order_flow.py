import allure
from constants import DZEN_DOMAIN
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
    """Helper: открыть страницу и нажать "Заказать" """
    main = MainPage(driver)
    main.open_main(base_url)
    main.accept_cookies_if_present()
    click_entry_fn(main)
    return main


def _fill_order_form(driver, data):
    """Helper: заполнить форму заказа полностью и нажать "Заказать" """
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
    
    return rent


@allure.feature("Order")
class TestOrderFlow:

    # test 1: Проверяем, что успешно создается заказ (видна модалка с текстом)
    @allure.title("Появляется подтверждение оформления заказа (top entry)")
    def test_order_success_modal_text_top(self, driver, base_url):
        _open_and_start_order(driver, base_url, lambda m: m.click_order_button_top())
        rent = _fill_order_form(driver, DATA_TOP)

        success_text = rent.success_should_be_visible()
        assert "Заказ оформлен" in success_text, f"Нет подтверждения заказа. Текст: {success_text}"

    # test 2: Проверяем, что кнопка "Посмотреть статус" закрывает overlay
    @allure.title("Кнопка 'Посмотреть статус' закрывает overlay (top entry)")
    def test_check_order_status_closes_overlay_top(self, driver, base_url):
        _open_and_start_order(driver, base_url, lambda m: m.click_order_button_top())
        rent = _fill_order_form(driver, DATA_TOP)

        rent.click_check_order_status_modal_button()
        rent.wait_overlay_to_disappear()

    # test 3: Проверяем, что логотип Самоката ведет на главную
    @allure.title("Логотип Самоката ведет на главную (top entry)")
    def test_scooter_logo_returns_to_main_top(self, driver, base_url):
        main = _open_and_start_order(driver, base_url, lambda m: m.click_order_button_top())
        rent = _fill_order_form(driver, DATA_TOP)
        
        rent.click_check_order_status_modal_button()
        rent.wait_overlay_to_disappear()

        main.click_scooter_logo()
        main.assert_current_url_is(base_url)

    # test 4: Проверяем, что логотип Яндекса открывает Dzen
    @allure.title("Логотип Яндекса открывает Dzen (top entry)")
    def test_yandex_logo_opens_dzen_top(self, driver, base_url):
        main = _open_and_start_order(driver, base_url, lambda m: m.click_order_button_top())
        rent = _fill_order_form(driver, DATA_TOP)
        
        rent.click_check_order_status_modal_button()
        rent.wait_overlay_to_disappear()

        main.wait_main_page_loaded()
        main.click_yandex_logo_and_switch_to_new_tab()
        main.wait_url_contains(DZEN_DOMAIN)
        # Если URL не содержит "dzen.ru", то wait_url_contains упадет

    # test 5: Проверяем, что успешно создается заказ (видна модалка с текстом)
    @allure.title("Появляется подтверждение оформления заказа (bottom entry)")
    def test_order_success_modal_text_bottom(self, driver, base_url):
        _open_and_start_order(driver, base_url, lambda m: m.click_order_button_bottom())
        rent = _fill_order_form(driver, DATA_BOTTOM)

        success_text = rent.success_should_be_visible()
        assert "Заказ оформлен" in success_text, f"Нет подтверждения заказа. Текст: {success_text}"

    @allure.title("Кнопка 'Посмотреть статус' закрывает overlay (bottom entry)")
    def test_check_order_status_closes_overlay_bottom(self, driver, base_url):
        _open_and_start_order(driver, base_url, lambda m: m.click_order_button_bottom())
        rent = _fill_order_form(driver, DATA_BOTTOM)

        rent.click_check_order_status_modal_button()
        rent.wait_overlay_to_disappear()

    @allure.title("Логотип Самоката ведет на главную (bottom entry)")
    def test_scooter_logo_returns_to_main_bottom(self, driver, base_url):
        main = _open_and_start_order(driver, base_url, lambda m: m.click_order_button_bottom())
        rent = _fill_order_form(driver, DATA_BOTTOM)
        
        rent.click_check_order_status_modal_button()
        rent.wait_overlay_to_disappear()

        main.click_scooter_logo()
        main.assert_current_url_is(base_url)

    @allure.title("Логотип Яндекса открывает Dzen (bottom entry)")
    def test_yandex_logo_opens_dzen_bottom(self, driver, base_url):
        main = _open_and_start_order(driver, base_url, lambda m: m.click_order_button_bottom())
        rent = _fill_order_form(driver, DATA_BOTTOM)
        
        rent.click_check_order_status_modal_button()
        rent.wait_overlay_to_disappear()

        main.wait_main_page_loaded()
        main.click_yandex_logo_and_switch_to_new_tab()
        main.wait_url_contains(DZEN_DOMAIN)
