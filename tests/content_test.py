# This file does not require loging in to test each function

import pytest #testing framework 
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_PAGE_URL = "http://localhost:8000/app/content.html"

@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome() #start a new instance of chrome,
    yield driver #yield keyword allows the test to use the browser.
    driver.quit() #close the browser after the test function completes.

def test_sidebar_header(browser: WebDriver):
    #login(browser, "remy123@gmail.com", "remy123")  #REPLACE
    #submit_button = browser.find_elements(By.CSS_SELECTOR, ".btn.btn-primary.btn-block")
    #checks if the list of elements matching the login button selector is empty (length = 0)
    browser.get(LOGIN_PAGE_URL)
    try:
        sidebar_header = WebDriverWait(browser,10).until(
            EC.presence_of_element_located((By.ID, "title")) #REPLACE
        )
        assert sidebar_header.is_displayed(), "Sidebar header is missing"
        #assert "My Dashboard" in sidebar_header.text, "The text'My dashboard' is not present"
    except TimeoutException:
        pytest.fail("Header not found")

def test_sidebar_logo(browser: WebDriver):
    browser.get(LOGIN_PAGE_URL)
    try:
        logo = WebDriverWait(browser,10).until(
        EC.presence_of_element_located((By.ID, "logo")) #REPLACE
        )
        assert logo.is_displayed(), "logo is missing"
    except TimeoutException:
        pytest.fail("logo not found")
        
def test_menu_items(browser: WebDriver):
    browser.get(LOGIN_PAGE_URL)

    try:
        sidebar = WebDriverWait(browser,30).until(
        EC.presence_of_element_located((By.ID, "sidebar")) #expected conditions
        )

        toolbar_items = {
            "HOME":"home",
            "MY CONTENT":"content",
            "SETTINGS":"settings",
            "AI ASSISTANT":"ai",
            "LOGOUT":"logout",
        }

        for item_text, item_id in toolbar_items.items():
            item = sidebar.find_element(By.LINK_TEXT, item_text)
            assert item.is_displayed(), f"{item_text} link is missing"
    except TimeoutException:
        pytest.fail("menu items not found")

def test_my_content(browser: WebDriver):
    browser.get(LOGIN_PAGE_URL)
    try:
        notes = WebDriverWait(browser,10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "notes-container")) #expected conditions
        )
        assert notes.is_displayed(), "Form is missing"
    except TimeoutException:
        pytest.fail("from not found")