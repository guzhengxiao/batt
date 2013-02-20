#!/opt/local/bin/python2.7

import zmq, getopt , sys , random, time
from struct import *
def main():
    opts , args = getopt.getopt( sys.argv[1:] , "hn:z:" )
    send_count = 1
    zmq_host = 'tcp://127.0.0.1:5858'
    unlimit = False
    for o,a in opts:
        if o == '-h':
            echohelp()
            sys.exit(0)
        if o == '-n':
            try:
                send_count = int( a )
            except:
                if a == 'unlimit':
                    unlimit = True
                else:
                    print '-n must be integer or unlimit'
                    sys.exit(1)
        if o == '-z':
            zmq_host = a
    s = connzmq(zmq_host)

    i = 0
    while unlimit == True or i < send_count :
        data = {
            '@class' : 'bnow_test'
            ,'@time' : str(int(time.time()))
            ,'name' : random.choice('abcdefghijklmnopqrstuvwxyz') * 3
            ,'length' : str(random.randint( 0 , 1000000 ))
        }
        msg = madebin( data )
        s.send( msg , copy=False )
        i += 1
        if i % 10000 == 0:
            print str(i) + ' messages has send '
    print str(i)+' messages has send '
    print 'finish'

def madebin( data ):
    msg = ''
    for k,v in data.iteritems():
        lenk = len(k)
        lenv = len(v)
        msg += pack( '>' + str(lenk+1) + 'ph' + str(lenv) + 's' , k ,lenv, v )
    return msg
    
def connzmq( host ):
    ctx = zmq.Context()
    s = ctx.socket(zmq.PUB)
    s.connect(host)
    return s
    
def echohelp():
    print 'hello i\'m help'

if __name__ == "__main__":
    main()
