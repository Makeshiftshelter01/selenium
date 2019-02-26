import json
import platform
import sys

# config
from ruri_config import Config

#셀레니움 크롤링
#from selenium_crawl import selenium_WebCrawler
from selenium_crawl_test import selenium_WebCrawler
# 크롤링
class Crawling:
    # 기본값 호출
    def setcsstags(self, target):
        #크롤링 가능한 website 존재유무 => 일단 주소를 넘긴다.
        config = Config()
        if config.read_init_config(target) != True:
            sys.exit()
        ctargetdata = config.read_info_in_config(target)
        return ctargetdata

  
    #셀레니움 크롤링
    def selenium_upperpage(self,start_page, target, lastpage, pagetype ='page'):
        ##### 세팅 정보
        ctargetdata = self.setcsstags(target) #크롤링 하기 위한 타겟 사이트의 필수 데이터 호출
        
        ##### 실행 및 결과 호출
        sw = selenium_WebCrawler() #웹 크롤러 기능 활성화
        sw.selenium_upperpage_only(start_page, lastpage, ctargetdata, pagetype) #크롤링 실행 및 결과를 변수에 담음
        #return result

    def selenium_lowerpage(self, coll, target):
        ##### 세팅 정보
        ctargetdata = self.setcsstags(target) #크롤링 하기 위한 타겟 사이트의 필수 데이터 호출
        
        ##### 실행 및 결과 호출
        sw = selenium_WebCrawler() #웹 크롤러 기능 활성화
        sw.selenium_lowerpage_only(coll, ctargetdata) #크롤링 실행 및 결과를 변수에 담음
        #return result

    def selenium_fixerrors(self, coll, target):
        ##### 세팅 정보
        ctargetdata = self.setcsstags(target) #크롤링 하기 위한 타겟 사이트의 필수 데이터 호출
        
        ##### 실행 및 결과 호출
        sw = selenium_WebCrawler() #웹 크롤러 기능 활성화
        sw.selenium_lowerpage_fix(coll, ctargetdata) #크롤링 실행 및 결과를 변수에 담음
        #return result