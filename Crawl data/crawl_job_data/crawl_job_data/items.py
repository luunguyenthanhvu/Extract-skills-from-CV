# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class CrawlJobDataItem(scrapy.Item):
    title = Field()
    required_skills = Field()
