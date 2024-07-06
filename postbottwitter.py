import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import os

# Load Twitter credentials from environment variables
load_dotenv()
USERNAME = os.getenv('name')
PASSWORD = os.getenv('password')

# Path to the media file you want to upload
media_path = r'E:\\Twitter bot\\pic1.png'  # Replace with the actual path to your media file

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

    def post_tweet_with_media(self, tweet_body, media_path):
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        bot = self.bot

        try:
            bot.find_element(By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']").click()
        except NoSuchElementException:
            time.sleep(3)
            bot.find_element(By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']").click()

        time.sleep(4)

        try:
            bot.find_element(By.XPATH, "//div[@role='textbox']").send_keys(tweet_body)
        except NoSuchElementException:
            time.sleep(3)
            bot.find_element(By.XPATH, "//div[@role='textbox']").send_keys(tweet_body)

        time.sleep(4)

        try:
            # Upload the media file
            media_input = bot.find_element(By.XPATH, '//input[@type="file"]')
            media_input.send_keys(media_path)
            print("Uploaded media")

            # Wait for the media to be fully uploaded
            time.sleep(4)

            tweet_button = bot.find_element(By.CSS_SELECTOR, "[data-testid='tweetButton']")
            tweet_button.click()
            print("Clicked the tweet button")
        except NoSuchElementException:
            print("Error: Tweet button not found")
        time.sleep(4)
        print("Tweet with media posted successfully")

    def schedule_tweet(self, tweet_body, media_path, post_time):
        def job():
            self.login_to_twitter()
            self.post_tweet_with_media(tweet_body, media_path)
            driver.quit()

        schedule.every().day.at(post_time).do(job)
        print(f"Tweet scheduled at {post_time}")

        while True:
            schedule.run_pending()
            time.sleep(1)

def main():
    tweet_body = 'Your scheduled tweet with media'  # Replace with your tweet text
    post_time = "15:03"  # Replace with the desired post time in HH:MM format (24-hour clock)

    twitter_bot = TwitterBot()
    twitter_bot.schedule_tweet(tweet_body, media_path, post_time)

if __name__ == "__main__":
    main()