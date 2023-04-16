from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

chrome_driver_path = os.path.join('chromedriver_win32', 'chromedriver.exe')
driver = webdriver.Chrome(service=Service(chrome_driver_path))


def coockieClicker():

    driver.get('https://orteil.dashnet.org/cookieclicker/')
    time.sleep(3)

    timeCheckUpdate = time.time() + 5
    timeEndGame = time.time() + 60*5

    driver.find_element(
        By.CSS_SELECTOR, '.fc-button.fc-cta-consent.fc-primary-button').click()
    time.sleep(3)

    # Select Language
    driver.find_element(By.ID, 'langSelect-EN').click()
    time.sleep(3)

    cookie = driver.find_element(By.ID, 'bigCookie')

    def check_upgrades():
        print('Checking Upgrades')
        products = [product.text for product in driver.find_elements(
            By.CSS_SELECTOR, '.product.unlocked.enabled .productName')]
        prices = [float(price.text.replace(',', '')) for price in driver.find_elements(
            By.CSS_SELECTOR, '.product.unlocked.enabled .price')]

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
            driver.find_element(
                By.CSS_SELECTOR, f'.product#{product_ID}').click()
            print(f'Purchased product: {higher_price_product}')

    while True:
        cookie.click()
        if time.time() > timeCheckUpdate:
            check_upgrades()
            timeCheckUpdate = time.time() + 5

        if time.time() > timeEndGame:
            cookies_per_sec = driver.find_element(
                By.ID, 'cookiesPerSecond').text
            print("Program finished")
            print('Working at: ', cookies_per_sec, ' cookies per second')
            driver.quit()


def cookieClickerClassic():
    driver.get('https://orteil.dashnet.org/experiments/cookie/')
    time.sleep(3)

    timeCheckUpdate = time.time() + 5
    timeEndGame = time.time() + 60*5

    cookie = driver.find_element(By.ID, 'cookie')

    def check_upgrades():
        print('Checking Upgrades')
        products = [product.text.split("\n")[0] for product in driver.find_elements(
            By.CSS_SELECTOR, '#store div:not(.grayed)')]

        toPurchaseProducts = []

        for each in products:
            if (not each.isnumeric()):
                toPurchaseProducts.append(each)

        upgrades = dict(product.split(" - ") for product in toPurchaseProducts)
        print(upgrades)

        if upgrades:
            # get product with higher price
            product_names = list(upgrades.keys())
            product_prices = [int(item.replace(',', ''))
                              for item in upgrades.values()]
            higher_price = max(product_prices)

            index_higher_price = product_prices.index(higher_price)
            higher_price_product = product_names[index_higher_price]

            product_ID = f'buy{higher_price_product}'
            driver.find_element(
                By.ID, product_ID).click()
            print(f'Purchased product: {higher_price_product}')

    while True:
        cookie.click()
        if time.time() > timeCheckUpdate:
            check_upgrades()
            timeCheckUpdate = time.time() + 5

        if time.time() > timeEndGame:
            cookies_per_sec = driver.find_element(
                By.ID, 'cps').text
            print("Program finished")
            print('Working at: ', cookies_per_sec, ' cookies per second')
            driver.quit()

if __name__ == '__main__':
    try:
        print('Running Cookie Clikcer.')
        coockieClicker()
    except:
        print('There was an Error running Cockie Clicker.')
        print('Now running Cookie Clikcer classic.')
        cookieClickerClassic()