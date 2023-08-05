# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from bs4 import BeautifulSoup
import requests
import xlwt as ExcelWrite
from time import  sleep
import os

class ScrathTable:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        self.outputFilePath = os.path.dirname(__file__) + '/outputTableFile.xls'
        self.start_row = 0


    def __getExcel(self, outputSheet, url):
        print "要抓取的URL：" + str(url)
        html = requests.get(url, headers=self.headers).text
        beautyHtml = BeautifulSoup(html, 'lxml')

        tables = beautyHtml.find_all('table')
        if tables:
            print "一共找到 " + str(len(tables)) + " 个表格"
            for table in tables:
                outputSheet.write(self.start_row, 0, label="表格")
                trs = table.find_all('tr')

                if trs:
                    row_count = len(trs)
                    print "表格中一共 " + str(row_count) + "行（算表头）"
                    for i in xrange(0, row_count):
                        tr = trs[i]
                        tds = tr.find_all('td')
                        if tds==None:
                            tds = tr.find_all('th')
                            if tds==None:
                                print "不包括td th, 可能有其他元素标签"
                        col_count = len(tds)
                        for j in xrange(0, col_count):
                            td = tds[j]
                            td_value = td.text
                            print td_value.encode('utf8')
                            outputSheet.write(self.start_row, j + 1, label=td_value)
                        self.start_row = self.start_row + 1
                else:
                    print "表格tr中没有数据"
                self.start_row = self.start_row + 1

        else :
            print url + " 中没有表格格式数据"

    def getExcelFromTable(self, url, outputFilePath="currentFolder/outputTableFile.xls"):
        outputFile = ExcelWrite.Workbook(encoding='utf-8')
        outputSheet = outputFile.add_sheet("output_sheet", cell_overwrite_ok=True)

        self.__getExcel(outputSheet, url)

        if outputFilePath == "currentFolder/outputTableFile.xls":
            outputFilePath=self.outputFilePath

        print "生成Excel成功：" + outputFilePath
        outputFile.save(self.outputFilePath)