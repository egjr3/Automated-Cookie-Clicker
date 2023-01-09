from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

timeout = time.time() + 5
five_min = time.time() + 60*5

chrome_driver_path = os.path.join('chromedriver_win32','chromedriver.exe')
driver = webdriver.Chrome(service=Service(chrome_driver_path))

driver.get('https://orteil.dashnet.org/cookieclicker/')
time.sleep(3)

# Select Language
driver.find_element(By.ID, 'langSelect-EN').click()
time.sleep(3)

cookie = driver.find_element(By.ID, 'bigCookie')

def check_upgrades():
    print('Checking Upgrades')
    products = [product.text for product in driver.find_elements(By.CSS_SELECTOR, '.product.unlocked.enabled .productName')]
    prices = [float(price.text.replace(',','')) for price in driver.find_elements(By.CSS_SELECTOR, '.product.unlocked.enabled .price')]

    upgrades = dict(zip(products, prices))
    print(upgrades)

    if upgrades:
        # get product with higher price
        product_names = list(upgrades.keys())
        product_prices = list(upgrades.values())
        higher_price = max(product_prices)
        index_higher_upgrade = product_prices.index(higher_price)
        higher_price_product = product_names[index_higher_upgrade]

        product_ID = f'product{product_names.index(higher_price_product)}'
        driver.find_element(By.CSS_SELECTOR, f'.product#{product_ID}').click()
        print(f'Purchased product: {higher_price_product}')

while True:
    cookie.click()
    if time.time() > timeout:
        check_upgrades()
        timeout = time.time() + 5

    if time.time() > five_min:
        cookies_per_sec = driver.find_element(By.ID, 'cookiesPerSecond').text
        print(cookies_per_sec)
        break