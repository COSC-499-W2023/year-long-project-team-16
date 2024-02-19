
# CASE 6 : CHANGE PASSWORD #========================================================================
#===================================================================================================
def test_change_password(browser):
    my_email = "ubcubc@gmail.com"                                                                                                                       # CHANGE
    my_password = "yarvp04117"

    login(browser, my_email, my_password)

    head_present = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "head"))
    )
    #can also use EC.text_to_be_present_in_element_located    
    
    assert head_present, "Login successful, 'head' element not found"  

    settings_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "settings"))
    )
    settings_link.click()

    uElement = WebDriverWait(browser,10).until(
        EC.presence_of_element_located((By.ID, "account-settings-form"))
    )

    assert uElement, "Navigated to the Settings page successfully, did not navigate to the settings page "
    
    password_link = WebDriverWait(browser,10).until(
        EC.element_to_be_clickable((By.ID, "password-settings-link"))
    )
    password_link.click()

    password_form_displayed = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "password-settings-form"))  # Adjust the ID based on your actual HTML
    )
    assert password_form_displayed, "Password form was not displayed after clicking the Password section"
    #
    current_password_field = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "current-password"))
    )
    current_password_field.clear()  # Clear any pre-filled text
    current_password_field.send_keys("yarvp04117")  # Replace with the actual current password
    #
    new_password_field = browser.find_element(By.ID, "new-password")
    new_password_field.clear()  # It's good practice to clear the field before entering text
    new_password_field.send_keys("1234")  # Replace with the desired new password
    #
    confirm_new_password_field = browser.find_element(By.ID, "confirm-new-password")
    confirm_new_password_field.clear()  # Clear any pre-filled text
    confirm_new_password_field.send_keys("1234")  # Repeat the new password
                                                                                                        #CHANGE

    save_changes_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    save_changes_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    expected_message = "Your password has been updated successfully." 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"


# CASE 7 : (SHOULD FAIL) CURRENT PASSWORD DOES NOT MATCH #==========================================
#===================================================================================================
def test_shouldFAIL_CURRENT_password_nomatch(browser):
    my_email = "ubcubc@gmail.com"                                                                                                                       # CHANGE
    my_password = "1234"

    login(browser, my_email, my_password)

    head_present = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "head"))
    )
    #can also use EC.text_to_be_present_in_element_located    
    
    assert head_present, "Login successful, 'head' element not found"  

    settings_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "settings"))
    )
    settings_link.click()

    uElement = WebDriverWait(browser,10).until(
        EC.presence_of_element_located((By.ID, "account-settings-form"))
    )

    assert uElement, "Navigated to the Settings page successfully, did not navigate to the settings page "

    password_link = WebDriverWait(browser,10).until(
        EC.element_to_be_clickable((By.ID, "password-settings-link"))
    )
    password_link.click()

    currentPW_field = browser.find_element(By.ID, "current-password")
    newPW_field = browser.find_element(By.ID, "new-password")
    confirmNewPW_field = browser.find_element(By.ID, "confirm-new-password")
    

    currentPW_field.send_keys("12345")
    newPW_field.send_keys("1234")      
    confirmNewPW_field.send_keys("1234")                                                                                                        #CHANGE

    save_changes_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    save_changes_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    expected_message = "Your password has been updated successfully." 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"

# CASE 8 : (SHOULD FAIL) NEW PASSWORD DO NOTH MATCH #===============================================
#===================================================================================================
def test_shouldFAIL_new_password_nomatch(browser):
    my_email = "ubcubc@gmail.com"                                                                                                                       # CHANGE
    my_password = "1234"

    login(browser, my_email, my_password)

    head_present = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "head"))
    )
    #can also use EC.text_to_be_present_in_element_located    
    
    assert head_present, "Login successful, 'head' element not found"  

    settings_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "settings"))
    )
    settings_link.click()

    uElement = WebDriverWait(browser,10).until(
        EC.presence_of_element_located((By.ID, "account-settings-form"))
    )

    assert uElement, "Navigated to the Settings page successfully, did not navigate to the settings page "

    password_link = WebDriverWait(browser,10).until(
        EC.element_to_be_clickable((By.ID, "password-settings-link"))
    )
    password_link.click()

    currentPW_field = browser.find_element(By.ID, "current-password")
    newPW_field = browser.find_element(By.ID, "new-password")
    confirmNewPW_field = browser.find_element(By.ID, "confirm-new-password")
    

    currentPW_field.send_keys("1234")
    newPW_field.send_keys("123")      
    confirmNewPW_field.send_keys("1234")                                                                                                        #CHANGE

    save_changes_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    save_changes_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    expected_message = "Your password has been updated successfully." 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"

