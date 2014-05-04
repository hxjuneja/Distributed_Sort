import zmq
import sys

context = zmq.Context()

# server 1
sock = context.socket(zmq.REQ)
sock.connect("tcp://172.16.86.44:5556")

# Open file
fo = open("data1.txt", "r+")
fo2 = open("dataA.txt", "w+")

data = fo.read().split("\n")

for i in data:
    field = i.split(" ")
    if len(field) > 1:
        if str(field[1]) == 'A':
             wf = " ".join(field)
             wf = wf + "\n"
             fo2.write(wf)
        else:
             wf = " ".join(field)
             wf = wf + "\n"
             sock.send("msg:%s"%wf)
             print("sent to node 2")
             
             print sock.recv()
