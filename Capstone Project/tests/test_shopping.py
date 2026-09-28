from selenium.webdriver.common.by import By
from utils.helpers import (
    read_test_data, open_page, click, type_text, get_text,
    take_screenshot, handle_alert, empty_cart,
)

data = read_test_data()
base_url = data["base_url"]
product = {} 


def test_1_login(driver):
    open_page(driver, base_url + "/login")
    take_screenshot(driver, "01_login_page")

    type_text(driver, By.CSS_SELECTOR, 'input[data-qa="login-email"]', data["email"])
    type_text(driver, By.CSS_SELECTOR, 'input[data-qa="login-password"]', data["password"])
    click(driver, By.CSS_SELECTOR, 'button[data-qa="login-button"]')
    handle_alert(driver)
    take_screenshot(driver, "02_after_login")

    text = get_text(driver, By.XPATH, "//a[contains(., 'Logged in as')]")
    assert data["name"] in text


def test_2_search_product(driver):
    open_page(driver, base_url + "/products")
    type_text(driver, By.ID, "search_product", data["search_word"])
    click(driver, By.ID, "submit_search")

    heading = get_text(driver, By.CSS_SELECTOR, ".features_items .title")
    assert "SEARCHED PRODUCTS" in heading.upper()

    product["name"] = get_text(driver, By.CSS_SELECTOR, ".features_items .productinfo p")
    link = driver.find_element(By.CSS_SELECTOR, '.features_items a[href^="/product_details"]')
    product["link"] = link.get_attribute("href")
    take_screenshot(driver, "03_search_result")

    assert data["search_word"].lower() in product["name"].lower()


def test_3_add_to_cart(driver):
    empty_cart(driver, base_url)
    open_page(driver, product["link"])
    take_screenshot(driver, "04_product_page")

    click(driver, By.CSS_SELECTOR, "button.cart")
    popup = get_text(driver, By.ID, "cartModal")
    take_screenshot(driver, "05_added_popup")

    assert "added" in popup.lower()


def test_4_update_quantity(driver):
    empty_cart(driver, base_url)
    open_page(driver, product["link"])
    type_text(driver, By.ID, "quantity", str(data["quantity"]))
    take_screenshot(driver, "06_quantity_changed")

    click(driver, By.CSS_SELECTOR, "button.cart")
    popup = get_text(driver, By.ID, "cartModal")
    assert "added" in popup.lower()


def test_5_verify_cart(driver):
    open_page(driver, base_url + "/view_cart")

    cart_name = get_text(driver, By.CSS_SELECTOR, ".cart_description h4 a")
    cart_price = get_text(driver, By.CSS_SELECTOR, ".cart_price p")
    cart_quantity = get_text(driver, By.CSS_SELECTOR, ".cart_quantity button")
    cart_total = get_text(driver, By.CSS_SELECTOR, ".cart_total_price")
    take_screenshot(driver, "07_cart_page")

    print("Cart:", cart_name, cart_price, cart_quantity, cart_total)

    price = int(cart_price.replace("Rs.", "").strip())
    expected_total = price * data["quantity"]

    assert cart_name == product["name"]
    assert cart_quantity == str(data["quantity"])
    assert cart_total == "Rs. " + str(expected_total)
