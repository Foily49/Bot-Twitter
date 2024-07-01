from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Twitter credentials
USERNAME = 'anastasia_luv7'
PASSWORD = 'Kelvin128'

# Target profile username
TARGET_PROFILE = 'waifuflare'

# Message to send
MESSAGE = "Hi! Thanks for following me. Have a great day!"

# Setup Chrome WebDriver
service = Service('E:\\Twitter bot\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

def login_to_twitter():
    try:
        driver.get("https://twitter.com/login")
        wait = WebDriverWait(driver, 20)
        print("Navigated to Twitter login page")

        username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        username_field.send_keys(USERNAME)
        print("Entered username")

        next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        next_button.click()
        print("Clicked Next button")

        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(PASSWORD)
        print("Entered password")
        password_field.send_keys(Keys.RETURN)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/home"]')))
        print("Login successful")
    except Exception as e:
        print("Error during login:", e)
        driver.quit()
        exit()

def extract_followers(profile_username):
    followers_list = set()  # Use a set to avoid duplicates
    try:
        driver.get(f"https://twitter.com/{profile_username}/followers")
        wait = WebDriverWait(driver, 20)
        print(f"Navigated to {profile_username}'s followers page")

        # Wait for the followers list to load
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="cellInnerDiv"]')))
        print("Followers page loaded")

        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            follower_elements = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]//div[@dir="ltr"]/span')
            for element in follower_elements:
                followers_list.add(element.text)
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for new followers to load
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print("Extracted followers:", followers_list)
        return followers_list

    except Exception as e:
        print("Error extracting followers:", e)
        driver.quit()
        exit()

def follow_and_message_followers(followers_list):
    for username in followers_list:
        try:
            # Navigate to the follower's profile page
            driver.get(f"https://twitter.com/{username}")
            time.sleep(3)  # Wait for the page to load properly

            # Follow the user
            try:
                follow_button = driver.find_element(By.XPATH, '//div[@data-testid="placementTracking"]//span[text()="Follow"]')
                follow_button.click()
                print(f"Followed {username}")
            except Exception as e:
                print(f"Could not find follow button for {username}: {e}")
                continue

            time.sleep(2)  # Wait for the follow action to complete

            # Find the message button and click it to initiate a message
            try:
                message_button = driver.find_element(By.XPATH, '//div[@data-testid="DMButton"]')
                message_button.click()
                print("Message button clicked")
            except Exception as e:
                print(f"Could not find message button for {username}: {e}")
                continue

            time.sleep(2)  # Wait for the message dialog to open

            # Find the message input field and send the message
            try:
                message_field = driver.find_element(By.XPATH, '//div[@data-testid="dmComposerTextInput"]')
                message_field.send_keys(MESSAGE)
                print("Message typed")
            except Exception as e:
                print(f"Could not find message field for {username}: {e}")
                continue

            # Find the send button and click it
            try:
                send_button = driver.find_element(By.XPATH, '//div[@data-testid="dmComposerSendButton"]')
                send_button.click()
                print("Send button clicked")
            except Exception as e:
                print(f"Could not find send button for {username}: {e}")
                continue

            print(f"Message sent to {username}")

        except Exception as e:
            print(f"Error interacting with {username}:", e)

def main():
    try:
        login_to_twitter()
        followers_list = extract_followers(TARGET_PROFILE)
        follow_and_message_followers(followers_list)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()