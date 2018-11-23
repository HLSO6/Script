from lxml import etree
from pymongo import *
client = MongoClient(host="localhost", port=27017)
mydb = client["peer_info"]
my_set = mydb["pools"]
x11_set = mydb['x11']
x13_set = mydb['x13']
x17_set = mydb['x17']

def render(url):
    """Fully render HTML, JavaScript and all."""

    import sys
    from PyQt5.QtCore import QEventLoop,QUrl
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebEngineWidgets import QWebEngineView

    class Render(QWebEngineView):
        def __init__(self, url):
            self.html = None
            self.app = QApplication(sys.argv)
            QWebEngineView.__init__(self)
            self.loadFinished.connect(self._loadFinished)
            self.load(QUrl(url))
            while self.html is None:
                self.app.processEvents(QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)
            self.app.quit()

        def _callable(self, data):
            self.html = data

        def _loadFinished(self, result):
            self.page().toHtml(self._callable)

    return Render(url).html

def get_html():
    dummy_url = 'https://miningpoolstats.stream/'
    new_html = render(dummy_url)
    filename = 'eos.html'
    with open(filename, 'wb') as f:
        f.write(new_html.encode("utf-8"))
    f.close()

def html_info():
    filename = 'eos.html'
    with open(filename, 'rb') as f:
        new_html = f.read()
    f.close()
    html = etree.HTML(new_html)
    html_data = html.xpath('//tr[@role="row"]')
    print(html_data)
    for info in html_data:
        in_data = {}
        name = info.xpath('.//b/text()')
        algorithm = info.xpath('.//td[3]//div/text()')
        pools = info.xpath('.//td[8]//span/text()')
        pools_hashrate = info.xpath('.//td[9]//span/text()')
        if len(name) != 0:
            print("name:%s,alg:%s,pools:%s,pools_hashrate:%s"%(name[0],algorithm[0],pools[0],pools_hashrate[0]))
            in_data['name'] = name[0]
            in_data['algorithm'] = algorithm[0]
            in_data['poolNums'] = pools[0]
            in_data['poolsHashrate'] = pools_hashrate[0]
            my_set.insert_one(in_data)

def myQuery():
    info = my_set.find()
    for item in info:
        if item['algorithm'] == 'X11':
            x11_set.insert_one(item)
        elif item['algorithm'] == 'X13':
            x13_set.insert_one(item)
        elif  item['algorithm'] == 'X17':
            x17_set.insert_one(item)
        else:
            continue

if __name__ == '__main__':
    myQuery()