#!/opt/local/bin/python2.7

import zmq, getopt , sys , random, time ,yaml
from threading import Thread
from struct import *
def main():
    opts , args = getopt.getopt( sys.argv[1:] , "hn:z:t:s:f:" )
    send_count = 1
    thread_count = 1
    sleep_time = 0
    zmq_host = 'tcp://127.0.0.1:5858'
    unlimit = False
    bdata = None
    for o,a in opts:
        if o == '-h':
            echohelp()
            sys.exit(0)
        if o == '-f':
            f = open(a)
            bdata = yaml.load(f)
        if o == '-t' :
            try:
                thread_count = int( a )
            except:
                print '-t must be integer'
                sys.exit(1)
        if o == '-s' :
            try:
                sleep_time = float( a )
            except:
                print '-t must be number'
                sys.exit(1)
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
    try:
        for i in range( 0 , thread_count ):
            t = Thread(None , send , None , ( i,unlimit, zmq_host , send_count , sleep_time ,bdata,s ) ) 
            t.start()
    except Exception as errtxt:
        print errtxt

def send( item,unlimit, zmq_host , send_count , sleep_time , bdata, s) :
    item += 1
    i = 0
    while unlimit == True or i < send_count :
        if bdata == None:
            data = random_data()
        else:
            data = choice_data( bdata )
        msg = madebin( data )
        s.send( msg , copy=False )
        i += 1
        if i % 10000 == 0:
            print 'thread ' + str(item) + ' ' + str(i) + ' messages has send '
        if sleep_time >0 :
            time.sleep( sleep_time )
    print 'thread ' + str(item) + ' ' + str(i)+' messages has send '
    print 'thread ' + str(item) + ' finish'
    

def madebin( data ):
    msg = ''
    for k,v in data.iteritems():
        v = str(v)
        lenk = len(k)
        lenv = len(v)
        msg += pack( '>' + str(lenk+1) + 'ph' + str(lenv) + 's' , k ,lenv, v )
    return msg
    
def connzmq( host ):
    ctx = zmq.Context()
    s = ctx.socket(zmq.PUB)
    s.connect(host)
    return s

def random_data():
    return {
        '@class' : 'bnow_test'
        ,'@time' : str(int(time.time()))
        ,'name' : random.choice('abcdefghijklmnopqrstuvwxyz') * 3
        ,'length' : str(random.randint( 0 , 1000000 ))
    }
def choice_data(bdata):
    return random.choice(bdata)
    
    
def echohelp():
    print 'hello i\'m help'

if __name__ == "__main__":
    main()
