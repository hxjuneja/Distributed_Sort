import zmq
import sys

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REQ)
sock.connect("tcp://localhost:5555")

sock2 = context.socket(zmq.REQ)
sock2.connect("tcp://localhost:5556")

# Send a "message" using the socket
sock.send("hello")
print("sent to client one")

sock2.send("hellosh")
print("sent to client two")

# Recive what you get back
print sock.recv()
print("recieve from one")

print sock2.recv()
print("recieved from two")
