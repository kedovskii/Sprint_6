from selenium.webdriver.common.by import By


class MainPageLocators:
    # Куки (если баннер появляется)
    COOKIE_ACCEPT_BUTTON = (By.ID, "rcc-confirm-button")

    # Кнопки "Заказать"
    ORDER_BUTTON_TOP = (By.XPATH, "//button[contains(@class,'Button_Button') and text()='Заказать']")
    ORDER_BUTTON_BOTTOM = (By.XPATH, "//div[contains(@class,'Home_FinishButton')]/button[text()='Заказать']")

    # FAQ: у учебного сервиса часто id вида accordion__heading-0..7 и panel-0..7
    @staticmethod
    def faq_question(index: int):
        return (By.ID, f"accordion__heading-{index}")

    @staticmethod
    def faq_answer(index: int):
        return (By.ID, f"accordion__panel-{index}")

    # Логотипы
    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CSS_SELECTOR, "a[class*='Header_LogoYandex']")