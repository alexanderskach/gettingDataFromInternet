
import os
from urllib.parse import urlparse

import scrapy

from scrapy.pipelines.images import ImagesPipeline


class LeroimerlenPipeline:
    def process_item(self, item, spider):
        return item

class LeroiPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return item['number'] + '/' + os.path.basename(urlparse(request.url).path)
