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
file1 = lconfig["file"]

counter = 0

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://*:%s"%port)
print("binding to port %s"%port)

fo = open("../data/FILE2.TXT", "r+") 
data = fo.read().split("\n")
sorted_data = data
sorted_data.sort(key = lambda x: int(x.split(" ")[2]))

while True:
    message = sock.recv()
    message = message.split(":")

    #prepare this node for alfa sort check
    if message[0] == "trig":
        print("got it")
        os.system("python client1.py")
        sock.send("started")

    #on msg add the content to file
    elif message[0] == "msg":
        fo = open(file1, "a+")
        content = message[1]
        fo.write(content)
        sock.send("done")
        print "done"
        fo.close()

    #prepare this node for numeric sorting
    elif message[0] == "sortReady":
        #extract and sort the data
        counter = 0
        #initiate the iterator
        sock.send("node is ready for sort\n--------------")

    #send back requested record
    elif message[0] == "keyPlease":
        if counter==len(sorted_data):
            msg = "end"
        else:
            msg = sorted_data[counter]
        sock.send(msg)

    #increament counter
    elif message[0] == "inc":
        counter = counter + 1
        sock.send("ok")

    elif message[0] == "slave":
        sock.send("done")
        counter = int(message[1])

    elif message[0] == "takeOver":
        sock.send("done")
        #os.system(os.P_DETACH, "python client1.py -s %d"%counter)
        from subprocess import Popen
        Popen(["python", "client1.py", "-s" , str(counter)])
    else:
        print("Please send again!!")
        sock.send("again")
