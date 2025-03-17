from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException

import time

import json

import os

import pyperclip  # For clipboard operations

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

import threading

import random



def create_and_approve_account(num_approvals=1, headless=False):

    # Set up Chrome options

    chrome_options = webdriver.ChromeOptions()

    

    # Add headless mode if requested

    if headless:

        chrome_options.add_argument("--headless")

        chrome_options.add_argument("--disable-gpu")  # Required for some systems

        chrome_options.add_argument("--window-size=1920,1080")  # Set window size for headless mode

    

    # Add permissions for clipboard access

    chrome_options.add_experimental_option("prefs", {

        "profile.default_content_settings.popups": 0,

        "profile.default_content_setting_values.notifications": 1,

        "profile.default_content_setting_values.clipboard": 1

    })

    

    # Initialize the driver

    driver = webdriver.Chrome(options=chrome_options)

    if not headless:

        driver.maximize_window()

    

    # Initialize or load the JSON file for storing recovery phrases

    json_file = "solflare.json"

    if os.path.exists(json_file):

        with open(json_file, "r") as f:

            recovery_phrases = json.load(f)

    else:

        recovery_phrases = []

    

    try:

        # Process for each approval

        approvals_completed = 0

        

        # First need to create a wallet

        print(f"Starting initial wallet creation process")

        

        # Navigate to the Solflare onboarding page

        driver.get("https://solflare.com/onboard/create")

        print("Navigated to Solflare onboarding page")

        

        # Wait for the recovery phrase to be visible

        recovery_phrase_element = WebDriverWait(driver, 20).until(

            EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div/div[1]/div[2]"))

        )

        time.sleep(2)  # Additional wait to ensure page is fully loaded

        

        # Get the recovery phrase text if possible

        try:

            recovery_phrase = recovery_phrase_element.text

            print("Recovery phrase captured")

        except:

            recovery_phrase = "Unable to capture directly"

            print("Could not capture recovery phrase directly")

        

        # Click on Copy button

        copy_button = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/div[1]/div[2]/div[3]/button[2]/span"))

        )

        copy_button.click()

        print("Clicked Copy button")

        

        # Wait for potential permission popup and handle it

        try:

            # Look for the permission dialog (this XPath might need adjustment)

            permission_allow = WebDriverWait(driver, 5).until(

                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Allow') or contains(text(), 'Allow site to access clipboard')]"))

            )

            permission_allow.click()

            print("Clicked Allow on clipboard permission popup")

        except TimeoutException:

            print("No clipboard permission popup detected or it was already allowed")

        

        # Give time for the clipboard operation to complete

        time.sleep(3)

        

        # Try to get the recovery phrase from clipboard

        try:

            clipboard_phrase = pyperclip.paste()

            if clipboard_phrase and len(clipboard_phrase) > 10:  # Basic validation

                recovery_phrase = clipboard_phrase

                print("Recovery phrase obtained from clipboard")

        except:

            print("Could not access clipboard")

        

        # Click on "I saved my recovery phrase"

        saved_phrase_button = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/div[2]/div/button/span"))

        )

        saved_phrase_button.click()

        print("Clicked 'I saved my recovery phrase'")

        

        time.sleep(2)  # Wait for transition

        

        # Click on Paste button

        paste_button = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/form/div/div[1]/div[2]/div[3]/button[1]/span"))

        )

        paste_button.click()

        print("Clicked Paste button")

        

        # Wait for potential permission popup and handle it

        try:

            # Look for the permission dialog

            permission_allow = WebDriverWait(driver, 5).until(

                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Allow') or contains(text(), 'Allow site to access clipboard')]"))

            )

            permission_allow.click()

            print("Clicked Allow on clipboard permission popup")

        except TimeoutException:

            print("No clipboard permission popup detected or it was already allowed")

        

        time.sleep(2)  # Wait for paste operation to complete

        

        # Click on Continue

        continue_button = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/form/div/div[2]/div/button/span"))

        )

        continue_button.click()

        print("Clicked Continue button")

        

        # Fill in the password fields

        password = "happymart212"

        new_password_field = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/form/div/div[1]/div[2]/div[1]/div/div/div/div/input"))

        )

        new_password_field.send_keys(password)

        print("Entered new password")

        

        repeat_password_field = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/form/div/div[1]/div[2]/div[2]/div/div/div/div/input"))

        )

        repeat_password_field.send_keys(password)

        print("Entered repeated password")

        

        # Click Continue

        continue_button = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/form/div/div[2]/button/span"))

        )

        continue_button.click()

        print("Clicked Continue button after password")

        

        # Wait for the "Enter Solana" button to appear

        time.sleep(4)  # Extra wait time for page transition

        

        # Click on Enter Solana

        enter_solana_button = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/div[2]/div/button[2]/span"))

        )

        enter_solana_button.click()

        print("Clicked Enter Solana")

        

        # Wait for dashboard to load

        time.sleep(5)

        

        # Save the recovery phrase to the JSON file

        account_info = {

            "approval_number": 0,  # Initial creation, no approvals yet

            "recovery_phrase": recovery_phrase,

            "password": password,

            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")

        }

        recovery_phrases.append(account_info)

        

        # Save to JSON file

        with open(json_file, "w") as f:

            json.dump(recovery_phrases, f, indent=4)

        print(f"Saved recovery phrase to {json_file}")

        

        # Main loop for approvals

        run_approval_process(driver, num_approvals, recovery_phrase, password, recovery_phrases, json_file)

    

    except Exception as e:

        print(f"An unexpected error occurred: {e}")

        import traceback

        traceback.print_exc()

        

        # Save any collected phrases even if an error occurred

        if recovery_phrases:

            with open(json_file, "w") as f:

                json.dump(recovery_phrases, f, indent=4)

            print(f"Saved collected recovery phrases to {json_file} before exit")

    

    finally:

        # Close the browser if headless, otherwise wait for user input

        if headless:

            driver.quit()

            print("Browser closed automatically in headless mode")

        else:

            input("Press Enter to close the browser...")

            driver.quit()



