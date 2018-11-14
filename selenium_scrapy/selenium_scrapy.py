# coding=utf-8

import time

from selenium import webdriver

class SinaBookSpider(object):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    total = 1526
    count = 0
    location = 0
    click_times = 0

    def run(self):
        self.driver.get("https://dapp.review/explore/eos?category=4&categorySecondary=")
        time.sleep(2)
        self.parselist()
        self.driver.quit()

    def parselist(self):
        """
        解析列表
        :return:
        """
        divs = self.driver.find_elements_by_class_name("jss328")
        print(divs)
        print(len(divs))
        for i in range(len(divs)):
            title = divs[i].find_element_by_tag_name('h2').text
            #count = divs[i].find_element_by_xpath('.//p/span').text
            count = divs[i].find_element_by_xpath('.//p/span[@class="jss112 jss121 jss346 jss350"]').text
            total_amount = divs[i].find_element_by_xpath('.//p/span[@class="jss112 jss121 jss348 jss350"]').text
            #count = divs[i].find_element_by_xpath('.//p/span[2]').text
            #count = divs[i].find_element_by_tag_name('span').text
            print("标题:%s,日活:%s,24h交易额:%s"%(title,count,total_amount))


if __name__ == '__main__':
    spider = SinaBookSpider()
    spider.run()

'''
dummy_url = 'https://btc.com/'
new_html = render(dummy_url)
print(new_html)
filename = 'eos.html'
with open(filename, 'wb') as f:
    f.write(new_html.encode("utf-8"))
f.close()
'''