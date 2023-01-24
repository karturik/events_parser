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

start_url = 'https://allexciting.com/festivals/'
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
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "av-inner-masonry.main_color")))
links_to_posts = driver.find_element(By.CLASS_NAME, 'av-masonry-container.isotope').find_elements(By.TAG_NAME, 'a')

links = set()

for link_to_post in links_to_posts:
    link = link_to_post.get_attribute('href')
    links.add(link)

print(links)
print(len(links))

for post_link in links:
    try:
        driver.get(post_link)
        title = driver.find_element(By.CLASS_NAME, 'av-special-heading-tag').text.replace(':', '')
        print(title)
        print(post_link)
        if not os.path.exists(f'allexciting.com/{title}'):
            os.mkdir(f'allexciting.com/{title}')
        if not os.path.exists(f'allexciting.com/{title}/media'):
            os.mkdir(f'allexciting.com/{title}/media')
        text = ''
        for i in range(1, 100):
            try:
                text += '\n' + driver.find_element(By.XPATH, f'//*[@id="after_section_1"]/div/div/div/div/div[1]/section[{i}]/div').text
            except Exception as e:
                break
        with open(f'allexciting.com/{title}/description.txt', 'w', encoding='utf-8') as file:
            file.write(text)
            file.close()
        try:
            img = driver.find_elements(By.CLASS_NAME, 'entry-content-wrapper.clearfix')[1].find_element(By.TAG_NAME, 'img').get_attribute('src')
            urllib.request.urlretrieve(img, f'allexciting.com/{title}/media/image.png')
        except Exception as e:
            print(e)
            pass
    except Exception as e:
        print(e)
        pass