def import_and_approve_account(num_approvals=1, phrase_index=0, headless=False):

    # Set up Chrome options

    chrome_options = webdriver.ChromeOptions()

    

    # Add headless mode if requested

    if headless:

        chrome_options.add_argument("--headless")

        chrome_options.add_argument("--disable-gpu")  # Required for some systems

        chrome_options.add_argument("--window-size=1920,1080")  # Set window size for headless mode

    

    # Add permissions for clipboard access

    chrome_options.add_experimental_option("prefs", {

        "profile.default_content_settings.popups": 0,

        "profile.default_content_setting_values.notifications": 1,

        "profile.default_content_setting_values.clipboard": 1

    })

    

    # Initialize the driver

    driver = webdriver.Chrome(options=chrome_options)

    if not headless:

        driver.maximize_window()

    

    # Load the JSON file for stored recovery phrases

    json_file = "solflare.json"

    if not os.path.exists(json_file):

        print("Error: solflare.json file not found. Please create an account first.")

        driver.quit()

        return

    

    with open(json_file, "r") as f:

        recovery_phrases = json.load(f)

    

    if not recovery_phrases or len(recovery_phrases) <= phrase_index:

        print("Error: No recovery phrases found in the JSON file or index out of range.")

        driver.quit()

        return

    

    # Get the recovery phrase from the JSON file

    recovery_phrase = recovery_phrases[phrase_index]["recovery_phrase"]

    password = recovery_phrases[phrase_index]["password"]

    

    try:

        # Navigate to the Solflare access page

        driver.get("https://solflare.com/onboard/access")

        print("Navigated to Solflare access page")

        

        # Copy the recovery phrase to clipboard

        pyperclip.copy(recovery_phrase)

        print("Copied recovery phrase to clipboard")

        

        # Wait for a moment

        time.sleep(2)

        

        # Click on Paste button

        paste_button = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/form/div/div[1]/div[2]/div[5]/button[1]/span"))

        )

        paste_button.click()

        print("Clicked Paste button")

        

        # Wait for potential permission popup and handle it

        try:

            # Look for the permission dialog

            permission_allow = WebDriverWait(driver, 5).until(

                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Allow') or contains(text(), 'Allow site to access clipboard')]"))

            )

            permission_allow.click()

            print("Clicked Allow on clipboard permission popup")

        except TimeoutException:

            print("No clipboard permission popup detected or it was already allowed")

        

        time.sleep(2)  # Wait for paste operation to complete

        

        # Click on Continue

        continue_button = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/form/div/div[2]/div/button/span"))

        )

        continue_button.click()

        print("Clicked Continue button")

        

        # Fill in the password fields

        new_password_field = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/form/div/div[1]/div[2]/div[1]/div/div/div/div/input"))

        )

        new_password_field.send_keys(password)

        print("Entered new password")

        

        repeat_password_field = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/form/div/div[1]/div[2]/div[2]/div/div/div/div/input"))

        )

        repeat_password_field.send_keys(password)

        print("Entered repeated password")

        

        # Click Continue

        continue_button = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/form/div/div[2]/button/span"))

        )

        continue_button.click()

        print("Clicked Continue button after password")

        

        # Wait for the page transition

        time.sleep(2)

        

        # Click Quick Setup

        try:

            quick_setup_button = WebDriverWait(driver, 10).until(

                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/div[2]/div[2]/div/button[2]/span"))

            )

            quick_setup_button.click()

            print("Clicked Quick Setup")

        except TimeoutException:

            print("Quick Setup button not found, might be already past this step")

        

        # Wait for the "Enter Solana" button to appear

        time.sleep(2)  # Extra wait time for page transition

        

        # Click on Enter Solana

        enter_solana_button = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/div[2]/div/button[2]/span"))

        )

        enter_solana_button.click()

        print("Clicked Enter Solana")

        

        # Wait for dashboard to load

        time.sleep(5)

        

        # Main loop for approvals

        run_approval_process(driver, num_approvals, recovery_phrase, password, recovery_phrases, json_file, phrase_index)

    

    except Exception as e:

        print(f"An unexpected error occurred: {e}")

        import traceback

        traceback.print_exc()

    

    finally:

        # Close the browser if headless, otherwise wait for user input

        if headless:

            driver.quit()

            print("Browser closed automatically in headless mode")

        else:

            input("Press Enter to close the browser...")

            driver.quit()



