#import csv
from datetime import datetime
import pandas as pd
import scrapy
from scrapy.exceptions import CloseSpider


class SearchSpider(scrapy.Spider):
    name = 'yinghui'
    start_urls = ['https://www.cnn.com',
                  'https://www.foxnews.com/',
                  'https://www.msnbc.com/',
                  'https://www.nbcnews.com/',
                  'https://news.yahoo.com/',
                  'https://www.economist.com/',
                  'https://www.bbc.com/',
                  'https://www.theguardian.com/us',
                  'https://www.huffpost.com/',
                  'https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en']
    count = 0
    max_links = 100
    df = pd.DataFrame(columns=['Title', 'Link'])
    start = datetime.now()

    def parse(self, response):
        if self.count >= self.max_links:
            raise CloseSpider('Max Links Exceeded')
        else:
            self.df.loc[len(self.df)] = [response.css("title::text").get().strip(),
                                         response.css("meta[property='og:url']::attr(content)").get().strip(),
                                         response.css("meta[property='og:description']::attr(content)").get().strip()]
            self.count += 1
            print(self.count)
            if self.count < self.max_links:
                temp = self.count
                for page in response.css('a'):
                    if temp >= self.max_links:
                        break
                    if page.css('a::attr(href)').get()[:8] == 'https://':
                        temp += 1
                        yield response.follow(page, self.parse)

    def close(self, reason):
        self.df.to_csv('data.csv', sep='~', index=False)
        print(datetime.now() - self.start)
