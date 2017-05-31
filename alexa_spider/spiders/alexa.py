# -*- coding: utf-8 -*-
import csv

from scrapy import Spider
from scrapy.http import Request
import pkgutil


class AlexaSpider(Spider):
    name = 'alexa'
    allowed_domains = ['alexa.com']

    def start_requests(self):        
        input_file = csv.DictReader(open(pkgutil.get_data("alexa_spider", "/resources/50k_domains.csv")))
        for row in input_file:
            domain = row['site']
            url = 'http://www.alexa.com/siteinfo/' + domain
            yield Request(url, meta={'domain': domain})

    def parse(self, response):
        country = response.xpath(
            '//h4[text()="Rank in "]/a/text()').extract_first()

        rank = response.xpath(
            '//h4[text()="Rank in "]/following-sibling::div/strong/text()').extract_first()
        try:
            rank = rank.strip()
        except:
            rank = ''

        search_visit = response.xpath(
            '//h4[text()="Search Visits"]'
            '/following-sibling::div/strong/text()').extract_first()
        try:
            search_visit = search_visit.strip()
        except:
            search_visit = ''

        if int(search_visit.split('.')[0]) > 20:
            yield {
                    'Country of Rank': country,
                    'Rank Number': rank,
                    'Search Visits': search_visit,
                    'Domain': response.meta['domain']
                }
