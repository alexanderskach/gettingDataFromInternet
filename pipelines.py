import csv
import os
from urllib.parse import urlparse

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from pymongo import MongoClient

class OpendataPipeline():
    def process_item(self, item, spider):
        print('ITEM_URL_1: ', item['urldata'])
        return item

class OpendataFilePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        print('ITEM_URL_2: ', item['urldata'])
        adapter = ItemAdapter(item)
        for file_url in adapter['urldata']:
            print('LINK: ----->>>',file_url)
            yield scrapy.Request(file_url)

    def item_completed(self, results, item, info):
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return os.path.basename(urlparse(request.url).path)

class CSVPipeline():

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.scrappy

        CUR_DIR = os.path.dirname(os.path.realpath(__file__))
        FILES_STORE = os.path.join(CUR_DIR, '..', 'data_file')
        self.file = FILES_STORE+'/1.csv'

        # with open(self.file, 'r', encoding='UTF-8') as csv_file:
        #     self.tmp_data = csv.DictReader(csv_file).fieldnames
        #     print('HEADERS:---->>>', self.tmp_data)
        self.csv_file = open(self.file, 'r', encoding='UTF-8')
        # self.tmp_data = csv.DictReader(self.csv_file).fieldnames

    def __del__(self):
            self.csv_file.close()

    def get_data(self, collection):
        # Quaery to get All data
        print('Quaery to get All data:')
        item_details = collection.find({})
        for item in item_details:
            print(item)

        # Quaery to get quantity of sick and place it happened for certain date
        print('Quaery to get quantity of sick and place it happened for certain date:')
        # item_details = collection.find({}, {"_id": 0, "Место": 1, "6 мая 2020": 1})
        item_details = collection.find({}, {"6 мая 2020": 1})
        for item in item_details:
            print(item)


    def save(self, spider, row):
        collection = self.mongobase[spider.name]
        collection.insert_one(row)

        self.get_data(collection)

    def process_item(self, item, spider):
        reader = csv.DictReader(self.csv_file, delimiter = ";")
        for row in reader:
            print(row)
            self.save(spider, row)






