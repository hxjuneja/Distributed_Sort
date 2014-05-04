import zmq
import sys

context = zmq.Context()

# connect to server
sock = context.socket(zmq.REQ)
sock.connect("tcp://172.16.86.84:5555")

# Open file
fo = open("../data/data1.txt", "r+")
fo2 = open("dataB.txt", "w+")

data = fo.read().split("\n")

for i in data:
    field = i.split(" ")
    if len(field) > 1:
        if str(field[1]) == 'B':
             wf = " ".join(field)
             wf = wf + "\n"
             fo2.write(wf)
        else:
             wf = " ".join(field)
             wf = wf + "\n"
             sock.send("Sending")
             print("sent to client one")
             print sock.recv()
