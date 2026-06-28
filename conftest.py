import pytest
from selenium import webdriver
@pytest.fixture
def input_value():
    input = 5
    return input
@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get_cookie(any)
    yield driver
    driver.quit()
