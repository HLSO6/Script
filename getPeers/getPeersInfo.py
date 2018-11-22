from bitcoinrpc.authproxy import AuthServiceProxy
import json
from  decimal import Decimal

rpc_user = '123'
rpc_password = '123'
rpc_host = '127.0.0.1'
rpc_port = 7116

p = AuthServiceProxy("http://%s:%s@%s:%s" %
                     (rpc_user, rpc_password, rpc_host, rpc_port))


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) == type(Decimal()):
            return obj.to_eng_string()
        return json.JSONEncoder.default(self, obj)

def getPeeInfo():
    info = p.getpeerinfo()
    js = json.dumps(info,cls=MyEncoder)
    with open('test.txt', 'w') as file:
        file.write(js)
    print(info)

if __name__ == '__main__':
    getPeeInfo()
    # readPeeInfo()