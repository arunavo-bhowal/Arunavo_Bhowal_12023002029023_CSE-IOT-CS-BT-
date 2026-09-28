import time
from selenium import webdriver
from selenium.webdriver.common.by import By


driver=webdriver.Chrome()
driver.get("https://testautomationpractice.blogspot.com")

driver.find_element(By.ID,"name").send_keys("Rachel")

button=driver.find_element(By.TAG_NAME,"button")
print(button.text)

genders = driver.find_elements(By.NAME, "gender")
for gender in genders:
    gender_id = gender.get_attribute("id")
    label = driver.find_element(
        By.CSS_SELECTOR,
        f"label[for='{gender_id}']"
    )
    print(label.text)

time.sleep(40)
driver.quit()