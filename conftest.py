import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from constants import BASE_URL, DZEN_URL, DZEN_DOMAIN, IMPLICIT_WAIT


@pytest.fixture(scope="function")
def driver():
    options = Options()
    # options.add_argument("-headless")  # если нужно без UI
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.implicitly_wait(IMPLICIT_WAIT)
    yield driver
    driver.quit()


# Скриншот в Allure при падении теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot_on_fail",
                    attachment_type=allure.attachment_type.PNG,
                )
                allure.attach(
                    driver.page_source,
                    name="page_source_on_fail",
                    attachment_type=allure.attachment_type.HTML,
                )
            except Exception:
                pass
