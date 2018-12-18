import copy
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #谷歌
from pymongo import *
import re
import  logging

#dapp_info = []
client = MongoClient(host="localhost", port=27017)
mydb = client["dapp"]
my_set = mydb["dapp_infox"]
my_history = mydb["dapp_historyx"]

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='dapp_url.log', level=logging.INFO, format=LOG_FORMAT)

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
        self.getDappUrl()
        # logging.info('--------------开始更新数据---------------------')
        # #self.insertCollection()
        # logging.info('--------------更新完毕---------------------')

    def getDappUrl(self):
        i = 0
        dapp_list = my_set.find()
        for info in dapp_list:
            if info['officialSite'] == "" :
                self.driver.get(info['url'])
                time.sleep(1)
                try:
                    divs1 = self.driver.find_element_by_tag_name('h1')
                    name = divs1.text
                    url = divs1.find_element_by_xpath('../div//a').get_attribute("href")
                except:
                    name = ""
                    url = ""
                url = re.sub(r'(\/\#|\?|\/dappreview).*', '', url)
                myquery = {"name": info['name']}
                newvalues = {"$set": {"officialSite": url}}
                my_set.update_one(myquery, newvalues)
                my_history.update_many(myquery, newvalues)
                #detail_urls = {}
                #detail_urls['name'] = info['name']
                #detail_urls['officialSite'] = url
                #dapp_info.append(detail_urls)
                i+=1
                logging.info(u"officialSite %d %s %s=%s" % (i, url, name, info['name']))
            else:
                myquery1 = {"name": info['name']}
                newvalues1 = {"$set": {"officialSite": info['officialSite']}}
                my_history.update_many(myquery1, newvalues1)
        self.driver.quit()

    # def insertCollection(self):
    #     logging.info(len(dapp_info))
    #     for info in dapp_info:
    #         if info['officialSite'] != "":
    #             myquery = {"name": info['name']}
    #             newvalues = {"$set": {"officialSite": info['officialSite']}}
    #             my_set.update_one(myquery, newvalues)
    #             my_history.update_many(myquery, newvalues)

if __name__ == '__main__':
    spider = dappViewSpider()
    spider.run()