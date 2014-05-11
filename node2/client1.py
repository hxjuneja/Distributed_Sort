from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import zmq

import config as c

class ClientCode():
    
    def __init__(self):
        context = zmq.Context()

        # local node config
        self.id = 1
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

        #Todo - convert this to pub-sub
        self.sock.send("trig")
        print self.sock.recv()
        self.alfaSortLogic()

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
                            print "sent to node %d"%i["id"]
                            print i["sock"].recv()

    def numSortLogic(self, counter=None):
    '''
        Main logic for n-way merge
        
        1. Sort locally
        2. Extract all the keys from other nodes
        3. Create a priority heap
        4. Pull a lowest value and write it to the file
        5. if the limit is over, send a message to other node to start 1 
    '''

        keys = []
        lc = 0
        records = []
        limit = 3
        if counter is None:
            counter = 0

        # Extract key from local file
        data = self.fo.read().split("\n")
       
        sorted_data = data.sort(key = lambda x: int(x.split(" ")[4]))

        while lc<=limit:
            field = sorted_data[counter].split(" ")
            records.append(sorted_data[counter])
            keys.append(field[4])

            # Extract keys from other nodes
            for i in self.nconfig:
                if i["id"]!=self.id:
                    i["sock"].send("keyPlease")
                    print "asked for key from node %d "%i["id"]
                    m = i["sock"].recv()
                    field = m.split(" ")
                    records.append(m)
                    keys.append(field[4])
            
            # create a priority heap out of keys
            heap = MinMaxHeap()
            for i in keys:
                heap.insert(i)

            # Pull the lowest value
            lowest = heap.extract_min()

            for i in range(len(keys)):
                if keys[i] == lowest:
                    break
            
            # increment counter of node[i] and write to file
            if i == self.id:
                counter = counter + 1
            else:
                self.nconfig[i]["sock"].send("inc")
                self.nconfig[i]["sock"].recv()
            
            fo2.write(sorted_data[i])
            lc = lc + 1

        #TODO - create handler for heap transfer
        if lc<=limit:
            # send a message to next node to take over
            self.nconfig[self.id+1]["sock"].send("takeOver")
            self.nconfig[self.id+1]["sock"].recv()
            self.nconfig[self.id]["sock"].send("slave:%s"i)


if __name__ == "__main__":
    c = ClientCode()
    if "-s" in argv:
        c.numSortLogic(int(argv[3]))
    else:
        c.alfaSortLogic()