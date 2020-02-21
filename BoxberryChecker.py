import datetime
import simpleaudio as sa
import wave
import ffmpeg
import ffprobe
from pydub import AudioSegment
from pydub.playback import play
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import time
import re
import math
import os

chrome_options = Options()
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--no-sandbox')

URL = "https://lk.boxberry.ru/auth/?redirectTo=%2F"

def login():
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=r'/Users/voronin/ToolsAndGiggles/chromedriver 2')
    driver.maximize_window()
    try:
        driver.get(URL)
        driver.find_element_by_xpath("//input[@id='username']").send_keys("89802479159")
        driver.find_element_by_xpath("//input[@id='password']").send_keys("847W&OD&3A#s")
        driver.find_element_by_xpath("//div[@class='bt1']//input").click()
        time.sleep(5)
    except NoSuchElementException:
        driver.save_screenshot("screenshot1.png")
        pass
    return driver


def check_status():
    driver = login()
    try:
        while True:
            start_time = time.time()
            try:
                driver.refresh()
                time.sleep(5)
                p = driver.find_element_by_xpath("//li[@class='j2']//b")
                print(datetime.datetime.now(), p.text)
                if p.text != "Поступит в пункт выдачи в течение 1-2 рабочих дней, о чем Вы получите уведомление по SMS":
                    sound = AudioSegment.from_mp3('Rooster-morning-sound.mp3')
                    play(sound)
                time.sleep(120)
            except NoSuchElementException:
                print(time.time() - start_time)
                driver.save_screenshot("screenshot.png")
                driver.close()
                driver = login()
    except KeyboardInterrupt:
        driver.close()
        return "Yikes"

