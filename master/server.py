from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import zmq

import config

# ZeroMQ Context
context = zmq.Context()

id = 0
lconfig = config.config[id]
lconfig = lconfig.itervalues().next()
port = lconfig["port"]
file = lconfig["file"]

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://*:%s"%port)

counter = 0
fo = open("../data/data1.txt", "r+")
data = fo.read().split("\n")
sorted_data = data
sorted_data.sort(key = lambda x: int(x.split(" ")[4]))

while True:
    message = sock.recv()
    message = message.split(":")
    print message

    if message[0] == "msg":
        fo = open(file, "a+")
        content = message[1]
        fo.write(content)
        sock.send("done")
        print "done"
        fo.close()

    #send back requested record
    elif message[0] == "keyPlease":
        if counter>len(sorted_data)-1:
            msg = "end"
        else:
            msg = sorted_data[counter]
        sock.send(msg)

    elif message[0] == "slave":
        counter = int(message[1])

        #extract and sort the data
        sock.send("done")

    #increament counter
    elif message[0] == "inc":
        counter = counter + 1
        sock.send("ok")

    else:
        print("Please send again!!")
        sock.send("again") 