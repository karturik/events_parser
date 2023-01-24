import requests
from bs4 import BeautifulSoup
import os
import urllib.request
from tqdm import tqdm

soup = BeautifulSoup(r = requests.get('https://www.azcentral.com/things-to-do/events/').content, features='html.parser')

post_links = soup.find_all('div', class_='c-card relative block border-gray-200 overflow-hidden bg-white subtle-shadow')

links = set()

for link in post_links:
    a = link.find('a')
    links.add('https://discoverevvnt.com' + a.get('href'))

print(len(links))

for link in tqdm(links):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, features='html.parser')
    try:
        src = soup.find('div', class_='aspect-video relative image-placeholder').find('span').find('img').get('src')
        title = soup.find('h1', class_='font-bold text-3xl md:text-xl lg:text-3xl').text.replace('"', '').replace("'", "").replace(":", "").replace("\\", "").replace("/", "")
        if not os.path.exists(f'azcentral.com/{title}'):
            os.mkdir(f'azcentral.com/{title}')
        if not os.path.exists(f'azcentral.com/{title}/media'):
            os.mkdir(f'azcentral.com/{title}/media')
        text2 = soup.find('div', class_='mt-6 mb-2 whitespace-pre-wrap text-gray-700').text
        if len(text2) > 7:
            text2 = text2
        else:
            text2 = title
        with open(f'azcentral.com/{title}/description.txt', 'w', encoding='utf-8') as file:
            file.write(text2)
            file.close()
        urllib.request.urlretrieve(src, f'azcentral.com/{title}/media/image.png')
    except Exception as e:
        print(e)
