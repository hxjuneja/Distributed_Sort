from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import zmq

import config

class ClientCode():
    
    def __init__(self):
        context = zmq.Context()

        # connect to server
        self.sock = context.socket(zmq.REQ)
        self.sock.connect("tcp://172.16.86.84:5555")

        # Open file
        self.fo = open("../data/data1.txt", "r+")
        self.fo2 = open("dataB.txt", "a+")

    def trigger(self):

        #Todo - convert this to pub-sub
        self.sock.send("trig")
        print self.sock.recv()
        self.logic()

    def logic(self):

        data = self.fo.read().split("\n")

        for i in data:
           field = i.split(" ")
           if len(field) > 1:
               if str(field[1]) == 'B':
                   wf = " ".join(field)
                   wf = wf + "\n"
                   self.fo2.write(wf)
               else:
                   wf = " ".join(field)
                   wf = wf + "\n"
                   self.sock.send("msg:%s"%wf)
                   print("sent ( %s )to node 1"%wf)
                   print self.sock.recv()


if __name__ == "__main__":
    c = ClientCode()
    c.logic()
