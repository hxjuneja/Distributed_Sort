import zmq
import os

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://*:5556")

while True:
    message = sock.recv()
    message = message.split(":")

    if message[0] == "trig":
        print("got it")
        os.system("python client1.py")
        sock.send("started")

    elif message[0] == "msg":
        fo = open("dataC.txt", "a+")
        content = message[1]
        fo.write(content)
        sock.send("done")
        print "done"
        fo.close()

    else:
        print("Please send again!!")
        sock.send("again") 
