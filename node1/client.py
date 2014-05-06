import zmq
import sys


class ClientCode():

    def __init__(self):

        context = zmq.Context()

        # connect to socket 
        self.sock = context.socket(zmq.REQ)
        self.sock.connect("tcp://localhost:5556")

        # Open files
        self.fo = open("../data/data1.txt", "r+")
        self.fo2 = open("dataA.txt", "a+")

    def trigger(self):

        #Todo - convert this to Pub-Sub
        self.sock.send("trig")
        print "sent trig"
        m = self.sock.recv()
        print m
        self.logic()

    def logic(self):

        data = self.fo.read().split("\n")
        for i in data:
            field = i.split(" ")
            if len(field) > 1:
                if str(field[1]) == 'A':
                    wf = " ".join(field)
                    wf = wf + "\n"
                    self.fo2.write(wf)
                else:
                    wf = " ".join(field)
                    wf = wf + "\n"
                    self.sock.send("msg:%s"%wf)
                    print("sent to node 2")
                    print self.sock.recv()


if __name__ == "__main__":
    c = ClientCode()
    c.trigger()
