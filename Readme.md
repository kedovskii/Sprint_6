# UI tests (Pytest + Selenium + Allure)

## Install dependencies
```bash
pip3 install -r requirements.txt

Run all tests
pytest -v

Run tests with Allure results
pytest -v --alluredir=allure-results --clean-alluredir

View Allure report
allure serve allure-results