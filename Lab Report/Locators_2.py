import time
from selenium import webdriver
from selenium.webdriver.common.by import By


driver=webdriver.Chrome()

driver.get("https://rahulshettyacademy.com/AutomationPractice")

table = driver.find_element(By.CLASS_NAME, "table-display")

print(table.text)

time.sleep(40)
driver.quit()