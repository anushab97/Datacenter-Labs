#!/usr/bin/env python3

from concurrent import futures
from PIL import Image
import io
import base64
import grpc
import lab6_pb2
import lab6_pb2_grpc
import numpy as np

class Server(lab6_pb2_grpc.RestCompareServicer):

    def add(self, request, context):
        sum = request.a + request.b
        return lab6_pb2.addReply(sum=sum)

    def rawImage(self, request, context):
        ioBuffer = io.BytesIO(request.img)
        img = Image.open(ioBuffer)
        return lab6_pb2.imageReply(width = img.size[0], height = img.size[1])

    def dotproduct(self, request, context):
        sum = np.dot(request.a, request.b)
        return lab6_pb2.dotProductReply(dotproduct=sum)

    def jsonImage(self, request, context):
        rawimg = base64.b64decode(request.img)
        ioBuffer = io.BytesIO(rawimg)
        img = Image.open(ioBuffer)
        return lab6_pb2.imageReply(width = img.size[0], height = img.size[1])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_RestCompareServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:5000')
    server.start()
    server.wait_for_termination()

serve()
