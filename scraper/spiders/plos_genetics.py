from itertools import product

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from scraper.items import PaperItem

class PLOSGeneticsIssueSpider(BaseSpider):
    name = 'plos_genetics'
    allowed_domains = ['plosgenetics.org']

    base_url = 'http://www.plosgenetics.org'

    def __init__(self):
        self.start_urls = []

        # plos genetics started in July of 2005, only have 6 issues that year
        self.start_urls.extend(
                self.make_urls(volumes=[1], issues=range(1, 7)))
        self.start_urls.extend(
                self.make_urls(volumes=range(2, 9), issues=range(1, 13)))
        self.start_urls.extend(
                self.make_urls(volumes=[10], issues=range(1, 7)))

        super(PLOSGeneticsIssueSpider, self).__init__()

    def make_urls(self, volumes, issues):
        journal_url = self.base_url + '/article/browse/issue/info%3Adoi%2F10.1371%2Fissue.pgen.v{0}.i{1}'
        for volume, issue in product(volumes, issues):
            volume = '0' * (2 - len(str(volume))) + str(volume)
            issue = '0' * (2 - len(str(issue))) + str(issue)

            yield journal_url.format(volume, issue)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select('//div[@class="item cf"]/div[@class="header"]/h3/a/@href')

        papers = []
        for url in urls:
            paper = PaperItem()
            paper['href'] = self.base_url + url.extract().split(';jessionid')[0]
            papers.append(paper)
        return papers


