import time
from pprint import pprint

import pymongo
import requests
from bs4 import BeautifulSoup as BS

# 1. Развернуть у себя на компьютере/виртуальной
# машине/хостинге MongoDB и реализовать функцию, к
# оторая будет добавлять только новые вакансии/продукты в вашу базу.

def get_vacansy(vacansy):

    time.sleep(1)
    params = {'page': 1}

    response = requests.get(vacansy, params=params, headers=headers)

    dom = BS(response.text, 'html.parser')

    vac = dom.find('h1', {'class': 'bloko-header-1', 'data-qa': 'vacancy-title'})

    tmp_1 = dom.find('div', {'data-qa': 'vacancy-salary'}).find('span').text.split()

    min_selary = '',
    max_selary = '',
    currency = ''

    match(tmp_1):
         case('\u043e\u0442', x, y, '\u0434\u043e', f, g, h, k, l):
             min_selary = tmp_1[1]+tmp_1[2]
             max_selary = tmp_1[4] + tmp_1[5]
             currency = tmp_1[6]

         case('\u043e\u0442', x, y, '\u0434\u043e', f, g, h, k, l, m):
             min_selary = tmp_1[1] + tmp_1[2]
             max_selary = tmp_1[4] + tmp_1[5]
             currency = tmp_1[6]

         case('\u043e\u0442', x, y, z, b, c):
             min_selary = tmp_1[1] + tmp_1[2]
             currency = tmp_1[3]

         case(a, x, y):
             min_selary = tmp_1[0]

    data = {"url": vacansy,
            "vacansy_title": vac.text,
            "min_salary": str_to_int(min_selary),
            "max_salary": str_to_int(max_selary),
            "currency": currency
            }
    return data

def str_to_int(selary):
    try:
        selary_i = int(selary)
    except:
        selary_i = '\u041d\u0435 \u0443\u043a\u0430\u0437\u0430\u043d\u043e'
    return selary_i

def save(data):
    collection.insert_one(data)
    print(data)


### Run program ###

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client["hh"]
collection = db["vacancy"]

url = 'https://hh.ru'

suffix = '/vacancies/inzhener/'

params = {'page': 1}

headers = {'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}

response = requests.get(url + suffix, params=params, headers=headers)
dom = BS(response.text, 'html.parser')

vacans = dom.find_all('a', {'class':'bloko-link', 'data-qa':'vacancy-serp__vacancy-title'})

vacans_list = []
vacans_dict = []

for vacan in vacans:

    vacans_data = {}

    vacans_data['name'] = vacan.text
    vacans_data['link'] = vacan.get('href')
    vacans_list.append(vacans_data)

for vacansy in vacans_list:
    save(get_vacansy(vacansy['link']))

# 2. Написать функцию, которая производит поиск и
# выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).

def find_by_sellery(selery):
    for doc in collection.find({'$or': [{'min_salary': {'$gt':selery}}, {'max_salary': {'$gt': selery}}]}): #$lte
        pprint(doc)
    pprint('Количество документов: ')
    pprint(collection.count_documents({'$or': [{'min_salary': {'$gt':selery}}, {'max_salary': {'$gt': selery}}]}))

find_by_sellery(150000)












