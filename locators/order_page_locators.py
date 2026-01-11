from selenium.webdriver.common.by import By


class OrderPageLocators:
    # Шаг 1: "Для кого самокат"
    NAME = (By.XPATH, "//input[@placeholder='* Имя']")
    SURNAME = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO = (By.XPATH, "//input[@placeholder='* Станция метро']")
    PHONE = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    METRO_DROPDOWN_ITEM_FIRST = (By.XPATH, "//div[contains(@class,'select-search__select')]//li[1]")

    # Шаг 2: "Про аренду"
    DATE = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENT_PERIOD_DROPDOWN = (By.XPATH, "//div[contains(@class,'Dropdown-control')]")
    # вариант периода будем искать по тексту динамически

    COLOR_BLACK = (By.ID, "black")
    COLOR_GREY = (By.ID, "grey")
    COMMENT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")

    ORDER_BUTTON = (By.XPATH, "//div[contains(@class,'Order_Buttons')]//button[text()='Заказать']")
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[text()='Да']")

    # Успех
    SUCCESS_MODAL = (By.CSS_SELECTOR, "div[class*='Order_Modal']")
    SUCCESS_TEXT = (By.XPATH, "//div[contains(@class,'Order_Modal')]//div[contains(@class,'Order_ModalHeader')]")
    SUCCESS_MODAL_TEXT_BLOCK = (By.CSS_SELECTOR, "div[class*='Order_Text']")

    ORDER_OVERLAY = (By.CSS_SELECTOR, "div[class*='Order_Overlay']")
    # CHECK_ORDER_STATUS_MODAL_BUTTON = (By.CSS_SELECTOR,"div[class*='Order_NextButton'] button")
    CHECK_ORDER_STATUS_MODAL_BUTTON = (By.XPATH,"//div[contains(@class,'Order_Modal')]//button[normalize-space()='Посмотреть статус']")
    
