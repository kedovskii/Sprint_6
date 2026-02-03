import allure
import pytest

from constants import BASE_URL
from pages.main_page import MainPage


FAQ_CASES = [
    (0, "Сутки — 400 рублей. Оплата курьеру — наличными или картой."),
    (1, "Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим."),
    (2, "Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30."),
    (3, "Только начиная с завтрашнего дня. Но скоро станем расторопнее."),
    (4, "Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010."),
    (5, "Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится."),
    (6, "Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои."),
    (7, "Да, обязательно. Всем самокатов! И Москве, и Московской области."),
]

@allure.feature("FAQ")
class TestFAQ:
    @pytest.mark.parametrize("index, expected", FAQ_CASES)
    @allure.title("FAQ: when clicking on question #{index}, the correct answer is displayed")
    def test_faq_answer_opens(self, driver, index, expected):
        main_page = MainPage(driver)
        main_page.open_main(BASE_URL)
        main_page.accept_cookies_if_present()

        main_page.open_faq_question(index)
        answer = main_page.get_faq_answer_text(index)

        assert expected == answer, f"FAQ question #{index}: expected answer '{expected}', but got '{answer}'"
