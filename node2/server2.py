import os
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import zmq

import config

# ZeroMQ Context
context = zmq.Context()

id = 1
lconfig = config.config[id]
lconfig = lconfig.itervalues().next()
port = lconfig["port"]
file = lconfig["file"]

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://*:%s"%port)
print("binding to port %s"%port)

while True:
    message = sock.recv()
    message = message.split(":")

    if message[0] == "trig":
        print("got it")
        os.system("python client1.py")
        sock.send("started")

    elif message[0] == "msg":
        fo = open(file, "a+")
        content = message[1]
        fo.write(content)
        sock.send("done")
        print "done"
        fo.close()

    else:
        print("Please send again!!")
        sock.send("again") 
