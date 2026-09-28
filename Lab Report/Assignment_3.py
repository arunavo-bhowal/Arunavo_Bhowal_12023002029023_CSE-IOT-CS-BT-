from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://rahulshettyacademy.com/AutomationPractice/")

wait = WebDriverWait(driver, 10)

checkboxes = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "input[type='checkbox']")
    )
)

checkboxes[0].click()
checkboxes[1].click()

print("Option 1 selected:", checkboxes[0].is_selected())
print("Option 2 selected:", checkboxes[1].is_selected())

autocomplete = wait.until(
    EC.element_to_be_clickable(
        (By.ID, "autocomplete")
    )
)

autocomplete.send_keys("Ind")

suggestions = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".ui-menu-item")
    )
)

for suggestion in suggestions:
    if "India" in suggestion.text:
        suggestion.click()
        print("Selected country:", suggestion.text)
        break

driver.quit()