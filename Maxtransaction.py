#!/usr/bin/env python3

from bitcoinrpc.authproxy import AuthServiceProxy  #pip install python-bitcoinrpc

rpc_user = 'bitcoinrpc'
rpc_password = '123456'
rpc_host = '127.0.0.1'
rpc_port = 7117

p = AuthServiceProxy("http://%s:%s@%s:%s" %
                     (rpc_user, rpc_password, rpc_host, rpc_port))

def CreateMaxTransaction():
    list = []
    send = {}
    for i in range(0, 2500):
        print('<-----------%d------------>' % i)
        address = p.getnewaddress()
        list.append(address)
        send[address] = 0.001
    print('Address count=',len(list))
    txid = p.sendmany("", send, 0)
    print('txid:', txid)

def CreateMaxBlock():
    list = []
    send = {}
    listlocal = p.getaddressesbyaccount("")
    for k in range(0, 320):
        print('<-----------%d------------>' % k)
        address = listlocal.pop(0)
        list.append(address)
        send[address] = 0.001
    for j in range(0, 100):
        print('<-----------%d------------>' % j)
        txid = p.sendmany("", send, 0)
        print('txid:', txid)
    print('end')

if __name__ == '__main__':
    CreateMaxTransaction()
    #CreateMaxBlock()