def run_approval_process(driver, num_approvals, recovery_phrase, password, recovery_phrases, json_file, phrase_index=None):

    approvals_completed = 0

    

    while approvals_completed < num_approvals:

        print(f"Starting approval process {approvals_completed+1}/{num_approvals}")

        

        # Start the Win a share process with retry mechanism

        max_retries = 100

        for attempt in range(max_retries):

            try:

                print(f"Attempting to click 'Win a share' (attempt {attempt+1})")

                

                # Check for and close any dialogs first

                try:

                    # Look for dialog close buttons or X buttons that might be blocking clicks

                    close_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'close') or contains(@class, 'close')]")

                    if close_buttons:

                        for button in close_buttons:

                            try:

                                button.click()

                                print("Closed a dialog that might be blocking clicks")

                                time.sleep(1)

                            except:

                                pass

                except:

                    pass

                

                # Click on Win a share of 70k $USDC

                win_share_button = WebDriverWait(driver, 20).until(

                    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div/div[2]/div/div/div/div[3]/div/div/div[1]"))

                )

                

                # Scroll to make sure it's in view

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", win_share_button)

                time.sleep(1)

                

                # Try using JavaScript to click if normal click might be intercepted

                try:

                    win_share_button.click()

                except ElementClickInterceptedException:

                    print("Click intercepted, trying JavaScript click")

                    driver.execute_script("arguments[0].click();", win_share_button)

                

                print("Clicked Win a share of 70k $USDC")

                

                # Wait for the Next button to appear

                time.sleep(3)

                

                # Click Next

                next_button = WebDriverWait(driver, 20).until(

                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div/div/div[1]/div[3]/div/button/span"))

                )

                next_button.click()

                print("Clicked Next")

                

                # Wait for transition

                time.sleep(2)

                

                # Click Continue

                continue_button = WebDriverWait(driver, 20).until(

                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div/div/div[1]/div[3]/div/button[2]/span"))

                )

                continue_button.click()

                print("Clicked Continue")

                

                # Wait enough time for either error or trust site dialog to appear

                time.sleep(2)

                

                # Check for both possible outcomes

                trust_site_present = False

                error_present = False

                

                # First check for trust site dialog

                try:

                    trust_site_element = WebDriverWait(driver, 2).until(

                        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'I trust this site')]"))

                    )

                    trust_site_present = True

                    print("Trust site dialog detected")

                except TimeoutException:

                    trust_site_present = False

                

                # Then check for error message

                try:

                    error_element = WebDriverWait(driver, 2).until(

                        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Request failed with status code 400')]"))

                    )

                    error_present = True

                    print("Error 400 detected")

                except TimeoutException:

                    try:

                        # Try another way to detect error

                        error_element = WebDriverWait(driver, 2).until(

                            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[3]/div/div/div/div/div/div/div/div[1]"))

                        )

                        error_text = error_element.text

                        if "Request failed" in error_text or "400" in error_text:

                            error_present = True

                            print(f"Error detected: {error_text}")

                    except TimeoutException:

                        error_present = False

                

                # Handle the detected outcome

                if trust_site_present:

                    # Click I trust this site

                    trust_site_element.click()

                    print("Clicked I trust this site")

                    

                    # Click Approve

                    approve_button = WebDriverWait(driver, 15).until(

                        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Approve')]"))

                    )

                    approve_button.click()

                    print("Clicked Approve")

                    

                    # Wait for approval to process

                    time.sleep(5)

                    

                    # Update or add the approval info to JSON

                    if phrase_index is not None:

                        # Update existing record for imported account

                        recovery_phrases[phrase_index]["approval_number"] += 1

                        recovery_phrases[phrase_index]["last_approval_timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

                    else:

                        # Update the account info for new account

                        account_info = {

                            "approval_number": approvals_completed + 1,

                            "recovery_phrase": recovery_phrase,

                            "password": password,

                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")

                        }

                        recovery_phrases.append(account_info)

                    

                    # Save to JSON file

                    with open(json_file, "w") as f:

                        json.dump(recovery_phrases, f, indent=4)

                    print(f"Saved recovery phrase to {json_file}")

                    

                    # Increment approvals counter

                    approvals_completed += 1

                    print(f"Successfully completed approval {approvals_completed}/{num_approvals}")

                    

                    print("Clearing cookies and site data without refreshing...")

                    driver.delete_all_cookies()

                    driver.execute_script("localStorage.clear();")

                    driver.execute_script("sessionStorage.clear();")

                    time.sleep(2)  # Small pause after clearing data

                    

                    # Break out of the retry loop

                    break

                    

                elif error_present:

                    print("Error 400 detected, clearing cookies and site data...")

                    driver.delete_all_cookies()

                    driver.execute_script("localStorage.clear();")

                    driver.execute_script("sessionStorage.clear();")

                    time.sleep(2)  # Small pause after clearing data

                    print("Continuing to next attempt after error")

                    

                else:

                    print("Neither trust site dialog nor error detected, waiting longer...")

                    time.sleep(3)

                    

                    # Try looking for trust site dialog again

                    try:

                        trust_site_element = WebDriverWait(driver, 5).until(

                            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'I trust this site')]"))

                        )

                        trust_site_element.click()

                        print("Clicked I trust this site (delayed detection)")

                        

                        # Click Approve

                        approve_button = WebDriverWait(driver, 15).until(

                            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Approve')]"))

                        )

                        approve_button.click()

                        print("Clicked Approve")

                        

                        # Wait for approval to process

                        time.sleep(5)

                        

                        # Update or add the approval info to JSON

                        if phrase_index is not None:

                            # Update existing record for imported account

                            recovery_phrases[phrase_index]["approval_number"] += 1

                            recovery_phrases[phrase_index]["last_approval_timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

                        else:

                            # Update the account info for new account

                            account_info = {

                                "approval_number": approvals_completed + 1,

                                "recovery_phrase": recovery_phrase,

                                "password": password,

                                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")

                            }

                            recovery_phrases.append(account_info)

                        

                        # Save to JSON file

                        with open(json_file, "w") as f:

                            json.dump(recovery_phrases, f, indent=4)

                        print(f"Saved recovery phrase to {json_file}")

                        

                        # Increment approvals counter

                        approvals_completed += 1

                        print(f"Successfully completed approval {approvals_completed}/{num_approvals}")

                        

                        print("Clearing cookies and site data without refreshing...")

                        driver.delete_all_cookies()

                        driver.execute_script("localStorage.clear();")

                        driver.execute_script("sessionStorage.clear();")

                        time.sleep(2)  # Small pause after clearing data

                        

                        # Break out of the retry loop

                        break

                    except TimeoutException:

                        print("Still no trust site dialog, continuing without refreshing")

                        # Continue with the next attempt

            

            except (TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException) as e:

                print(f"Error occurred: {e}")

                print(f"Retrying... (attempt {attempt+1}/{max_retries})")

                

                # Try to handle any dialogs or overlays that might be blocking clicks

                try:

                    # Try clicking on the body to dismiss any tooltips or small popups

                    driver.find_element(By.TAG_NAME, "body").click()

                except:

                    pass

                

                time.sleep(2)

        

        # If we've exhausted all retries but haven't incremented the counter for this loop iteration

        if attempt == max_retries - 1 and approvals_completed < (num_approvals - max_retries + 1 + attempt):

            print(f"Failed to complete approval after {max_retries} attempts. Trying a full page refresh...")

            

            # Try a more aggressive approach - refresh the page completely

            driver.get("https://solflare.com")

            time.sleep(5)

            

            # After refresh, we might need to log in again

            try:

                # Look for unlock wallet button

                unlock_button = WebDriverWait(driver, 10).until(

                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Unlock Wallet') or contains(text(), 'Enter Solana')]"))

                )

                unlock_button.click()

                print("Clicked Unlock Wallet")

                

                # Enter password

                password_field = WebDriverWait(driver, 10).until(

                    EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))

                )

                password_field.send_keys(password)

                print("Entered password")

                

                # Click Unlock button

                unlock_button = WebDriverWait(driver, 10).until(

                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Unlock') or contains(text(), 'Enter')]"))

                )

                unlock_button.click()

                print("Clicked Unlock button")

                

                time.sleep(5)  # Wait for dashboard to load

            except:

                print("Could not find login elements, may already be logged in or different page state")



