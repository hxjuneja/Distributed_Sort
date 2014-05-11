from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import zmq

import config as c 
from heap import *

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
        self.fo = open("../data/FILE1.TXT", "r+")
        self.fo2 = open(self.lconfig["file"], "a+")

    def alfaSortLogic(self):

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
                            print "sent to node %d"%(i["id"])
                            print i["sock"].recv()

    def trigger(self):

        # Todo - convert this to Pub-Sub

        trigMessage = "trig"

        if "-s" in sys.argv:
            trigMessage = "sortReady"

        for i in self.nconfig:
            if i["id"]!=self.id:
                i["sock"].send(trigMessage)
                print "sent trig to %d "%i["id"]
                m = i["sock"].recv()
                print m

        if "-s" in sys.argv:
            self.numSortLogic()
        else:
            self.alfaSortLogic()


    def numSortLogic(self):
        '''
            Main logic for n-way merge

            1. Sort locally
            2. Extract all the keys from other nodes
            3. Create a priority heap
            4. Pull a lowest value and write it to the file
            5. if the limit is over, send a message to other node to start 1
        '''

        limit = 1000
        
        keys = []
        counter = 0
        lc = 0
        records = []

        # Extract key from local file
        data = self.fo.read().split("\n")
        sorted_data = data
        sorted_data.sort(key = lambda x: int(x.split(" ")[2]))

        while lc<limit:

            keys = []
            records = []
 
            # Extract keys from other nodes
            for i in self.nconfig:
                if i["id"]!=self.id:
                    i["sock"].send("keyPlease")
                    print "asked for key from node %d "%i["id"]
                    m = i["sock"].recv()
                    if m == "end":
                        m = None
                        records.append(None)
                        keys.append(m)
                    else:
                        field = m.split(" ")
                        records.append(m)
                        keys.append(int(field[2]))
                else:
                    field = sorted_data[counter].split(" ")
                    records.append(sorted_data[counter])
                    keys.append(int(field[2]))

            # Creates a priority heap out of keys
            heap = MinMaxHeap()
            for i in keys:
                if i == None:
                    heap.insert(i)
                else:
                    heap.insert(i)


            # Pull the lowest value
            lowest = None
            while lowest is None:
                lowest = heap.extract_min()

            # Find node no (i) using lowest value
            for i in range(len(keys)):
                if keys[i] == lowest:
                    break

            # Increment counter of node[i] and write to file
            if i == self.id:
                counter = counter + 1
            else:
                self.nconfig[i]["sock"].send("inc")
                self.nconfig[i]["sock"].recv() == "end"

            m = records[i]

            self.fo2.write(m+"\n")
            lc = lc + 1

        if lc==limit:

            # Send Master(this) node to update counter and start listning 
            self.nconfig[self.id]["sock"].send("slave:%s"%counter)
            self.nconfig[self.id]["sock"].recv()

            # Send a message to next node to take over
            print "--------------\n handling to node %d"%(self.id+1)
            self.nconfig[self.id+1]["sock"].send("takeOver")
            self.nconfig[self.id+1]["sock"].recv()

if __name__ == "__main__":
    c = ClientCode()
    c.trigger()
