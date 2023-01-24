from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import urllib.request

start_url = 'https://www.nycgo.com/things-to-do/events-in-nyc/'
options = Options()
# options.add_argument("--headless")
# prefs = {'profile.default_content_setting_values': {'images': 2}}
# options.add_experimental_option('prefs', prefs)
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--blink-settings=imagesEnabled=false')
# options.add_argument('--no-sandbox')
options.add_argument("--window-size=1024,720")
driver = webdriver.Chrome(options=options)

driver.get(start_url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-simple-image-container")))
links_to_posts = driver.find_elements(By.CLASS_NAME, 'card-simple-image-container')

links = set()

for link_to_post in links_to_posts:
    link = link_to_post.find_element(By.TAG_NAME, 'a').get_attribute('href')
    links.add(link)

print(links)

for post_link in links:
    try:
        images_links = []
        driver.get(post_link)
        title = driver.find_element(By.CLASS_NAME, 'section-header').text.replace(':', '')
        print(title)
        print(post_link)
        if not os.path.exists(f'nycgo.com/{title}'):
            os.mkdir(f'nycgo.com/{title}')
        if not os.path.exists(f'nycgo.com/{title}/images'):
            os.mkdir(f'nycgo.com/{title}/images')
        text = driver.find_element(By.TAG_NAME, 'p').text
        with open(f'nycgo.com/{title}/description.txt', 'w', encoding='utf-8') as file:
            file.write(text)
            file.close()
        src = driver.find_element(By.CLASS_NAME, 'bg-masthead').find_element(By.TAG_NAME, 'img').get_attribute('src')
        urllib.request.urlretrieve(src, f'nycgo.com/{title}/images/image.png')
    except:
        pass