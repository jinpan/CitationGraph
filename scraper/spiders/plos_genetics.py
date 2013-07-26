from itertools import product
from json import loads
from os import path
from re import match

from django.core.management import setup_environ
from CitationGraph import settings
setup_environ(settings)
from scraper.models import PaperQueue
from website.models import Journal

from bs4 import BeautifulSoup
from scrapy.spider import BaseSpider


class PLOSGeneticsIssueSpider(BaseSpider):
    name = 'PLOS Genetics'
    allowed_domains = ['plosgenetics.org']

    journal = Journal.objects.get(name=name)
    base_url = journal.url

    def __init__(self):
        self.start_urls = []

        # plos genetics started in July of 2005, only have 6 issues that year
        self.start_urls.extend(
                self.make_urls(volumes=[1], issues=range(1, 7)))
        self.start_urls.extend(
                self.make_urls(volumes=range(2, 8), issues=range(1, 13)))
        self.start_urls.extend(
                self.make_urls(volumes=[9], issues=range(1, 7)))

        super(PLOSGeneticsIssueSpider, self).__init__()

    def make_urls(self, volumes, issues):
        journal_url = self.base_url + '/article/browse/issue/info%3Adoi%2F10.1371%2Fissue.pgen.v{0}.i{1}'
        for volume, issue in product(volumes, issues):
            volume = '%02d' % volume  # pads with zeros
            issue = '%02d'% issue

            yield journal_url.format(volume, issue)

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        urls = map(lambda x: x.find('a').get('href'), soup.find_all('h3'))

        for url in urls:
            paper = PaperQueue(URL=self.base_url+url, journal=self.journal)
            paper.save()


class PLOSGeneticsArticleSpider(BaseSpider):

    name = 'plos_genetics'
    allowed_domains = ['plos_genetics.org']

    base_url = 'http://www.plosgenetics.org'

    def __init__(self):
        self.start_urls = []
        file_name = path.join(config.root_directory, 'mined', 'plos_genetics.json')
        data = loads(open(file_name).read())

        for item in data:
            self.start_urls.append(self.base_url + data['href'])

        super(PLOSGeneticsArticleSpider, self).__init__()

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        title = hxs.select('//h1/text()').extract()
        publication_date = hxs.select('//div[@class="articleinfo"]//p')[2].extract()
        # citations = hxs.select(


