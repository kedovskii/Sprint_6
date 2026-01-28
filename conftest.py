import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

BASE_URL = "https://qa-scooter.praktikum-services.ru/"
DZEN_URL = "https://dzen.ru/"
DZEN_DOMAIN = "dzen.ru" 


@pytest.fixture(scope="function")
def driver():
    options = Options()
    # options.add_argument("-headless")  # если нужно без UI
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.implicitly_wait(3)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def base_url():
    return BASE_URL


@pytest.fixture(scope="function")
def dzen_url():
    return DZEN_URL


@pytest.fixture(scope="function")
def dzen_domain():
    return DZEN_DOMAIN


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
