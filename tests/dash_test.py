# 1.check if sidebar header is present, and contains "My dashboard"
# 2.check if the logo is present
# 3.check if the menu items are present (home, my content, settings, my profile, lougout)
# 4.check if "generate content is present"
# 5.check if the content form is present

import pytest #testing framework 
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_PAGE_URL = "http://localhost:8000/login.html"

@pytest.fixture(scope="function")
def browser():

    driver = webdriver.Chrome() #start a new instance of chrome,
    yield driver #yield keyword allows the test to use the browser.
    driver.quit() #close the browser after the test function completes.

def login(browser, email, password):
    
    browser.get(LOGIN_PAGE_URL) #navigates the browser to the login page
    #textboxes
    email_input = browser.find_element(By.ID, "email")
    password_input = browser.find_element(By.ID, "password")
    #typing to the corresponding input fields
    email_input.send_keys(email)
    password_input.send_keys(password)
    # waiting 10 seconds for the login button to appear.
    # WebDriverWait is a is a class in Selenium that facilitates the implementation of explicit waits.

    #locating and clicking the submit button
    login_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-primary.btn-block"))
        #EC stands for "Expected Conditions." It's a module in Selenium that provides 
        # a set of predefined conditionsto use with WebDriverWait. Presense_of_element_located
        # is one of those predefined conditions
    )
    # this or simply login_button.click();
    browser.execute_script("arguments[0].click();", login_button)

def test_sidebar_header(browser):
    login(browser, "remy123@gmail.com", "remy123")
    submit_button = browser.find_elements(By.CSS_SELECTOR, ".btn.btn-primary.btn-block")
    #checks if the list of elements matching the login button selector is empty (length = 0)
    if len(submit_button)==0:
        sidebar_header = WebDriverWait(browser,10).until(
            EC.presence_of_element_located((By.ID, "name of sidebar-header")) #expected conditions
        )
        assert sidebar_header.is_displayed(), "Sidebar header is missing"
        assert "My Dashboard" in sidebar_header.text, "The text'My dashboard' is not present"
    else:
        assert False, "Login was not successful"

def test_sidebar_logo(browser):
    login(browser, "remy123@gmail.com", "remy123")
    submit_button = browser.find_elements(By.CSS_SELECTOR, ".btn.btn-primary.btn-block")
    #checks if the list of elements matching the login button selector is empty (length = 0)
    if len(submit_button)==0:
        logo = WebDriverWait(browser,10).until(
            EC.presence_of_element_located((By.TAG_NAME, "name of image")) #expected conditions
        )
        assert logo.is_displayed(), "logo is missing"
    else:
        assert False, "Login was not successful"

def test_menu_items(browser):
    login(browser, "remy123@gmail.com", "remy123")
    submit_button = browser.find_elements(By.CSS_SELECTOR, ".btn.btn-primary.btn-block")

    if len(submit_button)==0:
        sidebar = WebDriverWait(browser,10).until(
            EC.presence_of_element_located((By.ID, "sidebar")) #expected conditions
        )
        #home = sidebar.find_element(By.LINK_TEXT, "Home")
        #assert home.is_displayed(), "home link is missing"

        # To iterate through the items in the toolbar and their corresponding IDs
        toolbar_items = {
            

        }
    else:
        assert False, "Login was not successful"



