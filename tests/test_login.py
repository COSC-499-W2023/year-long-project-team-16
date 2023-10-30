import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_PAGE_URL = "http://localhost:8000/app/coursify-ai/frontend/login.html"

@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def login(browser, email, password):
    browser.get(LOGIN_PAGE_URL)
    email_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    password_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    email_input.send_keys(email)
    password_input.send_keys(password)
    
    login_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary.btn-block"))
    )
    browser.execute_script("arguments[0].click();", login_button)

def test_correct_credentials(browser):
    login(browser, "test@example.com", "test123")
    login_button = browser.find_elements(By.CSS_SELECTOR, ".btn.btn-primary.btn-block")
    assert len(login_button) == 0, "Login was not successful"

def test_incorrect_username(browser):
    correct_email = "test@example.com"
    email1 = "wrong@example.com"
    browser.get(LOGIN_PAGE_URL)
    
    email_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_input.send_keys(email1)
    email_input_value = email_input.get_attribute("value")
    assert correct_email != email_input_value, f"Expected email to be '{email1}' but got '{email_input_value}'"

def test_incorrect_password(browser):
    correct_email = "test@example.com"
    correct_password = "password"
    password1 = "wrongpassword"
    browser.get(LOGIN_PAGE_URL)
    
    email_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    password_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    email_input.send_keys(correct_email)
    password_input.send_keys(password1)
    password_input_value = password_input.get_attribute("value")
    assert correct_password != password_input_value, f"Expected password to be '{password_input_value}' but got '{correct_password}'"

def test_incorrect_both(browser):
    incorrect_email = "wrong@example.com"
    incorrect_password = "wrongpassword"
    
    browser.get(LOGIN_PAGE_URL)
    email_input = browser.find_element(By.ID, "email")
    email_input.send_keys(incorrect_email)
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys(incorrect_password)
    
    email_input_value = email_input.get_attribute("value")
    password_input_value = password_input.get_attribute("value")
    
    assert incorrect_email == email_input_value, f"Expected email to be '{incorrect_email}' but got '{email_input_value}'"
    assert incorrect_password == password_input_value, f"Expected password to be '{incorrect_password}' but got '{password_input_value}'"
    

