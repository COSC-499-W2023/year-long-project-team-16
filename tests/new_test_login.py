import pytest #testing framework 
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_PAGE_URL = "http://localhost:8000/login.html" #constant that holds the URL of the login page

# The fixture 'broswe' is set to have a 'function' scope, 
# meaning every function requesting the 'browser'
# a new instance of the Chrome browser will be created. 
@pytest.fixture(scope="function")
def browser():

    driver = webdriver.Chrome() #start a new instance of chrome,
    yield driver #yield keyword allows the test to use the browser.
    driver.quit() #close the browser after the test function completes.

#Reusable function to perform the login action
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

# CORRECT CREDENTIALS TESTING   
#-----------------------------
# what happens when the correct credentials are provided. 
# if logged in successfully, the test is successfull if there is no login button.
def test_correct_credentials(browser):
    login(browser, "test@example.com", "test123")
    login_button = browser.find_elements(By.CSS_SELECTOR, ".btn.btn-primary.btn-block")
    #checks if the list of elements matching the login button selector is empty (length = 0)
    assert len(login_button) == 0, "Login was not successful"

""" INCORRECT USERNAME TESTING - OLD
def test_incorrect_username(browser):
    correct_email = "test@example.com"  #REPLACE
    #email1 = "wrong@example.com"
    incorrect_email = "wrong@example.com" 
    
    # inputs = ["wrong@example.com","wrong123@example.com","test@example.com"
    # ,"wrong@example.com"]
    iswrong = True
    browser.get(LOGIN_PAGE_URL) 
    email_input = browser.find_element(By.ID, "email")
    email_input.send_keys(incorrect_email)

    #retrieving the incorrectly inputed email
    email_input_value = email_input.get_attribute("value")

    if(correct_email == incorrect_email):
        iswrong= False
    else:
        iswrong = True
    
    assert iswrong, f"Expected email to be '{incorrect_email}' but got '{email_input_value}'"

"""

# INCORRECT USERNAME TESTING - NEW
def test_incorrect_username(browser):
    incorrect_email = "wrong@example.com"
    testpassword = "Remy1234"

    # navigate to login page and input the wrong email 
    browser.get(LOGIN_PAGE_URL)

    #input wrong email
    email_input = browser.find_element(By.ID, "email")
    email_input.send_keys(incorrect_email)

    #input password
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys(testpassword)
    
    #Click login button
    login_button = browser.find_element(By.CSS_SELECTOR, ".btn.btn-primary.btn-block")
    login_button.click()

    #waiting 10 seconds
    error_message_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message"))
    )
    
    # if the error message does not contain "Invalid email", the test has failed
    assert "Invalid email" in error_message_element.text, "Expected an 'Invalid email' message but didn't get one"

# INCORRECT PASSWORD TESTING - OLD
"""def test_incorrect_password(browser):
    correct_email = "test@example.com"
    correct_password = "password"
    password1 = "wrongpassword"
    browser.get(LOGIN_PAGE_URL)
    email_input = browser.find_element(By.ID, "email")
    email_input.send_keys(correct_email)
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys(password1)
    password_input_value = password_input.get_attribute("value")
    assert correct_password != password_input_value, f"Expected password to be '{password_input_value}' but got '{correct_password}'"
"""

# INCORRECT PASSWORD TESTING - NEW
def test_incorrect_password(browser):
    correct_email = "test@example.com"
    #correct_password = "password"
    wrong_password = "wrongpassword"
    browser.get(LOGIN_PAGE_URL)
    #EMAIL
    email_input = browser.find_element(By.ID, "email")
    email_input.send_keys(correct_email)
    #PW
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys(wrong_password)
    #Click login button
    login_button = browser.find_element(By.CSS_SELECTOR, ".btn.btn-primary.btn-block")
    login_button.click()

    #waiting 10 seconds
    error_message_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message"))
    )
    
    # if the error message does not contain "Incorrect password", the test has failed
    assert "Incorrect password" in error_message_element.text, "Expected an 'Incorrect password' message but didn't get one"

    # The assertion checks if the error message contains the substring "Incorrect password". This has to be the
    # exact error message that the web application shows for incorrect username / password

     





