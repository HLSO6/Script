from pymongo import *
import re

client = MongoClient(host="localhost", port=27017)
mydb = client["peer_info"]
my_set = mydb["peer"]
your_set = mydb["update_peer"]
no_set = mydb["update"]
ip_set = mydb["only_ip"]
up_set = mydb["update_ip"]

def rmDuplicate():#对update集合去重到update_peer
    info = no_set.find()
    print("去重前个数:%d" % (no_set.estimated_document_count()))
    for item in info:
        query = {'addr':item['addr']}
        result = your_set.find_one(query)
        if result is None:
            your_set.insert_one(item)
    print("去重后个数:%d" % (your_set.estimated_document_count()))

def rmDuplicateIp():#对only_ip集合的去重到update_ip
    info = ip_set.find()
    print("去重前个数:%d" % (ip_set.estimated_document_count()))
    for item in info:
        query = {'addr':item['addr']}
        result = up_set.find_one(query)
        if result is None:
            up_set.insert_one(item)
    print("去重后个数:%d" % (up_set.estimated_document_count()))

def myQuery(): #清理收集的数据到update集合
    info = my_set.find()
    for item in info:
        if item['seed'] != '':
            no_set.insert_one(item)
    print("节点个数:%d" % (no_set.estimated_document_count()))

def myIpInfo():#对update集合的addr去除端口到only_ip
    info = no_set.find()
    for item in info:
        item['addr'] = re.sub(r'\:.*', '', item['addr'])
        ip_set.insert_one(item)

'''
    清理收集的数据到update集合
    对update集合去重到update_peer
    
    对update集合的addr去除端口到only_ip
    对only_ip集合的去重到update_ip
'''

if __name__ == '__main__':
    #rmDuplicate()
    #myQuery()
    #myIpInfo()
    rmDuplicateIp()