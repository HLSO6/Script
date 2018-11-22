import json
from pymongo import *

client = MongoClient(host="localhost", port=27017)
mydb = client["peer_info"]
my_set = mydb["peer"]

def readPeeInfo():
    with open('test.txt', 'r') as file:
        js = file.read()
    peers_list = json.loads(js)
    for addr in peers_list:
        info = {}
        info['ids'] = addr['id']
        info['addr'] = addr['addr']
        info['version'] = addr['version']
        info['subver'] = addr['subver']
        info['ip'] = '137.116.138.155'
        info['seed'] = 'seed6'
        my_set.insert_one(info)
    print(peers_list)

if __name__ == '__main__':
    readPeeInfo()