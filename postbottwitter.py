from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
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

class TwitterBot:
    def __init__(self):
        self.bot = driver
        self.is_logged_in = False

    def login_to_twitter(self):
        try:
            self.bot.get("https://twitter.com/login")
            wait = WebDriverWait(self.bot, 20)
            print("Navigated to Twitter login page")

            username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
            username_field.send_keys(USERNAME)
            print("Entered username")

            next_button = self.bot.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            print("Clicked Next button")

            password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.send_keys(PASSWORD)
            print("Entered password")
            password_field.send_keys(Keys.RETURN)

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/home"]')))
            print("Login successful")
            self.is_logged_in = True
        except Exception as e:
            print("Error during login:", e)
            self.bot.quit()
            exit()

    def post_tweet(self, tweet_body):
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        bot = self.bot

        try:
            bot.find_element(By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']").click()
        except NoSuchElementException:
            time.sleep(3)
            bot.find_element(By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']").click()

        time.sleep(4)
        body = tweet_body

        try:
            bot.find_element(By.XPATH, "//div[@role='textbox']").send_keys(body)
        except NoSuchElementException:
            time.sleep(3)
            bot.find_element(By.XPATH, "//div[@role='textbox']").send_keys(body)

        time.sleep(4)
        try:
            tweet_button=bot.find_element(By.CSS_SELECTOR, "[data-testid='tweetButton']")
            tweet_button.click()
            print("Clicked the tweet button")
        except NoSuchElementException:
            print("Error: Tweet button not found")
        time.sleep(4)
        print("Tweet posted successfully")

def main():
    tweet_body = 'Your tweet here'  # Replace with your tweet text

    twitter_bot = TwitterBot()
    twitter_bot.login_to_twitter()
    twitter_bot.post_tweet(tweet_body)

if __name__ == "__main__":
    main()