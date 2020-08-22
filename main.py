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
    webscraper = WebScraper(driver)
    webscraper.get_url("https://www.instagram.com/")

    login = Login(webscraper, USERNAME, PASSWORD)
    login.signin()

    account = Account(webscraper)
    account.get_profile("flyingpiggy._")

    name = account.get_name()
    print(name)

    followers_count = account.get_followers_or_following_count("followers")
    print("You have {}".format(followers_count))

    following_count = account.get_followers_or_following_count("following")
    print("You have {}".format(following_count))

    followers = account.get_followers_or_following_list("followers")

    following = account.get_followers_or_following_list("following")

    non_followers = list(filter(lambda x: x not in followers, following))
    
    print(non_followers)

class Account():
    def __init__(self, webscraper):
        self.webscraper = webscraper

    def get_profile(self, username):
        self.webscraper.get_url("https://www.instagram.com/{}".format(username))

    def get_name(self):
        selector = self.webscraper.get_selector('#react-root > section > main > div > header > section > div.-vDIg > h1')
        return selector.text

    def get_followers_or_following_count(self, list_type):
        selector = ""
        if list_type == "followers":
            selector = self.webscraper.get_selector('#react-root > section > main > div > header > section > ul > li:nth-child(2) > a')
        if list_type == "following":
            selector = self.webscraper.get_selector('#react-root > section > main > div > header > section > ul > li:nth-child(3) > a')

        return selector.text

    def get_followers_or_following_list(self, list_type):
        selector = ""
        if list_type == "followers":
            selector = self.webscraper.get_selector('#react-root > section > main > div > header > section > ul > li:nth-child(2) > a')
        if list_type == "following":
            selector = self.webscraper.get_selector('#react-root > section > main > div > header > section > ul > li:nth-child(3) > a')

        selector.click()

        popup_selector = self.webscraper.get_selector('body > div.RnEpo.Yx5HN > div > div > div.isgrP')

        last_height = self.webscraper.execute_script("return document.getElementsByClassName('isgrP')[0].scrollHeight", popup_selector)
        while True:
            self.webscraper.execute_script("arguments[0].scrollTo(0, document.getElementsByClassName('isgrP')[0].scrollHeight)", popup_selector)

            time.sleep(0.5)            
            new_height = self.webscraper.driver.execute_script("return document.getElementsByClassName('isgrP')[0].scrollHeight", popup_selector)
            if new_height == last_height:
                break
            
            last_height = new_height

        the_list = []
        the_list_elements = self.webscraper.get_selector('body > div.RnEpo.Yx5HN > div > div > div.isgrP > ul > div > li > div > div.t2ksc > div.enpQJ > div.d7ByH > span > a', True)
        for element in the_list_elements:
            the_list.append(element.text)

        close_selector = self.webscraper.get_selector("body > div.RnEpo.Yx5HN > div > div > div:nth-child(1) > div > div:nth-child(3) > button > div")
        close_selector.click()

        return the_list


class WebScraper():
    def __init__(self, driver):
        self.driver = driver

    def get_url(self, url):
        self.driver.get(url)


    def get_selector(self, selector, isMultiple=False):
        selector = self.wait(selector, isMultiple)
        return selector

    

    def wait(self, selector, isMultiple=False):
        if isMultiple == True:
            return WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
        else:
            return WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def execute_script(self, script, selector):
        self.driver.execute_script(script, selector)

class Login():
    def __init__(self, webscraper, username, password):
        self.webscraper = webscraper
        self.username = username
        self.password = password
    
    def signin(self):
        username_selector = self.webscraper.get_selector("#loginForm > div > div:nth-child(1) > div > label > input")
        username_selector.send_keys(self.username)

        password_selector = self.webscraper.get_selector("#loginForm > div > div:nth-child(2) > div > label > input")
        password_selector.send_keys(self.password)

        button_selector = self.webscraper.get_selector("#loginForm > div > div:nth-child(3) > button > div")
        button_selector.click()

        self.webscraper.wait("#react-root > section > main > div > div > div > section > div > div.olLwo")


if __name__ == '__main__':
    main()