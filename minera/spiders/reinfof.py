import scrapy
from scrapy import FormRequest
 
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os


load_dotenv(find_dotenv())

def printf(d = ''):
    print('\n')
    print('*' * 20)
    print('*' * 20)
    print(d)
    print('*' * 20)
    print('*' * 20)
    print('\n')

test_envar = os.getenv('testito')

printf(test_envar)

class ExampleSpider(scrapy.Spider):
    name = 'reinfof'
 
    start_urls = ['http://pad.minem.gob.pe/REINFO_WEB/Index.aspx']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        #'CLOSESPIDER_PAGECOUNT': 5,
        'DOWNLOAD_DELAY': 1.5,
        #'LOG_ENABLED': False,
        'FEEDS': {
            'reinfo.json': {
            'format': 'json',
            'encoding': 'utf8',
            'indent': 4,
            },
        },
    }
    
    qty_items = int(os.getenv('QTY_ITEMS'))
    counter = 1
    initial_page = int(os.getenv('INITIAL_PAGE')) - 1
    
 
    def parse(self, response):
        view_state = response.xpath(
            "//input[@name='__VIEWSTATE']/@value").get()
        generator = response.xpath(
            "//input[@name='__VIEWSTATEGENERATOR']/@value").get()
 
        yield FormRequest.from_response(
            response,
            formdata={
                'ToolkitScriptManager1_HiddenField': '',
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': generator,
                '__VIEWSTATEENCRYPTED': '',
                'txtpagina': str(self.initial_page),
                'txttotal': '3555',
                'txtruc': '',
                'txtdeclarante': '',
                'ddltipersona': '',
                'txtidunidad': '',
                'txtnomderecho': '',
                'ddldepartamento': '99',
                'ddlordenado': '1',
                'ddlforma': 'ASC',
                'ImgBtnSiguiente.x': '3',
                'ImgBtnSiguiente.y': '16'
            },
 
            meta={
                'current_page': self.initial_page,
                'view_state': view_state,
                'generator': generator
            },
 
            callback=self.parse_data
        )
 
    def parse_data(self, response):
        
        # pagination
        current_page = response.meta['current_page']
        view_state  = response.meta['view_state']
        generator  = response.meta['generator']
        
        for row in response.xpath("(//table)[2]//tr[position() > 3]"):
            
            # CANTIDAD
            if self.qty_items < self.counter:
                return
            self.counter += 1
            
            yield {
                'ID': row.xpath(".//td[2]/span/text()").get(),
                'RUC': row.xpath(".//td[3]/span/text()").get(),
                'MINERO_INFORMAL': row.xpath(".//td[4]/span/text()").get(),
                'CODIGO_UNICO': row.xpath(".//td[5]/span/text()").get(),
                'NOMBRE': row.xpath(".//td[6]/span/text()").get(),
                'DEPARTAMENTO': row.xpath(".//td[7]/span/text()").get(),
                'PROVINCIA': row.xpath(".//td[8]/span/text()").get(),
                'DISTRITO': row.xpath(".//td[9]/span/text()").get(), 
            }
 
        next_page = current_page + 1
        
        '''if next_page == 2:
            return 'Ya van 2 páginas se acabó el payaso.'
            '''
        
        yield FormRequest.from_response(
            response,
            formdata={
                'ToolkitScriptManager1_HiddenField': '',
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': generator,
                '__VIEWSTATEENCRYPTED': '',
                'txtpagina': str(next_page),
                'txttotal': '3555',
                'txtruc': '',
                'txtdeclarante': '',
                'ddltipersona': '',
                'txtidunidad': '',
                'txtnomderecho': '',
                'ddldepartamento': '99',
                'ddlordenado': '1',
                'ddlforma': 'ASC',
                'ImgBtnSiguiente.x': '3',
                'ImgBtnSiguiente.y': '16'
            },
 
            meta={
                'current_page': next_page,
                'view_state': view_state,
                'generator': generator
            },
 
            callback=self.parse_data
        )