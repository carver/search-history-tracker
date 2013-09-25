from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import re
import time
import unittest

try:
    import config
except ImportError:
    exit('You must copy the file config.example.py to config.py and fill in your details')

MAX_RESULTS = 50

def is_element_present(driver, how, what):

    try: driver.find_element(by=how, value=what)
    except NoSuchElementException as e: return False
    return True

searches = []
if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get("https://accounts.google.com/Login?continue=https://history.google.com/&hl=en")
    driver.find_element_by_id("Email").send_keys(config.google['user'])
    driver.find_element_by_id("Passwd").send_keys(config.google['password'])
    driver.find_element_by_id("signIn").click()
    #driver.find_element_by_css_selector("em").click()
    assert "Daily search activity" == driver.find_element_by_xpath("//div[@id='first_row']/div[2]/h4").text, "login failed, couldn't find usual title"
    
    try:
        driver.implicitly_wait(1)
        searches.extend(driver.find_element_by_id("bkmk_href_%d" % i).text for i in range(MAX_RESULTS))
    except NoSuchElementException:
        print("found %d searches" % len(searches))
    else:
        print("found up to the max of %d searches" % MAX_RESULTS)
    finally:
        driver.implicitly_wait(30)

    driver.quit()
    
    path = config.result_path
    with open('%smy-searches.txt' % path ,'a') as f:
        f.write('\n'.join(reversed(searches))+'\n')
