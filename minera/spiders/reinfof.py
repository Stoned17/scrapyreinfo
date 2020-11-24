import scrapy
from scrapy import FormRequest
 
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os, datetime


load_dotenv(find_dotenv())


class ReinfofSpider(scrapy.Spider):
    export_file_name = os.getenv('EXPORT_FILE')
    file_name = 'reinfo{:%d%m%y-%H%M%S}.'.format(datetime.datetime.now())

    export_format = [
        {},
        {
            f'{file_name}json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
            },
        },
        {
            f'{file_name}csv': {
                'format': 'csv',
            },
        },
    ]

    qty_items = int(os.getenv('QTY_ITEMS'))
    counter = 1
    current_page = int(os.getenv('CURRENT_PAGE')) - 1
    qty_pages = os.getenv('QTY_PAGES')
    ruc_number = os.getenv('RUC_NUMBER')
    nom_minero = os.getenv('NOMBRE_MINERO')
    tipo_person = os.getenv('TIPO_PERSONA')
    cod_derecho = os.getenv('COD_DERECHO')
    nom_derecho = os.getenv('NOM_DERECHO')
    departamento = os.getenv('DEPARTAMENTO')
    order_by = os.getenv('ORDER_BY')
    order_type = os.getenv('ORDER_TYPE')


    name = 'reinfof'
 
    start_urls = ['http://pad.minem.gob.pe/REINFO_WEB/Index.aspx']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'DOWNLOAD_DELAY': 1.5,
        #'LOG_ENABLED': False,
        'FEEDS': export_format[int(export_file_name)]
    }
    
    
 
    def parse(self, response):
        view_state = response.xpath(
            "//input[@name='__VIEWSTATE']/@value").get()
        generator = response.xpath(
            "//input[@name='__VIEWSTATEGENERATOR']/@value").get()
        qty_rows = response.xpath(
            "//span[@id='lbltotal']/text()").get()
        qty_pages = response.xpath('//input[@id="txttotal"]/@value').get()

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
                'txtpagina': str(self.current_page),
                'txttotal': qty_pages,
                'txtruc': self.ruc_number,
                'txtdeclarante': self.nom_minero,
                'ddltipersona': self.tipo_person,
                'txtidunidad': self.cod_derecho,
                'txtnomderecho': self.nom_derecho,
                'ddldepartamento': self.departamento,
                'ddlprovincia': '99',
                'ddlordenado': self.order_by,
                'ddlforma': self.order_type,
                'ImgBtnSiguiente.x': '3',
                'ImgBtnSiguiente.y': '16'
            },
 
            meta={
                'current_page': self.current_page,
            },
 
            callback=self.parse_data
        )
 
    def parse_data(self, response):
        
        # PAGINACION
        current_page = response.meta['current_page']

        view_state = response.xpath(
            "//input[@name='__VIEWSTATE']/@value").get()
        generator = response.xpath(
            "//input[@name='__VIEWSTATEGENERATOR']/@value").get()
        qty_rows = response.xpath(
            "//span[@id='lbltotal']/text()").get()
        qty_pages = response.xpath('//input[@id="txttotal"]/@value').get()

        if int(qty_pages) < current_page:
            return

        if self.qty_pages:
            if int(int(self.qty_pages) + self.current_page) == current_page:
                    return

        for row in response.xpath("(//table)[2]//tr[position() > 3]"):
            
            # CANTIDAD
            if not self.qty_pages and self.qty_items <= int(qty_rows):
                if self.qty_items < self.counter:
                    return
            else:
                self.qty_items = int(qty_rows)
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

        current_page = current_page + 1

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
                'txtpagina': str(current_page),
                'txttotal': qty_pages,
                'txtruc': self.ruc_number,
                'txtdeclarante': self.nom_minero,
                'ddltipersona': self.tipo_person,
                'txtidunidad': self.cod_derecho,
                'txtnomderecho': self.nom_derecho,
                'ddldepartamento': self.departamento,
                'ddlordenado': self.order_by,
                'ddlforma': self.order_type,
                'ImgBtnSiguiente.x': '3',
                'ImgBtnSiguiente.y': '16'
            },
 
            meta={
                'current_page': current_page,
            },
 
            callback=self.parse_data
        )