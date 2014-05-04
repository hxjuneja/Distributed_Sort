import zmq

context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://*:5555")

# Run a simple "Echo" server
while True:
    message = sock.recv()
    print("got:%s "%message)
    
    sock.send("hey, repling ya!!")
    print "Sent: " + message
