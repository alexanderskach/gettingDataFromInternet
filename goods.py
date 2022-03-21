# https://www.kinopoisk.ru/popular/films/?quick_filters=serials&tab=all

import requests
from bs4 import BeautifulSoup as BS
from pprint import pprint

url = 'https://rskrf.ru'

suffix = '/ratings/produkty-pitaniya/'

params = {'quick_filters': 'serials',
          'tab': 'all',
           'page': 2}

headers = {'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 '}

response = requests.get(url + suffix, params=params, headers=headers)
dom = BS(response.text, 'html.parser')

# with open('1.html', 'w') as f:
#     f.write(dom.text)

categories = dom.find_all('div', {'class':'category-item'})

category_list = []

for category in categories:
    categories_data = {}
    # name = product.find('p').text
    name = category.find('span', {'class': 'h5'}).text
    link = url + category.find('a').get('href')

    # try:
    #     rating = float(rating)
    # except:
    #     rating = None

    categories_data['name'] = name
    categories_data['link'] = link
    # serial_data['rating'] = rating

    category_list.append(categories_data)

pprint(category_list)


for i, product in enumerate(category_list):
    response = requests.get(category_list[i]['link'], params=params, headers=headers)
    dom = BS(response.text, 'html.parser')
    prod = dom.find('span', {'class': 'd-xl-none d-block'}).text

    pprint(prod)