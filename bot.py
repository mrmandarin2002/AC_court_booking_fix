# fuck AC
import time

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

profile = webdriver.FirefoxProfile()
profile.set_preference('permissions.default.image', 2)

from CONSTS import *
from SECRETS import *

class Bot:

    def __init__(self, court : int, booking_times : list, back, skip : int = 0):
        self.skip = skip
        self.back = back
        self.court = court
        self.booking_times = booking_times
        # make sure it is threaded so we can run multiple of these at the same time
        Process(target = self.start).start()
        self.clicked = 0

    # where the magic happens
    def start(self):
        self.driver = webdriver.Firefox(firefox_profile = profile, service=Service(GeckoDriverManager().install()), options = options)
        self.driver.get(COURTS[self.court])

        time.sleep(0.5)
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
        
        date = '0'
        # keep on looping, we try clicking every book button
        while True:

            startTime = time.time()
            #time.sleep(0.4)
            #date_button = self.driver.find_element_by_xpath("//button[@class='btn btn-secondary single-date-select-button single-date-select-one-click'][2]")
            date_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-secondary single-date-select-button single-date-select-one-click'][2]"))
            )
            # print("Presence Time: ", time.time() - startTime) 

            new_date = date_button.get_attribute("data-day")
            #print(new_date)
            if date != new_date:
                print("IN NEW DATE!")
                date_button.click()
                date = new_date
                book_buttons = [0]
                
                while len(book_buttons):
                    book_buttons = self.driver.find_elements(By.XPATH, "//button[@class='btn btn-primary']")
                    del book_buttons[0]
                    if self.back:
                        book_buttons.reverse()

                    try:
                        if book_buttons:
                            book_buttons[min(self.skip, len(book_buttons) - 1)].click()
                            print("BOOKED!")
                    except:
                        print("OOOPSSS")

            
            self.driver.get(COURTS[self.court])
            # print("Time taken:", time.time() - startTime)
            # print("------------")



if __name__ == '__main__':
    bots = []
    for i in range(4):
        bots.append(Bot(1, [], skip = i, back = True))
        bots.append(Bot(1, [], skip = i, back = True))
        bots.append(Bot(1, [], skip = i, back = True))
        bots.append(Bot(1, [], skip = i, back = True))

#bots = [Bot(i, []) for i in range(3)]




