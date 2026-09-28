from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://demoqa.com/alerts")

driver.maximize_window()

driver.find_element(By.ID, "alertButton").click()

time.sleep(1)

alert = driver.switch_to.alert

print(alert.text)

alert.accept()

driver.find_element(By.ID, "confirmButton").click()

time.sleep(1)

confirm = driver.switch_to.alert

print(confirm.text)

confirm.dismiss()

driver.find_element(By.ID, "promtButton").click()

time.sleep(1)

prompt = driver.switch_to.alert

prompt.send_keys("Arunavo")

prompt.accept()

time.sleep(2)

driver.quit()