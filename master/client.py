from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import zmq

import config as c 

class ClientCode():

    def __init__(self):

        context = zmq.Context()

        # local node config
        self.id = 0
        config = c.config
        self.lconfig = config[self.id].itervalues().next()

        # extract config for other nodes
        self.nconfig = []
        for i in config:
            a = i.itervalues().next()
            ip = a["ip"]

            # connect to socket 
            sock = context.socket(zmq.REQ)
            sock.connect("tcp://%s"%ip)
            a["sock"] = sock
            self.nconfig.append(a)

        # Open files
        self.fo = open("../data/data1.txt", "r+")
        self.fo2 = open(self.lconfig["file"], "a+")

    def trigger(self):

        # Todo - convert this to Pub-Sub
        for i in self.nconfig:
            if i["id"]!=self.id:
                i["sock"].send("trig")
                print "sent trig to %d "%i["id"]
                m = i["sock"].recv()
                print m
        self.logic()

    def logic(self):

        data = self.fo.read().split("\n")
        for i in data:
            field = i.split(" ")
            if len(field) > 1:
                if str(field[1]) == self.lconfig["fval"]:
                    wf = " ".join(field)
                    wf = wf + "\n"
                    self.fo2.write(wf)
                else:
                    for i in self.nconfig:
                        if str(field[1]) == i["fval"]:
                            wf = " ".join(field)
                            wf = wf + "\n"
                            i["sock"].send("msg:%s"%wf)
                            print "sent to node %d"%i["id"]
                            print i["sock"].recv()


if __name__ == "__main__":
    c = ClientCode()
    c.trigger()
