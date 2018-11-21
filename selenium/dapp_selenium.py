# -*- coding: utf-8 -*-
import copy
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #谷歌
from pymongo import *
import re
import  logging
#from selenium.webdriver import Firefox #火狐
#from selenium.webdriver.firefox.options import Options #火狐


dapp_list = []
every_list = []
detail_urls = {}

client = MongoClient(host="localhost", port=27017)
#client = MongoClient("mongodb://test:123456@127.0.0.1:27017/?authSource=test")
#mydb = client["test"]
mydb = client["dapp"]
my_set = mydb["dapp_info"]

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.INFO, format=LOG_FORMAT)

class dappViewSpider(object):
    options = Options()
    #options.add_argument('--headless') #指定后台运行浏览器模式
    options.add_argument('--disable-gpu')
    options.add_argument('lang=zh_CN.UTF-8')
    driver = webdriver.Chrome(options=options) #谷歌
    #driver = Firefox(executable_path='/usr/local/bin/geckodriver',firefox_options=options) #火狐
    driver.implicitly_wait(10)

    def run(self):
        logging.info('--------------------------------------------')
        logging.info('--------------------------------------------')
        logging.info('--------------------------------------------')
        self.driver.get("https://dapp.review/explore/eos")
        logging.info('-------开始模拟鼠标滚动--------')
        pos = 0
        for i in range(1500):#开始模拟鼠标滚动
            pos += i * 500
            js = "document.documentElement.scrollTop=%d" % pos
            self.driver.execute_script(js)
        time.sleep(3)
        self.parseList()
        self.getDappUrl()
        self.driver.quit()

    def parseList(self):
        localtime = int(time.time())
        divs = self.driver.find_elements_by_tag_name('small')
        logging.info(u"当前时间戳:%s,需要爬取%s个dapp应用"%(localtime,len(divs)))
        for i in range(len(divs)):
            dapp_info = {}
            #dapp_info['index'] = int(divs[i].find_element_by_xpath('..//..//a').text)  # ID
            dapp_info['name'] = divs[i].find_element_by_xpath('..//..//h2').text #标题
            dapp_info['dau'] = int(re.sub('[,]', '', divs[i].find_element_by_xpath('..//..//..//span[2]').text)) #日活
            dapp_info['txAmount'] = float(re.sub('[,]', '',divs[i].find_element_by_xpath('..//..//..//div[4]//div//p[2]//span[2]').text)) #24h 交易额
            dapp_info['txCount'] = int(re.sub('[,]', '',divs[i].find_element_by_xpath('..//..//..//div[4]//div//p[3]//span[2]').text)) #24h 交易笔数
            dapp_info['type'] = divs[i].text #类型
            dapp_info['url'] = divs[i].find_element_by_xpath('..//..//a').get_attribute("href") #详情链接
            try :
                dapp_info['icon'] = divs[i].find_element_by_xpath('..//..//../img').get_attribute("src") #image详情链接
            except:
                dapp_info['icon'] = ""
            #dapp_info['score'] = ""
            dapp_info['reviewed'] = False
            dapp_info['time'] = localtime
            dapp_info['officialSite'] = ""
            logging.info(u"正在获取：%s"%dapp_info)
            dapp_list.append(dapp_info)
            every_info = copy.deepcopy(dapp_info)
            every_info.pop('reviewed')
            every_list.append(every_info)

    def getDappUrl(self):
        i = 0
        for info in dapp_list:
            self.driver.get(info['url'])
            time.sleep(2)
            try:
                divs1 = self.driver.find_element_by_tag_name('h2')
                name = divs1.text
                url = divs1.find_element_by_xpath('../a').get_attribute("href")
            except:
                url = ""
            detail_urls[name] = re.sub(r'(\/\#|\?|\/dappreview).*', '', url)
            i+=1
            logging.info(u"officialSite %d %s %s"%(i,name,detail_urls[name]))

    def createInfoCollection(self):
        my_set.insert_many(dapp_list)
        if detail_urls:
            for key,value in detail_urls.items():
                newvalues = {"$set": {"officialSite": value}}
                myquery = {"name": key }
                try:
                    my_set.update_one(myquery, newvalues)
                except:
                    logging.error(u'更新失败-%s'% key)

    def updateInfoCollection(self):
        for dapp in dapp_list:
            dapp['officialSite'] = detail_urls[dapp['name']]
            myquery = {"name": dapp['name']}
            try:
                result = my_set.find_one(myquery)
                if result is None:
                    my_set.insert_one(dapp)
                else:
                    if dapp['officialSite'] == "":
                        newvalues =  {"$set": {"dau": dapp['dau'],
                                           "txAmount": dapp['txAmount'],
                                           "txCount": dapp['txCount'],
                                           "time": dapp['time']
                                           }}
                    else:
                        newvalues =  {"$set": {"dau": dapp['dau'],
                                           "txAmount": dapp['txAmount'],
                                           "txCount": dapp['txCount'],
                                            "time": dapp['time'],
                                           "officialSite": dapp['officialSite']
                                           }}
                    my_set.update_one(myquery, newvalues)
            except:
                logging.error(u'查询失败-%s'% dapp['name'])

    def updateDapps(self):
        dapp_history = mydb['dapp_history']
        for dapp in every_list:
            #my_dapp = mydb[dapp['name']]
            dapp['officialSite'] = detail_urls[dapp['name']]
            try:
                dapp_history.insert_one(dapp)
            except:
                logging.error(u'插入失败-%s' % dapp['name'])

    def updateStep(self):
        result = my_set.find_one()
        if result is None:
            logging.info(u'-------创建dapp_info集合--------')
            self.createInfoCollection()
        else:
            logging.info(u'-------更新dapp_info集合--------')
            self.updateInfoCollection()
        logging.info(u'-------更新dapp_history集合--------')
        self.updateDapps()

if __name__ == '__main__':
    spider = dappViewSpider()
    spider.run()
    logging.info(u'-------开始更新数据库--------')
    spider.updateStep()
    logging.info(u'-------数据库更新完毕--------')
    client.close()