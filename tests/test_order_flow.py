import allure
from constants import DZEN_DOMAIN, BASE_URL
from pages.main_page import MainPage
from pages.rent_page import RentPage
from test_data import DATA_TOP, DATA_BOTTOM


@allure.feature("Order")
class TestOrderFlow:

    @allure.title("Появляется подтверждение оформления заказа (top entry)")
    def test_order_success_modal_text_top(self, driver):
        main = MainPage(driver)
        main.open_and_start_order(BASE_URL, entry_position="top")
        
        rent = RentPage(driver)
        rent.fill_complete_order(DATA_TOP)

        success_text = rent.success_should_be_visible()
        assert "Заказ оформлен" in success_text, f"Нет подтверждения заказа. Текст: {success_text}"

    @allure.title("Кнопка 'Посмотреть статус' закрывает overlay (top entry)")
    def test_check_order_status_closes_overlay_top(self, driver):
        main = MainPage(driver)
        main.open_and_start_order(BASE_URL, entry_position="top")
        
        rent = RentPage(driver)
        rent.fill_complete_order(DATA_TOP)

        rent.click_check_order_status_modal_button()
        assert rent.is_overlay_closed()

    @allure.title("Логотип Самоката ведет на главную (top entry)")
    def test_scooter_logo_returns_to_main_top(self, driver):
        main = MainPage(driver)
        main.open_and_start_order(BASE_URL, entry_position="top")
        
        rent = RentPage(driver)
        rent.fill_complete_order(DATA_TOP)
        
        rent.click_check_order_status_modal_button()

        main.click_scooter_logo()
        main.assert_current_url_is(BASE_URL)

    @allure.title("Логотип Яндекса открывает Dzen (top entry)")
    def test_yandex_logo_opens_dzen_top(self, driver):
        main = MainPage(driver)
        main.open_and_start_order(BASE_URL, entry_position="top")
        
        rent = RentPage(driver)
        rent.fill_complete_order(DATA_TOP)
        
        rent.click_check_order_status_modal_button()

        main.wait_main_page_loaded()
        main.click_yandex_logo_and_switch_to_new_tab()
        main.assert_current_url_contains(DZEN_DOMAIN)

    @allure.title("Появляется подтверждение оформления заказа (bottom entry)")
    def test_order_success_modal_text_bottom(self, driver):
        main = MainPage(driver)
        main.open_and_start_order(BASE_URL, entry_position="bottom")
        
        rent = RentPage(driver)
        rent.fill_complete_order(DATA_BOTTOM)

        success_text = rent.success_should_be_visible()
        assert "Заказ оформлен" in success_text, f"Нет подтверждения заказа. Текст: {success_text}"

    @allure.title("Кнопка 'Посмотреть статус' закрывает overlay (bottom entry)")
    def test_check_order_status_closes_overlay_bottom(self, driver):
        main = MainPage(driver)
        main.open_and_start_order(BASE_URL, entry_position="bottom")
        
        rent = RentPage(driver)
        rent.fill_complete_order(DATA_BOTTOM)

        rent.click_check_order_status_modal_button()
        assert rent.is_overlay_closed()

    @allure.title("Логотип Самоката ведет на главную (bottom entry)")
    def test_scooter_logo_returns_to_main_bottom(self, driver):
        main = MainPage(driver)
        main.open_and_start_order(BASE_URL, entry_position="bottom")
        
        rent = RentPage(driver)
        rent.fill_complete_order(DATA_BOTTOM)
        
        rent.click_check_order_status_modal_button()

        main.click_scooter_logo()
        main.assert_current_url_is(BASE_URL)

    @allure.title("Логотип Яндекса открывает Dzen (bottom entry)")
    def test_yandex_logo_opens_dzen_bottom(self, driver):
        main = MainPage(driver)
        main.open_and_start_order(BASE_URL, entry_position="bottom")
        
        rent = RentPage(driver)
        rent.fill_complete_order(DATA_BOTTOM)
        
        rent.click_check_order_status_modal_button()

        main.wait_main_page_loaded()
        main.click_yandex_logo_and_switch_to_new_tab()
        main.assert_current_url_contains(DZEN_DOMAIN)
