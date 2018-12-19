#   -*-  coding: utf-8  -*-
#   $Header$
# manager_server.py

import random, time, sys
try: import queue
except: import Queue as queue
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager): pass

Queue_len = 20
for var in ['task_queue','pid_queue']+['result_queue%s' %i for i in range(Queue_len)]:
    exec ('''%s = queue.Queue()''' % var)
    exec ('''def get_%s(): return %s''' %(var,var))
    exec ("""QueueManager.register('get_%s', callable=globals()['get_%s'])""" %(var,var))
    if var.startswith('result'):
        exec ("""pid_queue.put('get_%s')""" % var)

def server(host='127.0.0.1', port=5001, authkey=b'abc'):
    manager = QueueManager(address=(host,port), authkey=authkey)
    manager.start()
    print('manager_serv start on %s @ %s:%s, press ^C to break.' % (authkey, host, port))
    try:
        manager.join()
    except KeyboardInterrupt:
        print('mamager_serv stop.')

if __name__ == '__main__':
    """on the windows, manager_server must run after this suite"""

    server(*sys.argv[1:])

#   $log$
