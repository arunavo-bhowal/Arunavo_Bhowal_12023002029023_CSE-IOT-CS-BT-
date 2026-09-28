import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utils.helpers import (
    read_test_data, get_driver, open_page, click, type_text, get_text,
)


def main():
    data = read_test_data()
    driver = get_driver()

    open_page(driver, data["base_url"] + "/login")
    type_text(driver, By.CSS_SELECTOR, 'input[data-qa="signup-name"]', data["name"])
    type_text(driver, By.CSS_SELECTOR, 'input[data-qa="signup-email"]', data["email"])
    click(driver, By.CSS_SELECTOR, 'button[data-qa="signup-button"]')
    time.sleep(2)

    if "already exist" in driver.page_source:
        print("Account is already there. Nothing to do.")
        driver.quit()
        return

    click(driver, By.ID, "id_gender1")
    type_text(driver, By.ID, "password", data["password"])
    Select(driver.find_element(By.ID, "days")).select_by_value("10")
    Select(driver.find_element(By.ID, "months")).select_by_value("5")
    Select(driver.find_element(By.ID, "years")).select_by_value("1999")
    type_text(driver, By.ID, "first_name", data["first_name"])
    type_text(driver, By.ID, "last_name", data["last_name"])
    type_text(driver, By.ID, "address1", data["address"])
    Select(driver.find_element(By.ID, "country")).select_by_visible_text("India")
    type_text(driver, By.ID, "state", data["state"])
    type_text(driver, By.ID, "city", data["city"])
    type_text(driver, By.ID, "zipcode", data["zipcode"])
    type_text(driver, By.ID, "mobile_number", data["mobile"])
    click(driver, By.CSS_SELECTOR, 'button[data-qa="create-account"]')

    message = get_text(driver, By.CSS_SELECTOR, 'h2[data-qa="account-created"]')
    print(message)
    driver.quit()


main()
