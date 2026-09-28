import time
from selenium import webdriver
from selenium.webdriver.common.by import By


driver=webdriver.Chrome()
driver.get("https://www.google.com")

driver.find_element(By.LINK_TEXT,"About").click()

time.sleep(40)

driver.quit()



