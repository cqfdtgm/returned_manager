#   -*-  coding: utf-8  -*-
#   $Header$
#   manager_worker.py

import sys
from .worker import rpc

def test(host='127.0.0.1',port=5001,authkey=b'abc'):
    for n in range(10):
        result = rpc(host, port, authkey, n)
        print(n, result)

if __name__=='__main__':
    test(*sys.argv[1:])

