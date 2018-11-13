# minimalistic server example from 
# https://github.com/seprich/py-bson-rpc/blob/master/README.md#quickstart

import socket
from node import *
from bsonrpc import JSONRpc
from bsonrpc import request, service_class
from bsonrpc.exceptions import FramingError
from bsonrpc.framing import (
	JSONFramingNetstring, JSONFramingNone, JSONFramingRFC7464)
import sys


# Class providing functions for the client to use:
@service_class
class ServerServices(object):
  
    global graph
    graph.name = ""
    graph.children = []
    graph.val = 0
    
    @request
    #increment the value of every node of a graph
    def graphFromList(self, root):
        self.graph.name = root[1]
        self.graph.val = root[3]
        self.graph.children = self.graphFromListChildren(self, root[5])
        return self.graph

    @request
    #convert the tree/graph made of lists to a JSON string and write it into a file
    def writeOnFile(self):
        with open("request.json", "w") as jsonFile:
            graphString = str(self.graph)
            graphString = graphString.replace("u", "")
            graphString = graphString.replace("[", "{")
            graphString = graphString.replace("]", "}")
            graphString = graphString.replace("'name',", "'name':")
            graphString = graphString.replace("'val',", "'val':")
            graphString = graphString.replace("'children',", "'children':")
            graphString = graphString.replace("'children': {{", "'children': [{")
            graphString = graphString.replace("{}", "[]")
            graphString = graphString[1:len(graphString)-1]
            graphString = graphString.replace("}}}", "}]}")
            jsonFile.write(graphString)
            jsonFile.close()
        return graphString

    @request
    def graphFromListChildren(self, children):
        for node in children:
            node.name = node[1]
            self.graph.val = rootnodenode[3]
            self.graph.children = root[5]
            print(node)
            if len(node[5]) != 0:
                self.graphFromListChildren(self, node[5])

def listen():
    # Quick-and-dirty TCP Server:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('localhost', 50001))
    serverSocket.listen(10)
    print("Server listening...")
    return serverSocket

def acceptConnection(serverSocket):
    while True:
        s, _ = serverSocket.accept()
        # JSONRpc object spawns internal thread to serve the connection.
        JSONRpc(s, ServerServices(),framing_cls=JSONFramingNone)
        sys.exit()


serverSocket = listen()
acceptConnection(serverSocket)
