# 1.check if sidebar header is present, and contains "My dashboard"
# 2.check if the logo is present
# 3.check if the menu items are present (home, my content, settings, my profile, lougout)
# 4.check if "generate content is present"
# 5.check if the content form is present

# Each test function in this file requires the correct log in credentials.


import time
import pytest #testing framework 
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

INDEX_PAGE_URL = "http://127.0.0.1:5000/"
DOWNLOAD_DIR = "year-long-project-team-16/pdfs/download"  # Set your download path here

@pytest.fixture(scope="function")
def browser():

    driver = webdriver.Chrome() #start a new instance of chrome,
    yield driver #yield keyword allows the test to use the browser.
    driver.quit() #close the browser after the test function completes.

def login(browser, email, password):
    
    browser.get(INDEX_PAGE_URL) #navigates the browser to the login page
    #textboxes
    email_input = browser.find_element(By.ID, "email")
    password_input = browser.find_element(By.ID, "password")
    #typing to the corresponding input fields
    email_input.send_keys(email)
    password_input.send_keys(password)
    # waiting 10 seconds for the login button to appear.
    # WebDriverWait is a is a class in Selenium that facilitates the implementation of explicit waits.

    #locating and clicking the submit button
    login_button = WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-primary.btn-block"))
        #EC stands for "Expected Conditions." It's a module in Selenium that provides 
        # a set of predefined conditionsto use with WebDriverWait. Presense_of_element_located
        # is one of those predefined conditions
    )
    # this or simply login_button.click();
    browser.execute_script("arguments[0].click();", login_button)


#def test_sidebar_logo(browser):
 #   login(browser, "remy123@gmail.com", "remy123") #REPLACE
  #  submit_button = browser.find_elements(By.CSS_SELECTOR, ".btn.btn-primary.btn-block")
   # #checks if the list of elements matching the login button selector is empty (length = 0)
    #if len(submit_button)==0:
     #   logo = WebDriverWait(browser,10).until(
      #      EC.presence_of_element_located((By.TAG_NAME, "name of image")) #REPLACE
       # )
        #assert logo.is_displayed(), "logo is missing"
    #else:
     #   assert False, "Login was not successful"

def open_index_page(browser):
    browser.get(INDEX_PAGE_URL)





def test_navigation_links(browser):
    browser.get(INDEX_PAGE_URL)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "navbar")))

    # Dictionary of navigation link IDs and their expected display status
    navigation_links = {
        "home": True,
        "content": True,
        "settings": True,
        
        # If an ID is later added, update this part accordingly
        "AI ASSISTANT": True,
        "logout": True,
    }

    for link_text, is_displayed in navigation_links.items():
        if link_text == "AI ASSISTANT":
            link = browser.find_element(By.LINK_TEXT, link_text)
        else:
            link = browser.find_element(By.ID, link_text)
        
        assert link.is_displayed() == is_displayed, f"{link_text} link is not displayed as expected"


def test_generate_content(browser):
    browser.get(INDEX_PAGE_URL)  # Replace with the actual URL of your form
    # Wait for the form to be present
    content_form = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "content-form"))
    )
    assert content_form.is_displayed(), "Content form is not displayed"

    # Test 'Length of Content' input field
    length_input = browser.find_element(By.ID, "length")
    assert length_input.get_attribute('type') == 'number'
    assert length_input.get_attribute('placeholder') == "Enter length (e.g., 1000 words)"
    assert length_input.get_attribute('required') is not None

    # Test 'Difficulty' input field
    difficulty_input = browser.find_element(By.ID, "difficulty")
    assert difficulty_input.get_attribute('type') == 'number'
    assert difficulty_input.get_attribute('min') == '0'
    assert difficulty_input.get_attribute('max') == '3'
    assert difficulty_input.get_attribute('required') is not None

    # Test 'Main Topics' input field
    topics_input = browser.find_element(By.ID, "topics")
    assert topics_input.get_attribute('type') == 'text'
    assert topics_input.get_attribute('placeholder') == "Enter main topics"
    assert topics_input.get_attribute('required') is not None

    # Test 'Upload PDF' input field
    pdf_upload = browser.find_element(By.ID, "pdf-upload")
    assert pdf_upload.get_attribute('type') == 'file'
    assert pdf_upload.get_attribute('accept') == ".pdf"

    # Test 'Generate' button
    generate_button = browser.find_element(By.ID, "generate-button")
    assert generate_button.is_displayed()
    assert generate_button.get_attribute('type') == 'submit'

def test_pdf_generation(browser):
    browser.get("http://127.0.0.1:5000/")  # Replace with the actual URL of your form
    # Assuming the form is immediately accessible

    # Fill the form here as required
    # Example:
    browser.find_element(By.ID, "length").send_keys("1000")
    browser.find_element(By.ID, "difficulty").send_keys("2")
    browser.find_element(By.ID, "topics").send_keys("Example Topics")

    # Submit the form
    browser.find_element(By.ID, "generate-button").click()

    # Wait for the PDF to download
    time.sleep(7)  # Wait time depends on your application's response time

    browser.find_element(By.ID, "generate-button").click()
    time.sleep(7)

    assert browser.current_url != INDEX_PAGE_URL, "Browser did not redirect from the index URL"

#def test_email_sent(browser):






