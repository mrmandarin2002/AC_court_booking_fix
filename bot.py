# fuck AC
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

from CONSTS import *
from SECRETS import *

class Bot:

    def __init__(self, court : int, booking_times : list):
        self.court = court
        self.booking_times = booking_times
        # make sure it is threaded so we can run multiple of these at the same time
        threading.Thread(target = self.start).start()

    # where the magic happens
    def start(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.driver.get(COURTS[self.court])

        # presses "login with utorid button"
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-primary btn-block btn-external-login btn-sign-in btn-sso-shibboleth']"))
        ).click()

        # fill username
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys(UTORID)

        # fill password
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        ).send_keys(PASSWORD)

        # click submit
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-primary btn-lg']"))
        ).click()
        self.book()

    def book(self):

        # accept the fucking cookies
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'gdpr-cookie-accept'))
        ).click()

        # keep on looping, we try clicking every book button
        while True:

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-secondary single-date-select-button single-date-select-one-click'][2]"))
            ).click()

            time.sleep(0.15) # not sure if we need this... we'll see

            for book_button in self.driver.find_elements(By.XPATH, "//button[@class='btn btn-primary']"):
                # there's like hidden buttons or some shit dunno this seems to fix it
                try:
                    book_button.click()
                except:
                    pass

            time.sleep(0.2)
            self.driver.refresh()

bots = [Bot(i, []) for i in range(3)]




