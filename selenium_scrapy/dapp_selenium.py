# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import *
import re

dapp_list = []
detail_urls = {}

client = MongoClient(host="localhost", port=27017)
mydb = client["dapp"]

class DappViewSpider(object):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    #driver = webdriver.Chrome(chrome_options=chrome_options)
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    def run(self):
        self.driver.get("https://dapp.review/explore/eos")
        '''
        print('-------开始模拟鼠标滚动--------')
        pos = 0
        for i in range(1500):#开始模拟鼠标滚动
            pos += i * 500
            js = "document.documentElement.scrollTop=%d" % pos
            self.driver.execute_script(js)
        '''
        time.sleep(3)
        self.ParseList()
        self.GetDappUrl()
        self.driver.quit()

    def ParseList(self):
        localtime = int(time.time())
        print(localtime)
        divs = self.driver.find_elements_by_tag_name('small')
        print(len(divs))
        for i in range(len(divs)):
            dapp_info = {}
            dapp_info['index'] = int(divs[i].find_element_by_xpath('..//..//a').text)  # ID
            dapp_info['title'] = divs[i].find_element_by_xpath('..//..//h2').text #标题
            dapp_info['dau'] = int(re.sub('[,]', '', divs[i].find_element_by_xpath('..//..//..//span[2]').text)) #日活
            dapp_info['tx_amount'] = float(re.sub('[,]', '',divs[i].find_element_by_xpath('..//..//..//div[4]//div//p[2]//span[2]').text)) #24h 交易额
            dapp_info['tx_count'] = int(re.sub('[,]', '',divs[i].find_element_by_xpath('..//..//..//div[4]//div//p[3]//span[2]').text)) #24h 交易笔数
            dapp_info['type'] = divs[i].text #类型
            dapp_info['url'] = divs[i].find_element_by_xpath('..//..//a').get_attribute("href") #详情链接
            try :
                dapp_info['icon'] = divs[i].find_element_by_xpath('..//..//../img').get_attribute("src") #image详情链接
            except:
                dapp_info['icon'] = ""
            dapp_info['score'] = ""
            dapp_info['reviewed'] = False
            dapp_info['time'] = localtime
            dapp_info['dapp_url'] = ""
            print(dapp_info)
            dapp_list.append(dapp_info)
        print('-------Dapp总个数:%d--------'% len(dapp_list))

    def GetDappUrl(self):
        i = 0
        for info in dapp_list:
            self.driver.get(info['url'])
            time.sleep(2)
            divs1 = self.driver.find_element_by_tag_name('h2')
            title = divs1.text
            try:
                url = divs1.find_element_by_xpath('../a').get_attribute("href")
            except:
                url = ""
            detail_urls[title] = url
            i+=1
            print(i,title,url)

    def CreateInfoCollection(self):
        my_set = mydb["dapp_info"]
        my_set.insert_many(dapp_list)
        if detail_urls:
            for key,value in detail_urls.items():
                newvalues = {"$set": {"dapp_url": value}}
                myquery = {"title": key }
                my_set.update_one(myquery, newvalues)

    def UpdateInfoCollection(self):
        my_set = mydb["dapp_info"]
        for dapp in dapp_list:
            myquery = {"title": dapp['title']}
            result = my_set.find_one(myquery)
            if result is None:
                my_set.insert_one(dapp)
            else:
                newvalues =  {"$set": {"index": dapp['index'],
                                       "dau": dapp['dau'],
                                       "tx_amount": dapp['tx_amount'],
                                       "tx_count": dapp['tx_count']
                                       }}
                my_set.update_one(myquery, newvalues)
        print('-------更新dapp_url--------')
        if detail_urls:
            for key,value in detail_urls.items():
                newvalues1 = {"$set": {"dapp_url": value}}
                myquery1 = {"title": key}
                result1 = my_set.find_one(myquery1)
                if result1['dapp_url'] =='':
                    my_set.update_one(myquery1, newvalues1)


    def UpdateDapps(self):
        for dapp in dapp_list:
            my_set = mydb[dapp['title']]
            my_set.insert_one(dapp)

    def UpdateStep(self):
        mydb = client["dapp"]
        my_set = mydb["dapp_info"]
        result = my_set.find_one()
        if result is None:
            print('-------创建dapp_info集合--------')
            self.CreateInfoCollection()
        else:
            print('-------更新dapp_info集合--------')
            self.UpdateInfoCollection()
        print('-------更新所有dapp集合--------')
        self.UpdateDapps()

if __name__ == '__main__':
    spider = DappViewSpider()
    spider.run()
    print('-------开始更新数据库--------')
    spider.UpdateStep()
    print('-------数据库更新完毕--------')
    client.close()