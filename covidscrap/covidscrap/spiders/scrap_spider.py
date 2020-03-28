import scrapy
from covidscrap.items import stateItem

class covidspider(scrapy.Spider):
    name= "gocovid"

    start_urls = [
        'https://www.mohfw.gov.in/'
    ]

    def parse(self,response):
        for p in response.xpath('//*[@id="cases"]/div/div/table/tbody/tr')[:-2]:
            item = stateItem()
            
            item['name'] = p.css('td::text')[1].get()
            item['confirmedIndians'] = p.css('td::text')[2].get()
            item['confirmedInternationals'] = p.css('td::text')[3].get()
            item['deaths'] = p.css('td::text')[5].get()
            item['cured'] = p.css('td::text')[4].get()
            yield item