def parallel_import_and_approve(num_approvals, parallel_count, starting_index=0, headless=False):

    # Load the JSON file for stored recovery phrases

    json_file = "solflare.json"

    if not os.path.exists(json_file):

        print("Error: solflare.json file not found. Please create an account first.")

        return

    

    with open(json_file, "r") as f:

        recovery_phrases = json.load(f)

    

    # Determine how many parallel instances we can actually run

    available_phrases = len(recovery_phrases) - starting_index

    if available_phrases < parallel_count:

        print(f"Warning: Only {available_phrases} phrases available from index {starting_index}. Adjusting parallel count.")

        parallel_count = max(1, available_phrases)

    

    print(f"Starting {parallel_count} parallel instances for approvals")

    

    # Create and start threads

    threads = []

    for i in range(parallel_count):

        phrase_index = starting_index + i

        if phrase_index >= len(recovery_phrases):

            break

            

        thread = threading.Thread(

            target=import_and_approve_account,

            args=(num_approvals, phrase_index, headless)

        )

        threads.append(thread)

        thread.start()

        print(f"Started thread {i+1} using phrase at index {phrase_index}")

        time.sleep(2)  # Small delay between starting threads

    

    # Wait for all threads to complete

    for i, thread in enumerate(threads):

        thread.join()

        print(f"Thread {i+1} completed")

    

    print("All parallel approvals completed!")



if __name__ == "__main__":

    print("Select an option:")

    print("1. Create account and run approve")

    print("2. Import account and run approve")

    choice = input("Enter choice (1 or 2): ")

    

    if choice == "1":

        # Ask for number of approvals

        num_approvals = int(input("How many approvals do you want to make? "))

        create_and_approve_account(num_approvals)

    

    elif choice == "2":

        # Ask for number of approvals and parallel instances

        num_approvals = int(input("How many approvals per account do you want to make? "))

        parallel_count = int(input("How many parallel approvals do you want to run? (max 5): "))

        

        # Validate parallel count

        parallel_count = min(5, max(1, parallel_count))

        

        # Optional: ask for starting index

        use_custom_index = input("Do you want to specify a starting index for accounts? (y/n): ").lower()

        starting_index = 0

        if use_custom_index == 'y':

            starting_index = int(input("Enter starting index: "))

        

        parallel_import_and_approve(num_approvals, parallel_count, starting_index)

    

    else:

        print("Invalid choice. Exiting.")