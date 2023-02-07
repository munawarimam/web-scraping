import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re


BASE_URL = 'https://shopee.co.id'

s=Service(r"D:\webdriver\chromedriver.exe")

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
                    # Or return res if you need the element found
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

def get_item_url(user_input):
    base_url = BASE_URL + '/search?keyword=' + user_input.replace(" ", "%20")
    list_url = []
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.get(base_url)
    scrolling_page(driver)
        
    try:
        WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.col-xs-2-4.shopee-search-item-result__item>a')))
    finally:
        items = driver.find_elements(By.CSS_SELECTOR, 'div.col-xs-2-4.shopee-search-item-result__item>a')
        for item in items:
            url = item.get_attribute('href')
            list_url.append(url)
        driver.quit()
        
    return list_url

def get_values(urls):
    list_data = []
    for url in urls[0:2]:
        print(url)
        driver = webdriver.Chrome(service=s)
        driver.get(url)
        try:
            WebDriverWait(driver, 30).until(AnyEc (
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div._44qnta')),
                EC.presence_of_element_located((By.CSS_SELECTOR, 'p.irIKAp')),
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.U9rGd1')) ))
        finally:
            product_name = driver.find_element(By.CSS_SELECTOR, 'div._44qnta').find_element(By.TAG_NAME, 'span').text
            price = driver.find_element(By.CSS_SELECTOR, 'div.pqTWkA').text
            desc_product = driver.find_elements(By.CSS_SELECTOR, 'div.U9rGd1')[1].text
            all_value = {'product': product_name, 'harga': price, 'deskripsi': desc_product}

            specs = driver.find_elements(By.CSS_SELECTOR, 'div.U9rGd1')[0].find_elements(By.CSS_SELECTOR, 'div.dR8kXc')
            for spec in specs:
                all_value.update({spec.find_element(By.TAG_NAME, 'label').text: spec.find_element(By.XPATH, "div|a").text})
            list_data.append(all_value)
            time.sleep(3)
        driver.quit()

    return list_data

def main(user_input):
    urls = get_item_url(user_input)
    all_values = get_values(urls)
    clean_values = [{key.strip('\n').lower().replace(" ", "_"): re.sub('[^a-zA-Z0-9 \n\.\,\-]', '', re.sub(' +', ' ', item.replace('\n', ' '))) for key, item in my_dict.items()} for my_dict in all_values]
    df = pd.DataFrame(clean_values)
    df.to_excel(r'C:\Users\USER\Desktop\shopee2.xlsx', index=False)