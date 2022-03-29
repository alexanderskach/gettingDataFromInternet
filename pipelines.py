# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class HhruPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.scrappy

    def process_item(self, item, spider):

        if spider.name == 'Hhru':
            print('------------->hh:')
            strn = " ".join(item['salary'])
            out = " ".join(strn.split())

            print('out: ',out.split())

            item['min'], item['max'], item['cur'] = self.process_salary(out.split());

            print('-----------cur: ', item['name'])
            print('-----------cur: ', item['link'])
            print('-----------min_salary: ', item['min'])
            print('-----------max_salary: ', item['max'])
            print('-----------cur: ', item['cur'])

            self.save(spider, item)

        if spider.name == 'superJ':
            print('------------->superjob:')

            strn = " ".join(item['salary'])
            out = " ".join(strn.split())

            print('out: ', out.split())

            item['min'], item['max'], item['cur'] = self.process_salary_j(out.split());

            print('-----------cur: ', item['name'])
            print('-----------cur: ', item['link'])
            print('-----------min_salary: ', item['min'])
            print('-----------max_salary: ', item['max'])
            print('-----------cur: ', item['cur'])

            self.save(spider, item)

            # collection = self.mongobase[spider.name]
            # collection.insert_one(item)

            return item

    def process_salary(self, salary):

        match (salary):

            case ('\u043e\u0442', x, y, '\u0434\u043e', f, g, h, k, l):
                print('min_salary:',salary[1] + salary[2])
                min_selary = salary[1] + salary[2]
                print('max_salary:', salary[4] + salary[5])
                max_selary = salary[4] + salary[5]
                print('currency:', salary[6])
                currency = salary[6]
                salary_list = [min_selary, max_selary, currency]

            case ('\u043e\u0442', x, y, '\u0434\u043e', f, g, h, k, l, m):
                min_selary = salary[1] + salary[2]
                max_selary = salary[4] + salary[5]
                currency = salary[6]
                salary_list = [min_selary, max_selary, currency]

            case ('\u043e\u0442', x, y, z, b, c):
                min_selary = salary[1] + salary[2]
                currency = salary[3]
                salary_list = [min_selary, '', currency]

            case (a, x, y):
                min_selary = salary[0]
                salary_list = [min_selary, '', '']

        return salary_list

    def process_salary_j(self, salary):
        match (salary):
            case ('\u043e\u0442', x, y, '\u0434\u043e', f, g, h, k, l):
                print('min_salary:',salary[1] + salary[2])
                min_selary = salary[1] + salary[2]
                print('max_salary:', salary[4] + salary[5])
                max_selary = salary[4] + salary[5]
                print('currency:', salary[6])
                currency = salary[6]
                salary_list = [min_selary, max_selary, currency]

            # ['до', '120', '000', 'руб.']
            case ('\u0434\u043e', f, g, h, k, l):
                print('max_salary:', salary[1] + salary[2])
                max_selary = salary[1] + salary[2]
                print('currency:', salary[3])
                currency = salary[3]
                salary_list = ['-', max_selary, currency]

            # По договоренности
            case ('\u041f\u043e \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0435\u043d\u043d\u043e\u0441\u0442\u0438'):
                min_selary = salary[0]
                salary_list = [min_selary, 0, '-']

            # ['от', '120', '000', 'руб.']
            case ('\u043e\u0442', h, k, l):
                print('min_salary:', salary[1] + salary[2])
                min_selary = salary[1] + salary[2]
                print('currency:', salary[3])
                currency = salary[3]
                salary_list = [min_selary, '', currency]

            # ['70', '000', '90', '000', 'руб.']
            case (m , h, k, l, f):
                print('min_salary:', salary[0] + salary[1])
                min_selary = salary[0] + salary[1]
                print('max_salary:', salary[0] + salary[1])
                max_selary = salary[2] + salary[3]
                print('currency:', salary[4])
                currency = salary[4]
                salary_list = [min_selary, max_selary, currency]

        return salary_list

    def save(self, spider, item):
        collection = self.mongobase[spider.name]
        collection.insert_one(ItemAdapter(item).asdict())


