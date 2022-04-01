from datetime import date
import requests
from lxml import html
import pymongo


client = pymongo.MongoClient('127.0.0.1', 27017)
db = client["articles"]
collection = db["news"]

header = {'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
url = 'https://lenta.ru'

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

def save(data):
    collection.insert_one(data)
    print(data)

cards = dom.xpath("//div[@class='card-mini__text']")


news_data = list()

for card in cards:

    article = {}

    # Если новость новая - выдает только время. Добавляем сегодняшнюю дату ко времени
    if (len(''.join(card.xpath(".//div[@class]/time[@class]/text()"))) < 6):

        article['time'] = str(date.today())+''.join(card.xpath(".//div[@class]/time[@class]/text()"))
    else:
        article['time'] = ''.join(card.xpath(".//div[@class]/time[@class]/text()"))

    article['title'] = ''.join(card.xpath(".//span[@class]/text()"))
    article['link'] = url + ''.join(card.xpath(".//parent::a/@href"))
    article['url'] = url

    print(article)
    news_data.append(article)

for data in news_data:
    print(data)
    save(data)
