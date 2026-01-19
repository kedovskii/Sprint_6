from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator):
        return self.driver.find_element(*locator)

    def click(self, locator):
        self.wait.until(ec.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str, clear: bool = True):
        el = self.wait.until(ec.visibility_of_element_located(locator))
        if clear:
            el.clear()
        el.send_keys(text)

    def text_of(self, locator) -> str:
        el = self.wait.until(ec.visibility_of_element_located(locator))
        return el.text

    def is_visible(self, locator) -> bool:
        self.wait.until(ec.visibility_of_element_located(locator))
        return True

    def scroll_into_view(self, locator):
        el = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        return el

    def _js_click(self, locator):
        el = self.find(locator)
        self.driver.execute_script("arguments[0].click();", el)

    def safe_click(self, locator):
        # 1) wait for presence
        self.wait.until(ec.presence_of_element_located(locator))
        # 2) scroll into view
        self.scroll_into_view(locator)

        try:
            # 3) normal click
            self.wait.until(ec.element_to_be_clickable(locator)).click()
        except ElementClickInterceptedException:
            # 4) ActionChains click
            el = self.find(locator)
            try:
                ActionChains(self.driver).move_to_element(el).click(el).perform()
            except ElementClickInterceptedException:
                # 5) last resort: JS click
                self._js_click(locator)

    def click_if_present(self, locator) -> bool:
        try:
            self.driver.find_element(*locator).click()
            return True
        except Exception:
            return False