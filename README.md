Distributed Sort
================

Distributed Sort using n-way merge and ZeroMQ

Installation
============

* Clone the repo
* Fill the configuration file config.py and add more nodes if needed
* Clone the repo in master node and run master/server.py to run the server on master node
* Similarly clone the repo in other nodes and use node*/server.py to run the server on other nodes
* Run ` python master/client.py -s` on master node to press the trigger and start the sort


