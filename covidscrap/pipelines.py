# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from api.models import state

class CovidscrapPipeline(object):
    
    def process_item(self, item, spider):
        a = state.objects.filter(name=item['name'])

        if(len(a)>0):
            print(item)
            p=a[0]
            inhos = int(item['confirmedIndians']) + int(item['confirmedInternationals']) - int(item['deaths']) - int(item['cured'])
            p.confirmedIndians =  item['confirmedIndians']
            p.confirmedInternationals =  item['confirmedInternationals']
            p.inHospital=inhos
            p.deaths =  item['deaths']
            p.cured =  item['cured']
            p.save()       
        else:
            item.save()
        
        return item