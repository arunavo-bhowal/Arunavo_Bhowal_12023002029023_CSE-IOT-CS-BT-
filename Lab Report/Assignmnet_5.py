from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://rahulshettyacademy.com/AutomationPractice/")

headers = driver.find_elements(By.XPATH, "//table[@id='product']/thead/tr/th")
rows = driver.find_elements(By.XPATH, "//table[@id='product']/tbody/tr")

for header in headers:
    print(header.text, end=" | ")

print()

for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")

    for column in columns:
        print(column.text, end=" | ")

    print()

driver.quit()