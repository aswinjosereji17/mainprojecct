from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class Hosttest(TestCase):

   
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000'

    def tearDown(self):
        self.driver.quit()


    def testing(self):

        # login
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        theme=driver.find_element(By.CSS_SELECTOR,"button.dropdown-toggle[data-toggle='dropdown']")
        theme.click()
        time.sleep(1)
        theme=driver.find_element(By.CSS_SELECTOR,"button.dropdown-item > a[href='/login_user']")
        theme.click()
        elem = driver.find_element(By.NAME, "username")
        elem.send_keys("user17")
        elem = driver.find_element(By.NAME, "password")
        elem.send_keys("User17@2023")
        time.sleep(1)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button#submit.submitbtn")
        submit_button.click()
        time.sleep(1)
      
      #redirect to user dashboard
        browse=driver.find_element(By.CSS_SELECTOR,"div.custom-dropdownn")
        browse.click()
        time.sleep(1)
        browse=driver.find_element(By.CSS_SELECTOR,"a[href='/user_profile/']")
        browse.click()
        time.sleep(1)
       

        #logout
        browse=driver.find_element(By.CSS_SELECTOR,"a#logt.nav-link.collapsed > span")
        browse.click()
        time.sleep(2)


     

if __name__ == '__main__':
    import unittest
    unittest.main()