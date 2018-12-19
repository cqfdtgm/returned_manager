#   -*-  coding: utf-8  -*-
#   $Header$
#   manager_worker.py

import random, time, sys
try: import queue
except: import Queue as queue
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager): pass

from .server import Queue_len
for var in ['task_queue','pid_queue']+['result_queue%s' %i for i in range(Queue_len)]:
    exec ("""QueueManager.register('get_%s')""" %(var))

def test_func(x):
    time.sleep(random.randint(0,3))
    return x*x

def worker(host="127.0.0.1", port=5001, authkey=b'abc', func=test_func):
    print(host, port, authkey, func)
    while True:
        try:
            m = QueueManager(address=(host, port), authkey=authkey)
            m.connect()
            print('connect to serv')
            task = m.get_task_queue()
            con = task.get(timeout=9)
            print('con: ', con)
            pid = con['pid']
            k, kw = con['k'], con['kw']    # content must be dict
            result = func(*k, **kw)
            print('result', result)
            pid = getattr(m, pid)()
            print('to put result')
            pid.put(result)
        except ConnectionRefusedError:
            print('manager serv not running! wait to retry..')
            time.sleep(5)
        except queue.Empty:
            print('task queue is empty! wait to retry..')
        except KeyboardInterrupt:
            print('user stop the worker.')

def rpc(host='127.0.0.1', port=5001, authkey=b'abc', *k, **kw):
    """wrap the function"""

    m = QueueManager(address=(host, port), authkey=authkey)
    m.connect()
    print('get pid_s')
    pid_s = m.get_pid_queue().get()
    pid = getattr(m, pid_s)()
    print('pid_s', pid_s)
    task = m.get_task_queue()
    print('get_task', task)
    task.put({'pid':pid_s,'k': k, 'kw':kw})
    print('to get result')
    result = pid.get()
    print('to get result')
    m.get_pid_queue().put(pid_s)
    print('put back pid_s')
    return result

if __name__=='__main__':
    worker(*sys.argv[1:])
