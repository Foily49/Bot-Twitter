from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time

# Load Twitter credentials from environment variables
load_dotenv()
USERNAME = os.getenv('name')
PASSWORD = os.getenv('password')

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

def post_tweet(caption):
    try:
        # Navigate to the home page
        driver.get("https://twitter.com/home")
        wait = WebDriverWait(driver, 20)
        print("Navigated to Twitter home page")

        # Click on the Tweet button
        tweet_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/compose/tweet"]')))
        tweet_button.click()
        print("Clicked Tweet button")

        # Wait for the Tweet dialog to appear
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div')))
        print("Tweet dialog opened")

        # Enter the caption
        caption_field = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div')
        caption_field.click()
        caption_field.send_keys(caption)
        print("Entered caption")

        # Click on the Tweet button to post
        post_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span')
        post_button.click()
        print("Posted the tweet")
    except Exception as e:
        print("Error posting tweet:", e)

def main():
    caption = 'Your caption here'  # Replace with your caption

    login_to_twitter()
    post_tweet(caption)

if __name__ == "__main__":
    main()