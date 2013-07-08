# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class JournalIssueItem(Item):
    date = Field()
    articles = Field()

class PaperItem(Item):
    href = Field()

