import zmq

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://*:5556")

fo = open("dataB.txt", "w+")

# Run a simple "Echo" server
while True:
    message = sock.recv()
    message = message.split(":")

    if message[0] == "msg":
        content = message[1]
        fo.write(content)
        sock.send("done")
        print "done"
    else:
        print("Please send again!!")
        sock.send("again") 
