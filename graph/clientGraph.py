from node import *
import socket
from bsonrpc import JSONRpc
import sys
from bsonrpc.exceptions import FramingError
from bsonrpc.framing import (
	JSONFramingNetstring, JSONFramingNone, JSONFramingRFC7464)


def connectToServer():
    try:
        # tcp client
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(('localhost', 50001))
        return clientSocket
    except:
        print("Error. Server not found")
        sys.exit()
        
def startConnection(s):
    rpc = JSONRpc(s,framing_cls=JSONFramingNone)
    server = rpc.get_peer_proxy()
    return server, rpc

#call function from server to increment every node from the tree/graph
def incrementValues(server, listTree):
    # Execute in server:
    incrementNodes = server.graphFromList(listTree)
    return incrementNodes
    
def closeConnection(rpc):
    rpc.close()
    
def createTree():
    #leaves from root
    leaf1 = node("leaf1")
    leaf2 = node("leaf2")
    root = node("root", [leaf1, leaf1, leaf2])
    return root

#receive a tree/graph object and convert it to a combination of lists
def createListFromTree(root):
    listTree = []
    listChildren = []
    for node in root.children:
        listChild = ["name", node.name, "val", node.val, "children", node.children]
        listChildren.append(listChild)
    listRoot = ["name", root.name, "val", root.val, "children", listChildren]
    listTree.append(listRoot)
    return listTree

#convert the list received from the server to a graph object made of nodes
def convertToObject(incrementedList, root):
    for listNode in incrementedList:
        print("list node", listNode)
        for node in root:
            node.name = listNode[1]
            print("name of node: ", node.name)
            node.val = listNode[3]
            print("value: ", node.val)
            if len(listNode[5]) != 0:
                print("Items inside ", node.name, ": ", listNode[2])
                convertToObject(listNode[5], node.children)
                
def printTree(root):
    print("--- Small tree from object:")
    root.show()

def printTreeList(listTree):
    print("\n--- Small tree with lists:")
    print(str(listTree)[1:len(listTree)-2])

def printTreeListIncremented(incrementNodes):
    print("\n--- Small tree incremented from JSON:")
    print(str(incrementNodes)[1:len(incrementNodes)-2])

def printTreeIncremented(root):
    print("\n--- Small tree incremented as object:")
    root.show()

def printJSONString(server):
    print("\n--- JSON String with graph and incremented values (exported as request.json):")
    print(server.writeOnFile())

def startProgram():
    socket = connectToServer()
    server, rpc = startConnection(socket)
    root = createTree()
    listTree = createListFromTree(root)
    incrementNodes = incrementValues(server, listTree)
    printTree(root)
    printTreeList(listTree)
    printTreeListIncremented(incrementNodes)
    convertToObject(incrementNodes, [root])
    printTreeIncremented(root)
    printJSONString(server)
    closeConnection(rpc)   # Closes the socket 's' also

startProgram()
