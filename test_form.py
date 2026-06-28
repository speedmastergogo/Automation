from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import pytest
url = "https://demoqa.com/automation-practice-form"
def test_case_01(setup):
    driver = setup
    wait = WebDriverWait(driver,10)
    driver.get(url)
    submit_btn = wait.until(EC.visibility_of_element_located((By.ID,"submit")))
    driver.execute_script("arguments[0].scrollIntoView();",submit_btn)
    time.sleep(1)
    submit_btn.click()
    #enter the details in the form
def test_case_02(setup):
    driver = setup
    driver.get(url)
    wait = WebDriverWait(driver,10)
    enter_first_name = wait.until(EC.presence_of_element_located((By.ID,"firstName")))
    enter_first_name.send_keys("John")
    enter_last_name = wait.until(EC.presence_of_element_located((By.ID,"lastName")))
    enter_last_name.send_keys("Doe")
    enter_email = wait.until(EC.presence_of_element_located((By.ID,"userEmail")))
    enter_email.send_keys("tomotid662@adsprite.com")
    select_gender = wait.until(EC.presence_of_element_located((By.ID,"gender-radio-1")))
    select_gender.click()
    enter_mobile = wait.until(EC.presence_of_element_located((By.ID,"userNumber")))
    enter_mobile.send_keys("1023456789")
    select_date_of_birth = wait.until(EC.presence_of_element_located((By.ID,"dateOfBirthInput")))
    select_date_of_birth.click()
    select_month = Select(wait.until(EC.presence_of_element_located((By.XPATH,"//select[@class='react-datepicker__month-select']"))))
    select_month.select_by_visible_text("May")
    select_year = Select(wait.until(EC.presence_of_element_located((By.XPATH,"//select[@class='react-datepicker__year-select']"))))
    select_year.select_by_value("1990")
    select_date = wait.until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'react-datepicker__day') and text()='3'] [1]")))
    select_date.click()
    enter_subjects = wait.until(EC.presence_of_element_located((By.ID,"subjectsInput")))
    enter_subjects.send_keys("Maths")
    enter_subjects.send_keys(Keys.TAB)
    select_hobbies = wait.until(EC.presence_of_element_located((By.XPATH,"//label[text()='Sports']")))
    driver.execute_script("arguments[0].scrollIntoView();",select_hobbies)
    time.sleep(1)
    select_hobbies.click()
    upload_picture = wait.until(EC.presence_of_element_located((By.ID,"uploadPicture")))
    upload_picture.send_keys("/home/u-64/Desktop/PyTest/image/ChatGPT Image Apr 17, 2026, 01_43_27 PM.png")
    enter_current_address = wait.until(EC.presence_of_element_located((By.ID,"currentAddress")))
    enter_current_address.send_keys("123 Main Street, Cityville, State, 12345")
    select_state = wait.until(EC.presence_of_element_located((By.ID,"react-select-3-input")))
    select_state.send_keys("NCR")
    select_state.send_keys(Keys.ENTER)
    select_city = wait.until(EC.presence_of_element_located((By.ID,"react-select-4-input")))
    select_city.send_keys("Delhi")
    select_city.send_keys(Keys.ENTER)
    click_submit = wait.until(EC.presence_of_element_located((By.XPATH,"//button[@id='submit']")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});",click_submit)
    time.sleep(1)
    click_submit.click()
    time.sleep(1)
    driver.save_screenshot("/home/u-64/Desktop/PyTest/image/form_submission.png")
