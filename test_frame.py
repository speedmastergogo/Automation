from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
def test_frames1(setup):
    driver = setup
    driver.get("https://demoqa.com/frames")
    wait = WebDriverWait(driver,10)
    frame1 = wait.until(EC.presence_of_element_located((By.ID,"frame1")))
    driver.switch_to.frame(frame1)
    heading1 = wait.until(EC.presence_of_element_located((By.ID,"sampleHeading")))
    assert heading1.text == "This is a sample page", "switch to frame1 failed"
    print("switch to frame1 successful")
    driver.switch_to.default_content()
def test_frames2(setup):
    driver = setup
    driver.get("https://demoqa.com/frames")
    wait = WebDriverWait(driver,10)
    frame2 = wait.until(EC.presence_of_element_located((By.ID,"frame2")))
    driver.switch_to.frame(frame2)
    heading2 = wait.until(EC.presence_of_element_located((By.ID,"sampleHeading")))
    assert heading2.text == "This is a sample page" , "switch to frame2 failed"
    print("switch to frame2 successfully")
    driver.switch_to.default_content()
    