#Distributed Sort

Distributed Sort using n-way merge and ZeroMQ

##Installation

* Clone the repo on all the nodes using
  `git clone https://github.com/hardikj/Distributed_Sort.git`
* Use python2.7

##Configuration

* Edit configuration file config.py and add more nodes if needed
* run server.py on each node to run the server
* Run ` python master/client.py -s` on master node to press the trigger and start the sort

##What's under the Hood

As an example currently.
The sort is performed on the data stored per machine (Data/File1.txt, Data/File2.Txt etc) and the data is a set of integers that are globally unique. The N-way merge is performed on all the files and in the end, each machine have its own disjoint chunk of the globally sorted data (ie. machine[i].max < machine[i+1].min). There can be an arbitrary number of machines.

Feel free to add more examplle, fork, clone or collaborate.
