
import re

import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def clear_str(value):
    value = value.replace('\xa0', '')
    try:
        return int(value)
    except:
        return value

def add_schema_to_url(value):
    value = 'https://www.combook.ru'+value
    try:
        return value
    except:
        return value


def convert_to_int(value):
        try:
            tmp = re.findall(r'(\d+)', value)
            tmp = ''.join(tmp)
            value = int(tmp)
            return value
        except ValueError:
            # Handle the exception
            return 'error casting!'

def get_number(value):

    value = re.findall(r'(\d+)', value)
    return ''.join(value)


class LeroimerlenItem(scrapy.Item):

    name = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_str))
    number = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(get_number))
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(convert_to_int))
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(add_schema_to_url))



