import re
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = 'https://www.tokopedia.com'

class AnyEc:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """
    def __init__(self, *args):
        self.ecs = args
    def __call__(self, driver):
        for fn in self.ecs:
            try:
                res = fn(driver)
                if res:
                    return True
            except:
                pass

def scrolling_page(driver):
    SCROLL_PAUSE_TIME = 5

    # Get scroll height
    total_height = driver.execute_script("return document.body.scrollHeight")
    browser_window_height = driver.get_window_size(windowHandle='current')['height']
    current_position = driver.execute_script('return window.pageYOffset')

    while total_height - current_position > browser_window_height:
        driver.execute_script(f"window.scrollTo({current_position}, {browser_window_height + current_position});")
        time.sleep(SCROLL_PAUSE_TIME)
        current_position = driver.execute_script('return window.pageYOffset')

def get_item_url(user_input, driver):
    base_url = BASE_URL + '/search?condition=1&navsource=&srp_page_id=&srp_page_title=&st=product&q=' + user_input.replace(" ", "%20")
    list_url = []
    driver.get(base_url)
    scrolling_page(driver)

    try:
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-974ipl>a')))
    finally:
        items = driver.find_elements(By.CSS_SELECTOR, 'div.css-974ipl>a')
        for item in items:
            url = item.get_attribute('href')
            list_url.append(url)

    return list_url

def get_values(urls, driver):
    list_data = []
    for url in urls:
        driver.get(url)
        try:
            WebDriverWait(driver, 30).until(AnyEc (
                EC.presence_of_element_located((By.CLASS_NAME,'css-1os9jjn')),
                EC.presence_of_element_located((By.CLASS_NAME, 'css-1k1relq')),
                EC.presence_of_element_located((By.CLASS_NAME, 'eytdjj01'))))
        finally:
            product_name = driver.find_element(By.CLASS_NAME, 'css-1os9jjn').text
            price = driver.find_element(By.CSS_SELECTOR, 'div.price').text
            desc_product = driver.find_element(By.CLASS_NAME, 'eytdjj01').text
            all_value = {'product': product_name, 'harga': price, 'deskripsi': desc_product}
            list_data.append(all_value)

    return list_data

def main(user_input, driver):
    urls = get_item_url(user_input, driver)
    new_urls = [ x for x in urls if "ta.tokopedia" not in x ]
    all_values = get_values(new_urls, driver)
    clean_values = [{key.strip('\n').lower().replace(" ", "_"): re.sub('[^a-zA-Z0-9 \n\.\,\-]', ' ', re.sub(' +', ' ', item.replace('\n', ' '))) for key, item in my_dict.items()} for my_dict in all_values]
    df = pd.DataFrame(clean_values)
    return df