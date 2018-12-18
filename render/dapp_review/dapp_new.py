#coding:utf-8
import copy
import json
import urllib.request
import time
from urllib.request import Request
from pymongo import *
import socket
import re
import  logging

dapp_list = []
every_list = []
detail_urls = {}
localtime = int(time.time())

client = MongoClient(host="localhost", port=27017)
mydb = client["dapp"]
my_set = mydb["dapp_infox"]

tag_dic = {
    1:'以太坊',
    8:'波场',
    3:'柚子',
    2:'星云链',
    5:'小蚁',
    6:'其他'
}
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='dapp_new.log', level=logging.INFO, format=LOG_FORMAT)

def get_data():
    for j in [1, 2, 3, 5, 6, 8]:
        if j == 1:
            k = 65
        else:
            k = 10
        for i in range(1,k):
            socket.setdefaulttimeout(10)
            header = {'Accept-Language': 'zh-CN,zh;q=0.9'}
            url = "https://dapp.review/api/dapp/dapps/?search=&page=%s&page_size=24&is_support_chinese=flase&ordering=-dau_last_day&new=false&block_chain=%s" % (i,j)
            request = Request(url=url, headers=header)
            try:
                jsondata = json.loads(urllib.request.urlopen(request).read().decode('utf-8'))
                parseList(jsondata,tag_dic[j])
            except:
                continue

def str2_int(stri):
    int(re.sub('[,]', '', str(stri)))

def parseList(js,tag):
    #logging.info(js)
    if 'detail' not in js.keys():
        for info in js['results']:
            dapp_info = {}
            dapp_info['name'] = info['title']
            dapp_info['dau'] = info['dau_last_day'] != None and str2_int(info['dau_last_day']) or info['dau_last_day']
            dapp_info['txAmount'] = info['volume_last_day'] != None and  float(re.sub('[,]', '', str(info['volume_last_day']))) or info['dau_last_day']
            dapp_info['txCount'] = info['tx_last_day'] != None and str2_int(info['tx_last_day']) or info['tx_last_day']
            dapp_info['type'] = info['categories'][0]['category']
            dapp_info['url'] = 'https://dapp.review/dapp/%s' % info['id']
            dapp_info['icon'] = info['logo_url'] != None and info['logo_url'] or info['logo']
            if tag == '小蚁' or tag == '其他':
                dapp_info['description'] = info['description_short']
            else:
                dapp_info['description'] = ""
            dapp_info['reviewed'] = False
            dapp_info['time'] = localtime
            dapp_info['officialSite'] = ""
            dapp_info['tag'] = tag
            logging.info(u"正在获取：%s" % dapp_info)
            dapp_list.append(dapp_info)
            every_info = copy.deepcopy(dapp_info)
            every_info.pop('reviewed')
            every_list.append(every_info)

def updateDapps():
    dapp_history = mydb['dapp_historyx']
    dapp_history.insert_many(every_list)

def createInfoCollection():
    if len(dapp_list) != 0:
        my_set.insert_many(dapp_list)

def updateInfoCollection():
    for dapp in dapp_list:
        myquery = {"name": dapp['name']}
        try:
            result = my_set.find_one(myquery)
            if result is None:
                my_set.insert_one(dapp)
            else:
                newvalues = {"$set": {"dau": dapp['dau'],
                                      "txAmount": dapp['txAmount'],
                                      "txCount": dapp['txCount'],
                                      "time": dapp['time']
                                      }}
                my_set.update_one(myquery, newvalues)
        except:
            logging.error(u'查询失败-%s' % dapp['name'])

def updateStep():
    result = my_set.find_one()
    if result is None:
        logging.info(u'-------创建dapp_info集合--------')
        createInfoCollection()
    else:
        logging.info(u'-------更新dapp_info集合--------')
        updateInfoCollection()
    logging.info(u'-------更新dapp_history集合--------')
    updateDapps()

if __name__ == '__main__':
    get_data()
    updateStep()