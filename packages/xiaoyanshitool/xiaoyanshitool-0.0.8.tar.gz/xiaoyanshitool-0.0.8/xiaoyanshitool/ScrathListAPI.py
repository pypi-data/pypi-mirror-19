# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from bs4 import BeautifulSoup
import requests
import xlwt as ExcelWrite
from time import  sleep
import os


class ScrathList:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        self.outputFilePath = os.path.dirname(__file__) + '/outputListFile.xls'
        self.start_row = 0


    def __getList(self, outputSheet, url):
        print "要抓取的URL：" + str(url)
        html = requests.get(url, headers=self.headers).text
        beautyHtml = BeautifulSoup(html, 'lxml')

        uls = beautyHtml.find_all('ul')
        if uls:
            print "一共找到 " + str(len(uls)) + " 个列表"
            for ul in uls:
                outputSheet.write(self.start_row, 0, label="列表")
                lis = ul.find_all('li')

                if lis:
                    row_count = len(lis)
                    print "列表中一共 " + str(row_count) + "行"
                    for i in xrange(0, row_count):
                        li = lis[i]
                        li_value = li.text
                        outputSheet.write(self.start_row, 1, label=li_value)
                        self.start_row = self.start_row + 1
                else:
                    print "列表ul中没有li数据"
                self.start_row = self.start_row + 1

        else :
            print url + " 中没有列表格式数据"

    def getExcelFromList(self, url, outputFilePath="currentFolder/outputListFile.xls"):
        outputFile = ExcelWrite.Workbook(encoding='utf-8')
        outputSheet = outputFile.add_sheet("output_sheet", cell_overwrite_ok=True)

        self.__getList(outputSheet, url)

        if outputFilePath == "currentFolder/outputListFile.xls":
            outputFilePath=self.outputFilePath

        print "生成Excel成功：" + outputFilePath
        outputFile.save(self.outputFilePath)