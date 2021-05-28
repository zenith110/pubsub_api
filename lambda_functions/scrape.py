import requests 
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import os
chrome_driver = "chromedriver.exe"
zipcode = 32765
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver)

# Begin the web driver by starting on google
driver.get("https://www.publix.com/")
weekly_ad = driver.find_element_by_xpath('//*[@id="two-column-container"]/div[1]/div/div/ul/li[1]/a')
weekly_ad.click()
store_button = driver.find_element_by_xpath('//*[@id="main"]/div[4]/div[2]/div/div/button')
store_button.click()
store_search = driver.find_element_by_xpath('//*[@id="input_ZIPorCity,Stateorstorenumber106"]')
store_search.send_keys(zipcode)
store_search.send_keys(Keys.RETURN)
store_button_click = driver.find_element_by_xpath('//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[2]/div/ul/li[1]/div/button')
store_button_click.click()
print("Gonna switch pages!")
driver.get(driver.current_url + "/deli")
# store_keys = driver.find_element_by_class_name("text-input-wrapper")
# store_keys.send_keys()
# search.send_keys(Keys.RETURN)
# store_select = driver.find_element_by_class_name("choose-store-button button small")
# store_select.click()
