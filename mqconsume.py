#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013 
## File : xzb_mq_tool.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-02-14>
## Updated: Time-stamp: <2013-02-26 15:23:15>
##-------------------------------------------------------------------
import pika
import sys
import time
import commands
import json
import os

filename = None
fb = None

def insert_message(queue_name, message , mq_host):
   print "Insert into queue(" + queue_name + "). msg:" + message
   connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host))
   channel = connection.channel()

   channel.queue_declare(queue=queue_name, durable=True)

   channel.basic_publish(exchange='',
                         routing_key=queue_name,
                         body=message,
                         properties=pika.BasicProperties(
                             delivery_mode = 2, # make message persistent
                         ))
   print " [x] Sent %r" % (message,)
   connection.close()

def get_message(queue_name , mq_host):
   connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host))
   channel = connection.channel()

   channel.queue_declare(queue=queue_name, durable=True)
   print ' [*] Waiting for messages. To exit press CTRL+C'

   channel.basic_qos(prefetch_count=1)
   channel.basic_consume(callback, queue=queue_name)

   channel.start_consuming()

def get_queue_name(message):
   list1 = message.split(" ")
   for item in list1:
       if item.find("http") == 0:
           list2 = item.split("/")
           return "snake_worker-shell#1#d1#" + list2[2]
   print "Error: fail to get_queue_name from message:" + message
   sys.exit(-1)
   return ""

def callback(ch, method, properties, body):
    global filename , fb
    bdata = body.encode('utf-8')+"\n"
    checkfile( filename , fb )
    fb.write(bdata)
    ch.basic_ack(delivery_tag = method.delivery_tag)

def thisfile():
    maxfilename = 0
    for filename in os.listdir('.'):
        if filename.endswith('.bdata'):
            thisfilename = int(filename[5:-6])
            if thisfilename > maxfilename:
                maxfilename = thisfilename
    return 'bdata'+ str(maxfilename) +'.bdata'

def nextfile():
    return 'bdata'+str(int( thisfile()[5:-6]) +1) + '.bdata'

def checkfile(filename1, fb1):
    global filename , fb
    if os.path.getsize(filename1) > 1024*1024*10 :
        fb1.close()
        filename = nextfile()
        fb = open( filename , 'w+' )
    else:
        filename = filename1
        fb = fb1

# xzb_mq_tool.py insert sudo xzb_fetch_url.sh --fetch_url http://haowenz.com/a/bl/2013/2608.html --dst_dir webcrawler_raw_haowenz
# xzb_mq_tool.py get snake_worker-shell#1#d1#haowenz.com
if __name__ == "__main__":
   mq_host = sys.argv[1]
   fname = thisfile()
   fp = open(fname , 'w+')
   checkfile(fname , fp)
   if sys.argv[2] == "insert":
       message = " ".join(sys.argv[3:])
       queue_name = get_queue_name(message)
       insert_message(queue_name, message ,mq_host)
   else:
       if sys.argv[2] == "get":
           queue_name = sys.argv[3]
           get_message(queue_name , mq_host)
       else:
           print "Error unknown command:" + str(sys.argv)
