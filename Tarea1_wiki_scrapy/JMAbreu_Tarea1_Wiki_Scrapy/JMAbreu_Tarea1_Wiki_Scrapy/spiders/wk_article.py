# -*- coding: utf-8 -*-
import scrapy
from JMAbreu_Tarea1_Wiki_Scrapy.items import articles, article

class WkArticleSpider(scrapy.Spider):
    name = 'wk_article'
    #allowed_domains = ['en.wikipedia.org']
    #start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']
    #allowed_domains = ['prensalibre.com']
    #start_urls = ['https://prensalibre.com/']
    allowed_domains = ['catalog.data.gov']
    start_urls = ['https://catalog.data.gov/dataset']

    custom_settings = {
        'FEED_FORMAT' : 'json',
        'FEED_URI' : 'file:C://Users//jabreu//UVG//Data Scients//Data Adquisitions//Tarea1_wiki_scrapy//JMAbreu_Tarea1_Wiki_Scrapy//featured_article-%(time)s.json'
    }

    def parse(self, response):
        host = self.allowed_domains[0]
        cant = 1
        #for link in response.css(".story-title > a"):
        for link in response.css(".dataset-heading > a"):
            link = f"{link.attrib.get('href')}"
            title = link
            yield response.follow(link,callback=self.parse_detail, meta={'link' : link,'title':title})
            if cant == 25:
                break
            cant = cant+1

    def parse_detail(self,response):
        items = articles()
        item = article()

        items["link"] = response.meta["link"]
        item["title"] = response.meta["title"]
        item["paragraph"] = list()

        #for text in response.css(".sart-content > p::text").extract():
        for text in response.css(".notes > p").extract():
            item["paragraph"].append(text)
        
        item["paragraph"] = item["paragraph"][0]
        items["body"] = item
        return items