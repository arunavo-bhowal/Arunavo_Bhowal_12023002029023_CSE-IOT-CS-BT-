import os
import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
DATA_FILE = os.path.join(BASE_DIR, "testdata", "testdata.json")


def read_test_data():
    with open(DATA_FILE) as f:
        data = json.load(f)
    return data


def get_driver():
    options = webdriver.ChromeOptions()
    options.page_load_strategy = "eager"   # dont wait for ads to finish loading
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument(
        "--host-resolver-rules="
        "MAP *.doubleclick.net 127.0.0.1, "
        "MAP *.googlesyndication.com 127.0.0.1, "
        "MAP *.googleadservices.com 127.0.0.1, "
        "MAP *.adtrafficquality.google 127.0.0.1"
    )
    driver = webdriver.Chrome(options=options)
    return driver


def remove_ads(driver):
    script = """
    document.querySelectorAll('iframe, ins.adsbygoogle, [id^="aswift"], [id^="google_ads"], #ad_position_box, .fc-consent-root').forEach(function(e){ e.remove(); });
    document.body.style.overflow = 'auto';
    if (window.location.hash.indexOf('google_vignette') !== -1) {
        history.replaceState(null, '', window.location.pathname + window.location.search);
    }
    """
    try:
        driver.execute_script(script)
    except Exception:
        pass


def handle_alert(driver):
    try:
        alert = driver.switch_to.alert
        print("Alert found:", alert.text)
        alert.accept()
    except NoAlertPresentException:
        pass


def open_page(driver, url):
    driver.get(url)
    time.sleep(1)
    handle_alert(driver)
    remove_ads(driver)


def click(driver, by, value):
    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((by, value)))
    remove_ads(driver)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].click();", element)   # js click so ads cant block it
    time.sleep(1)
    handle_alert(driver)
    remove_ads(driver)


def type_text(driver, by, value, text):
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((by, value)))
    element.clear()
    element.send_keys(text)


def get_text(driver, by, value):
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((by, value)))
    return element.text


def take_screenshot(driver, name):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    remove_ads(driver)
    path = os.path.join(SCREENSHOT_DIR, name + ".png")
    driver.save_screenshot(path)
    print("Screenshot saved:", path)


def empty_cart(driver, base_url):
    open_page(driver, base_url + "/view_cart")
    for i in range(10):
        delete_buttons = driver.find_elements(By.CLASS_NAME, "cart_quantity_delete")
        if len(delete_buttons) == 0:
            break
        driver.execute_script("arguments[0].click();", delete_buttons[0])
        time.sleep(2)
        remove_ads(driver)
