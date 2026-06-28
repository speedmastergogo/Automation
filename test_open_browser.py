from selenium import webdriver
import pytest
def test_open_browser(setup):
    setup.get("https://www.google.com")
    assert "Google" in setup.title ,"browser is not opened"
    print("browser opened successfully")
    