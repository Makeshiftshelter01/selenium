from pymongo import MongoClient
from ruri_connect import ConnectTo
from ruri_config import Config
from time import sleep
import math
import json
import os

import platform

class CrwalingDAO:
    #load db info
    def setdbinfo(self):
        host = "" # linux구분
        if platform.system() != "Linux":
            host = 'host'
        else:
            host = 'lhost'

        # ini파일을 이용해 접속 데이터 읽기
        config = Config()
        data = config.read_info_in_config('mongoDB')
        cnct = ConnectTo(data[host],int(data['port']),data['database'],data['collection']) #인스턴스화
        cnct.MongoDB() #mongoDB 접속, 현재는 mongoDB만 가능하지만 추후 다른 DB도 선택할 수 있도록 변경
        return cnct

    def insert_one(self, conn, keys, startini, endini, upper, lower, k):
        mongoDict = {}
        for j in range(startini, endini-1):
            # j를 이용해서 키 값을 넣을 때는 url과 head가 0, 1번을 차기하고 있기 때문에 +2를 넣어준다.
            mongoDict[keys[j+2]] = upper[j][k]
        
        # 컨텐츠 추가
        mongoDict['content'] = lower

        doc_id = conn.m_collection.insert_one(mongoDict).inserted_id
        print('no.', k+1, 'inserted id in mongodb : ', doc_id)

    def insert(self, cr, startini = 0, endini = 6):
        config = Config()

        # 크롤링 CSS를 가져오려 했는데 설정하는 기능이 없어 우선 ruriweb을 넣어 임시로 만듦.
        tmpruri = config.read_info_in_config('ruriweb')
        keys = list(tmpruri.keys())
        values = list(tmpruri.values())

        conn = self.setdbinfo() #접속값을 받아옴.
        upper = cr[0]
        lower = cr[1]
        exup = sorted(upper[0]) #자료를 가졌다고 생각하는 값을 선택
        rg = None #range

        print('titles this crawler has collected till now : ', len(exup)) ### 자료를 얼마나 모았을까? ###

        # 몽고DB에 입력
        # 만일 데이터가 1000개가 넘으면 500개 단위로 잘라 서버의 부담을 줄인다.
        if len(exup) > 1000:
            rg = math.ceil(len(exup)/500)
            # 전체를 500개로 나눈 몫의 수만큼 돌리고 500개가 안 되는 나머지는 별도로 돌린다.
            for i in range(rg):
                #몫의 범위만큼 loop를 돌리고 (rg가 최대값이 아닐 경우임)
                if i+1 != rg:
                    for k in range(i*500, (i+1)*500):
                        self.insert_one(conn, keys, startini, endini, upper, lower, k)
                    print('0.1초 sleep.')
                    sleep(0.1) #500번 입력 후 0.1초간 쉰다.
                #나머지의 범위만큼 loop를 돌림.
                else:  
                    for k in range(i*500, (i*500)+(len(exup) % 500)):
                        self.insert_one(conn, keys, startini, endini, upper, lower, k)

        # 1000개 이하면,   
        else:
            for i in range(0, len(exup)):
                self.insert_one(conn, keys, startini, endini, upper, lower, i)
        conn.m_client.close()

    def select(self, collection):
        config = Config()
        data = config.get_coll_dict(collection)
       
        host = "" # linux구분
        if platform.system() != "Linux":
            host = 'host'
        else:
            host = 'lhost'
        cnct = ConnectTo(data[host],int(data['port']),data['database'],data['collection'])
        cnct.MongoDB()
        cursor = cnct.m_collection.find({})
        
        result = []
        for l in cursor:
            result.append(l)
        return result


    def find_empty(self, collection):
        config = Config()
        data = config.get_coll_dict(collection)
       
        host = "" # linux구분
        if platform.system() != "Linux":
            host = 'host'
        else:
            host = 'lhost'
        cnct = ConnectTo(data[host],int(data['port']),data['database'],data['collection'])
        cnct.MongoDB()
        #cursor = cnct.m_collection.find({'content' : {'$size' : 0}}).limit(20)
        cursor = cnct.m_collection.find({'content' : {}}).limit(30)
        cnct.m_client.close()
        result = []
        for l in cursor:
            result.append(l)
        return result

    def find_fillblanks(self, collection):
        config = Config()
        data = config.get_coll_dict(collection)
       
        host = "" # linux구분
        if platform.system() != "Linux":
            host = 'host'
        else:
            host = 'lhost'
        cnct = ConnectTo(data[host],int(data['port']),data['database'],data['collection'])
        cnct.MongoDB()
        #cursor = cnct.m_collection.find({'content' : {'$size' : 0}}).limit(20)
        cursor = cnct.m_collection.find({'$and' : [{'content.ccontent': 'fillblanks'},
                            {'content.clinks': 'fillblanks'}, 
                            {'content.creplies': 'fillblanks'}, 
                            {'content.cthumbupl': 'fillblanks'},
                            {'content.cthumbdownl': 'fillblanks'}, 
                            {'content.idate': 'fillblanks'}, 
                            {'content.news_company': 'fillblanks'}]}).limit(30)
        cnct.m_client.close()
        result = []
        for l in cursor:
            result.append(l)
        return result    

    def update_one(self, result, collection, ids):
        config = Config()
        data = config.get_coll_dict(collection)
        #print(result)
        host = "" # linux구분
        if platform.system() != "Linux":
            host = 'host'
        else:
            host = 'lhost'
        cnct = ConnectTo(data[host],int(data['port']),data['database'],data['collection'])
        cnct.MongoDB()

        for i in range(len(ids)):
            cursor = cnct.m_collection.update_one({'_id': ids[i]}, {'$set': {'content': result[i]}})
            print('Updated', ids[i])

        cnct.m_client.close()