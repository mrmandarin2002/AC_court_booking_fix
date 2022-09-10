# fuck AC
from re import T
import time, os

from multiprocessing import Process

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

from CONSTS import *
from SECRETS import *

waitTime = 30

os.environ['GH_TOKEN'] = "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"

skips = [[] for i in range(10)]

class Bot:

    def __init__(self, court : int, booking_times : list, back, id : int, skip : int = 0):
        self.skip = skip
        self.back = back
        self.court = court
        self.booking_times = booking_times
        # make sure it is threaded so we can run multiple of these at the same time
        Process(target = self.start).start()
        self.clicked = 0

    # where the magic happens
    def start(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options = options)
        self.driver.get(COURTS[self.court])
        # presses "login with utorid button"
        time.sleep(1)
        WebDriverWait(self.driver, waitTime).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-primary btn-block btn-external-login btn-sign-in btn-sso-shibboleth']"))
        ).click()

        # fill username
        WebDriverWait(self.driver, waitTime).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys(UTORID)

        # fill password
        WebDriverWait(self.driver, waitTime).until(
            EC.presence_of_element_located((By.ID, "password"))
        ).send_keys(PASSWORD)

        # click submit
        WebDriverWait(self.driver, waitTime).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-primary btn-lg']"))
        ).click()

        # accept the fucking cookies
        WebDriverWait(self.driver, waitTime).until(
            EC.presence_of_element_located((By.ID, 'gdpr-cookie-accept'))
        ).click()
        self.date = '0'
        self.book()

    def book(self):     
        while True: 
            try:
                # keep on looping, we try clicking every book button
                startTime = time.time()
                date_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-secondary single-date-select-button single-date-select-one-click'][2]"))
                )
                # print("Presence Time: ", time.time() - startTime) 

                new_date = date_button.get_attribute("data-day")
                #print(new_date)
                if self.date != new_date:
                    print("IN NEW DATE!")
                    date_button.click()
                    self.date = new_date
                    book_buttons = [0]
                    
                    while len(book_buttons):
                        book_buttons = self.driver.find_elements(By.XPATH, "//button[@class='btn btn-primary']")
                        del book_buttons[0]

                        if book_buttons:
                            if self.back:
                                book_buttons.reverse()
                            book_buttons[min(self.skip, len(book_buttons) - 1)].click()
                            print("BOOKED!")
                            time.sleep(0.5)

                self.driver.get(COURTS[self.court]) 
                time.sleep(0.2)
            except:
                pass

court = 1


if __name__ == '__main__':
    bots = []
    for i in range(3):
        for x in range(6):
            bots.append(Bot(i, [], id = x, skip = 1, back = True))
            time.sleep(0.3)
    # testBot = Bot(0, [], id = 0, skip = 0, back = True)




