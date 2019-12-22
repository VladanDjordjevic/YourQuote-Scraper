# -*- coding: utf-8 -*-
import scrapy
import urllib
import json

class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['www.yourquote.in']
    header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    start_page = 1
    custom_settings = {'DOWNLOAD_TIMEOUT': 3}
    code = input("""
    Type Categories (CODE):
        1. Poetry(pot)   	   2. Inspiration(ins) 3. One-liner(olr)
        4. Politics(pts)       5. Life(lif)        6. Music(mus)
        7. Long-form(lon)      8. Horror(hor)      9. Love(lov)
        10. Miscellaneous(msc) 11. Meme(mem)       12. Humour(hmr)
        13. Philosophy(phy)    14. Letter(let)     15. Travel(trl)
        16. Shayari(shy)       17. Story(sto)      18. Diary(dia)
        19. Friendship(fds)    20. Film(flm)       21. Microtale(mtl)
        20. Erotica(ero)

    Enter code here : 
    """)
    def start_requests(self):
        yield scrapy.Request(
        url=f'https://www.yourquote.in/yourquote-web-cache/posts/explore/categories/{self.code}/posts/noauth?sort=top&page={self.start_page}&supportsWebP=true',
        method="GET",
        headers=self.header,
        callback=self.parse,
        errback=self.errback)

    def parse(self, response):
        data = json.loads(response.body)
        for key in data['posts']:
            yield {
              'quote':key["text"].replace('\n',' '),
              'user':key["user"]['slug'],
              'page': self.start_page
            }
        self.start_page += 1 
        yield scrapy.Request(
        url=f'https://www.yourquote.in/yourquote-web-cache/posts/explore/categories/lov/posts/noauth?sort=top&page={self.start_page}&supportsWebP=true',
        method="GET",
        headers=self.header,
        callback=self.parse,
        errback=self.errback)
    
    def errback(self, failure):
        self.logger.info('Handled by the errback: %s (%s exception)', failure.request.url, str(failure.value))
        return {'page': self.start_page,'url': failure.request.url}
