from random import randint
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

amount_of_swipes = input("How many shall be swiped?\n")

service = Service("C:\Program Files (x86)\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

likes = 0
dislikes = 0
matches = 0


def print_stats():
    print("Likes: " + str(likes))
    print("Dislikes: " + str(dislikes))
    print("Matches: " + str(matches))


class TinderBot:
    def __init__(self):
        self.driver = webdriver.Chrome(service=service, options=options)

    def login(self):
        self.driver.get("https://tinder.com")

        sleep(1)
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[1]/div/div[1]/div/main/div["
                                 "1]/div/div/div/div/header/div/div[2]/div[2]/a/span").click()
        sleep(1)
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[2]/div/div/div[1]/div/div[3]/span/div[2]/button").click()

        sleep(1)
        # switch to login popup
        base_window = self.driver.current_window_handle
        chwd = self.driver.window_handles
        self.driver.switch_to.window(chwd[1])
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[2]").click()

        email_in = self.driver.find_element(By.ID, "email")
        email_in.send_keys("INSERT EMAIL-ADDRESS FOR FACEBOOK")
        pw_in = self.driver.find_element(By.ID, "pass")
        pw_in.send_keys("INSERT PASSWORD FOR FACEBOOK")

        self.driver.find_element(By.ID, "loginbutton").click()

        self.driver.switch_to.window(base_window)

        sleep(5)

        # First popup close
        self.driver.find_element(By.XPATH, "//*[@id='q-53386290']/div/div/div/div/div[3]/button[1]").click()

        # Second popup close
        self.driver.find_element(By.XPATH, "//*[@id='q-53386290']/div/div/div/div/div[3]/button[1]").click()

    def like(self):
        global likes
        webdriver.ActionChains(self.driver).key_down(Keys.ARROW_RIGHT).key_up(Keys.ARROW_RIGHT).perform()
        likes += 1

    def dislike(self):
        global dislikes
        webdriver.ActionChains(self.driver).key_down(Keys.ARROW_LEFT).key_up(Keys.ARROW_LEFT).perform()
        dislikes += 1

    def auto_swipe(self):
        for _ in range(int(amount_of_swipes)):
            try:
                self.driver.find_element(By.XPATH, "//*[@id='q-53386290']/div/div/div[1]/div[2]/div[1]/span["
                                                   "1]/div/div/span/div/h3")

            except Exception:
                sleep(0.8)
                try:
                    if randint(0, 10) < 8:
                        self.like()
                    else:
                        self.dislike()

                except Exception:
                    try:
                        self.close_popup()
                    except Exception:
                        self.close_match()

    def close_popup(self):
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[3]/button[2]").click()

    def close_match(self):
        global matches
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[3]/button[2]").click()
        matches += 1


bot = TinderBot()
bot.login()
bot.auto_swipe()
print("Auto-swiping has ended. Here are the stats:")
print_stats()
