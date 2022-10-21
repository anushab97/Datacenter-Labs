import time
import sys
import grpc

import lab6_pb2
import lab6_pb2_grpc

import base64
import random

def doAdd(stub, debug=False):
    data = lab6_pb2.addMsg(a=5, b=10)
    response = stub.add(data)
    if debug:
        print("Response is: ", response.sum)

def doRawImage(stub, debug=False):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    data = lab6_pb2.rawImageMsg(img=img)
    response = stub.rawImage(data)
    if debug:
        print("Response is: ", response.width, response.height)

def doDotProduct(stub, debug=False):
    data = lab6_pb2.dotProductMsg()
    data.a.extend([random.random() for x in range(100)])
    data.b.extend([random.random() for x in range(100)])
    response = stub.dotproduct(data)
    if debug:
        print("Response is: ", response.dotproduct)

def doJsonImage(stub, debug=False):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    data = lab6_pb2.jsonImageMsg(img = base64.b64encode(img))
    response = stub.jsonImage(data)
    if debug:
        print("Response is: ", response.width, response.height)

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

channel = grpc.insecure_channel('{}:5000'.format(host))
stub = lab6_pb2_grpc.RestCompareStub(channel)
print("Running {} reps against".format(reps), host)

if cmd == 'add':
    start = time.perf_counter()
    for x in range(reps):
        doAdd(stub)
    t = ((time.perf_counter() - start)/reps)*1000
    print("Took", t, "ms per operation") 

elif cmd == 'rawImage':
    start = time.perf_counter()
    for x in range(reps):
        doJsonImage(stub)
    t = ((time.perf_counter() - start)/reps)*1000
    print("Took", t, "ms per operation")   

elif cmd == 'dotproduct':
    start = time.perf_counter()
    for x in range(reps):
        doDotProduct(stub)
    t = ((time.perf_counter() - start)/reps)*1000
    print("Took", t, "ms per operation")

elif cmd == 'jsonImage':
    start = time.perf_counter()
    for x in range(reps):
        doRawImage(stub)
    t = ((time.perf_counter() - start)/reps)*1000
    print("Took", t, "ms per operation")    


