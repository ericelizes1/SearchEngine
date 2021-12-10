import pandas as pd
import scrapy
from scrapy.exceptions import CloseSpider


class SearchSpider(scrapy.Spider):
    name = 'yinghui'
    # Start the spider with news website urls to assure a large
    # breadth of links will be obtained.
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
    
    # If a page has more than 100 links, stop at 100.
    max_links = 100
    df = pd.DataFrame(columns=['Title', 'Link', 'Desc'])

    
    # Function to scrape all links.
    def parse(self, response):
        # If the breadth limit for a webpage has been linked, stop traveling down that path.
        if self.count >= self.max_links:
            raise CloseSpider('Max Links Exceeded')
        else:
            # Get the title, URL, and description from the website and append it to the dataframe.
            self.df.loc[len(self.df)] = [response.css("title::text").get().strip(),
                                         response.css("meta[property='og:url']::attr(content)").get().strip(),
                                         response.css("meta[property='og:description']::attr(content)").get().strip()]
            self.count += 1
            print(self.count)
            
            # If the breadth limit still has not been reached, recur on each link found in the website.
            if self.count < self.max_links:
                temp = self.count
                for page in response.css('a'):
                    if temp >= self.max_links:
                        break
                    if page.css('a::attr(href)').get()[:8] == 'https://':
                        temp += 1
                        # Recur on each link as long as it does not exceed the maximum links number.
                        yield response.follow(page, self.parse)

                        
    def close(self, reason):
        self.df.to_csv('data.csv', sep='~', index=False)
        
