import scrapy

from covidscrap.items import stateItem

class covidspider(scrapy.Spider):
    name= "gocovid"
    
    start_urls = [
        'https://www.mohfw.gov.in/'
    ]
    
    def parse(self,response):
        # print(response.xpath('//*[@id="state-data"]/div/div/div/div/table/tbody/tr'))
        print(111111111111111111111111)    
        for p in response.xpath('//*[@id="state-data"]/div/div/div/div/table/tbody/tr')[:-3]:
            print(p)
            item = stateItem()
            item['confirmedInternationals'] = 0
            item['name']=p.css('td::text')[1].get()
            item['confirmedIndians'] = p.css('td::text')[2].get()
            item['deaths'] = p.css('td::text')[4].get()
            item['cured'] = p.css('td::text')[3].get()
            print(item)
            yield item