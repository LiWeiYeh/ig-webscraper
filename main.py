from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import time

CHROMEDRIVER_PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(CHROMEDRIVER_PATH)
USERNAME = "yifox95333@sanizr.com"
PASSWORD = "definitelynotabot"


def main():
    driver.get("https://www.instagram.com/")

    login = Login(driver, USERNAME, PASSWORD)
    login.signin()
    
    account = Account(driver)
    account.get_profile("liwei.y_")
    account.get_followers_list()

class Account():
    def __init__(self, driver):
        self.driver = driver

    def get_profile(self, username):
        self.driver.get("https://www.instagram.com/{}".format(username))

    def get_followers_count(self):
        followers_selector = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > header > section > ul > li:nth-child(2) > a')))
        return followers_selector.text

    def get_followers_list(self):
        followers_selector = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > header > section > ul > li:nth-child(2) > a')))
        followers_selector.click()

        followers_popup = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'body > div.RnEpo.Yx5HN > div > div > div.isgrP')))

        last_height = driver.execute_script("return document.getElementsByClassName('isgrP')[0].scrollHeight", followers_popup)
        while True:
            driver.execute_script("arguments[0].scrollTo(0, document.getElementsByClassName('isgrP')[0].scrollHeight)", followers_popup)

            time.sleep(0.5)            
            new_height = driver.execute_script("return document.getElementsByClassName('isgrP')[0].scrollHeight", followers_popup)
            print(new_height)
            if new_height == last_height:
                break
            
            last_height = new_height

        followers = []
        follower_elements = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, 'body > div.RnEpo.Yx5HN > div > div > div.isgrP > ul > div > li > div > div.t2ksc > div.enpQJ > div.d7ByH > span > a')))
        for follower_item in follower_elements:
            followers.append(follower_item.text)

    def get_followings_count(self):
        followings_selector = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > header > section > ul > li:nth-child(3) > a')))
        return followings_selector

    def get_followings_list(self):
        followings_selector = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > header > section > ul > li:nth-child(3) > a')))
        followings_selector.click()



class Login():
    def __init__(self, driver, username, password):
        self.driver = driver
        self.username = username
        self.password = password
    
    def signin(self):
        username_selector = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#loginForm > div > div:nth-child(1) > div > label > input")))
        username_selector.send_keys(self.username)
        username_selector.send_keys(Keys.RETURN)

        password_selector = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#loginForm > div > div:nth-child(2) > div > label > input")))
        password_selector.send_keys(self.password)
        password_selector.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#react-root > section > main > div > div > div > section > div > div.olLwo")))



if __name__ == '__main__':
    main()