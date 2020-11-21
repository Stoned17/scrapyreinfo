import scrapy

from scrapy.crawler import CrawlerProcess

import re


def printf(d = ''):
    print('\n')
    print('*' * 20)
    print('*' * 20)
    print(d)
    print('*' * 20)
    print('*' * 20)
    print('\n')

def clean(cadena):
    return  re.sub('[\\r\\n]','', cadena).strip()

class ReinfoSpider(scrapy.Spider):
    name = 'reinfo'
    #allowed_domains = ['pad.minem.gob.pe']
    start_urls = ['http://pad.minem.gob.pe/REINFO_WEB/Index.aspx']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        #'CLOSESPIDER_PAGECOUNT': 5,
        'DOWNLOAD_DELAY': 1.5,
        #'LOG_ENABLED': False,
    }

    def parse(self, response):
        #printf(response.url)
        #th1 = response.xpath('//th[@scope="col"]').getall()
        #theaders = response.xpath('//tr [@class="gvHeader"][3]//label/text()').getall()
        rows = response.xpath('//table[@class="gvRow"]/tr[position()>3]')
        
        
        #yield {'hola': 'hola'}
        for row in rows[:2]:
            id_minero = row.xpath('./td[2]/span/text()').get()
            ruc = row.xpath('./td[3]/span/text()').get()
            min_inf = row.xpath('./td[4]/span/text()').get()
            cod_uni = row.xpath('./td[5]/span/text()').get()
            nombre = row.xpath('./td[6]/span/text()').get()
            dep = row.xpath('./td[7]/span/text()').get()
            prov = row.xpath('./td[8]/span/text()').get()
            dist = row.xpath('./td[9]/span/text()').get()
            
            
            data = {
                'ID': id_minero,
                'RUC': ruc,
                'MINERO INFORMAL': min_inf,
                'CÓDIGO ÚNICO': cod_uni,
                'NOMBRE': nombre,
                'DEPARTMENTO': dep,
                'PROVINCIA': prov,
                'DISTRITO': dist,
                
            }
            yield data
            
            import json
            data = json.dumps(data, indent=4)
            
            printf(data)
        #printf(rows)
        #printf(ruc)
        
        '''for i in theaders:
            printf(clean(i))
        print('Nuevo')
        printf(theaders)
        printf(th1)'''




'''if __name__ == '__main__':
    crawler = CrawlerProcess()
    crawler.crawl(ReinfoSpider)
    crawler.start()'''