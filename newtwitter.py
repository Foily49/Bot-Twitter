from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os

# Load Twitter credentials from environment variables
load_dotenv()
USERNAME = os.getenv('name')
PASSWORD = os.getenv('password')

# Target profile username
TARGET_PROFILE = 'Sarabellalondon'  # Change this to the specified user

# Setup Chrome WebDriver
service = Service('E:\\\\Twitter bot\\\\chromedriver.exe')
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
            # Extract followers
            followers_elements = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')
            print(f"Found {len(followers_elements)} followers")

            for follower_element in followers_elements:
                try:
                    # Adding debug information
                    print(f"Follower element text: {follower_element.text}")
                    
                    # Attempting to find the username by locating the span that starts with @
                    spans = follower_element.find_elements(By.XPATH, './/span')
                    for span in spans:
                        if span.text.startswith('@'):
                            username = span.text
                            followers_list.add(username)
                            break
                except Exception as e:
                    print("Error extracting a follower username:", e)
                    continue

            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for the page to load

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print(f"Extracted {len(followers_list)} followers")
    except Exception as e:
        print("Error extracting followers:", e)
    return list(followers_list)

def follow_followers(followers_list):
    for username in followers_list:
        try:
            # Navigate to the follower's profile page
            driver.get(f"https://twitter.com/{username}")
            time.sleep(3)  # Wait for the page to load properly
            
            # Find the follow button and click it
            try:
                follow_button = driver.find_element(By.XPATH, '//div[@data-testid="placementTracking"]//span[text()="Follow"]')
                follow_button.click()
                print(f"Followed {username}")
            except Exception as e:
                print(f"Could not find follow button for {username}: {e}")
                continue

        except Exception as e:
            print("Error following user:", e)

def main():
    try:
        login_to_twitter()
        followers_list = extract_followers(TARGET_PROFILE)
        print("Followers:", followers_list)  # Print out the list of followers for verification
        follow_followers(followers_list)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()