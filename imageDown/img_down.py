import sys
import urllib.request
import json

file = open('test.txt', 'r')
js = file.read()
dapp_img = json.loads(js)
file.close()
for key,value in dapp_img.items():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=value, headers=headers)
    content = urllib.request.urlopen(req).read()
    type = sys.getfilesystemencoding()
    print(content)
    with open('./img/%s.jpg'% key,'wb') as f:
        f.write(content)
    f.close()