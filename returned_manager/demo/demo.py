#   -*-  coding: utf-8  -*-
#   $Header$
#   demo.py

"""to use this demo, please install returned_manager first:
    pip install returned_manager
    or download it and run:
    python setup.py install
    """
import sys    
from returned_manager import server, worker, rpc, test

if __name__=='__main__':
    """"
    To run this in three command line windws, in one machine, or in defrent machines ( test and worker must appoint "host" to server's IP, and of course, port and authkey must same as the server.
    In fact, because module  'multiprocessing.managers' between python 2.x and 3.x have some problem , you must run server|worker|test both in 2.x or in 3.x.
    """

    if len(sys.argv)<2: #   no argv, print help message
        print("""   python demo server|worker|test [host [port [authkey]]] """
    if sys.argv[1] == 'server':
        server(*sys.argv[2:])
    elif sys.argv[1] == 'worker':
        worker(*sys.argv[2:])
    elif sys.agv[1] == 'test':
        test(*sys.argv[2:])
