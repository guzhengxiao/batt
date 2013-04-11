#!/opt/local/bin/python2.7

# coding=utf-8
import zmq, getopt , sys , random, time ,json, mqconsume, os
from threading import Thread
from struct import *
bdata = []
def main():
    opts , args = getopt.getopt( sys.argv[1:] , "hn:z:t:s:f:qc:" )
    global bdata
    send_count = 1
    thread_count = 1
    sleep_time = 0
    zmq_host = 'tcp://127.0.0.1:5858'
    unlimit = False
    repeat = False
    classname = ''
    for o,a in opts:
        if o == '-h':
            echohelp()
            sys.exit(0)
        if o == '-q':
            repeat = True
        if o == '-f':
            f = open(a , "r")
            for dataline in f:
                try : 
                    tjson = json.loads(dataline)
                    bdata.append( tjson )
                except :
                    continue
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
        if o == '-c':
            classname = a
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
    if repeat == True :
        #bdata = []
        i = 0
        if bdata == []:
            for bdatafile in os.listdir('.'):
                if bdatafile[-6:] == '.bdata':
                    print bdatafile
                    bdatafp = open( bdatafile, "r" )
                    for bdataline in bdatafp:
                        try : 
                            zdata = json.loads(bdataline)
                            i += 1
                            zdata['@class'] = classname
                            zdata['@time'] = time.time()
                            zmqsend( zdata , s )
                            if i % 1000 == 0:
                                print 'has send ' + str(i) + ' messages '
                        except :
                            continue
        else:
            for zdata in bdata:
                i += 1
                zdata['@class'] = classname
                zdata['@time'] = time.time()
                zmqsend( zdata , s )
                if i % 1000 == 0:
                    print 'has send ' + str(i) + ' messages '
        print 'finished , has send ' + str(i) + ' message '
    else:
        try:
            for i in range( 0 , thread_count ):
                t = Thread(None , send , None , ( i,unlimit, zmq_host , send_count , sleep_time ,s ) ) 
                t.start()
        except:
            print 'Thread error  '

#qsend( zdata )

def send( item,unlimit, zmq_host , send_count , sleep_time ,  s) :
    global bdata
    item += 1
    i = 0
    time1 = str(int(time.time()))
    while unlimit == True or i < send_count :
        if bdata == []:
            data = random_data()
            data['@time'] = time1
        else:
            data = choice_data()
        print data
        zmqsend(data,s)
        i += 1
        if i % 10000 == 0:
            print 'thread ' + str(item) + ' ' + str(i) + ' messages has send '
        if sleep_time >0 :
            time.sleep( sleep_time )
    print 'thread ' + str(item) + ' ' + str(i)+' messages has send '
    print 'thread ' + str(item) + ' finish'
    
def zmqsend( data ,s ):
    msg = madebin( data )
    s.send( msg , copy=False )

def madebin( data ):
    msg = ''
    for k,v in data.iteritems():
        if type(k) == type(u''):
            k = k.encode('utf-8')
        else:
            k = str(k)
        if type(v) == type(u''):
            v = v.encode( 'utf-8' )
        elif type(v) == type({}) or type(v) == type([]):
            v = json.dumps(v)
        else :
            v = str(v)
        lenk = len(k)
        lenv = len(v)
        msg += pack( '>' + str(lenk+1) + 'ph' + str(lenv) + 's' , k ,lenv, v )
    return msg
    
def connzmq( host ):
    ctx = zmq.Context()
    s = ctx.socket(zmq.PUSH) 
    s.connect(host)
    return s

def random_data():
    return {
        '@class' : 'bnow_test'
        ,'@time' : str(int(time.time()))
        ,'name' : random.choice('abcdefghijklmnopqrstuvwxyz') * 3
        ,'length' : str(random.randint( 0 , 1000000 ))
    }
def choice_data():
    global bdata
    return random.choice(bdata)
    
    
def echohelp():
    print 'hello i\'m help'

if __name__ == "__main__":
    main()
