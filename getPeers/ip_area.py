import json
import urllib.request
from pymongo import *

def get_data(ip):
    API = "http://ip.taobao.com/service/getIpInfo.php?ip="
    url = API + ip
    jsondata = json.loads(urllib.request.urlopen(url).read())

    if jsondata['code'] == 1:
        print("No %s info." % ip)
        exit(1)
    else:
        return jsondata

def get_ip():
    client = MongoClient(host="localhost", port=27017)
    mydb = client["peer_info"]
    up_set = mydb["update_ip"]
    info = up_set.find()
    for item in info:
        if item['city'] is not None:
            continue
        data = get_data(item['addr'])
        newvalues ={'$set': {'country':data['data']['country'],'city':data['data']['city']}}
        myquery = {'addr':item['addr']}
        up_set.update_one(myquery,newvalues)
        print("国家:%s,城市:%s" % (data['data']['country'], data['data']['city']))

if __name__ == '__main__':
    #info = get_data('52.44.110.113')
    #print(info)
    #print("国家:%s,城市:%s"%(info['data']['country'],info['data']['city']))
    get_ip()