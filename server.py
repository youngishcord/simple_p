from numpy import delete
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
import pymongo
import json

client = pymongo.MongoClient('localhost', 27017)

db = client['simple_test']

collection = db['simple']

class Server(Protocol):
    def __init__(self, db, collection):
        self.db = db
        self.collection = collection
        print(self.db)
        print(self.collection)

    def connectionMade(self):
        print('New connection')
        self.transport.write('Hellow from server'.encode())
        
        
    def dataReceived(self, data):
        data = data.decode()
        data = json.loads(data)
        if data["func"] == "add":
            self.insert_doc(data["body"])
        elif data["func"] == "del":
            self.delete_doc(data["body"])

    
    def insert_doc(self, data):
        return self.collection.insert_one(data).inserted_id


    def delete_doc(self, data):
        return self.collection.delete_one(data)

    def connectionLost(self, reason = connectionDone):
        return print(reason)


class ServerFactory(ServFactory):
    def __init__(self, db, collection):
        self.db = db
        self.collection = collection

    def buildProtocol(self, addr):
        return Server(db, collection)



if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 2345)
    endpoint.listen(ServerFactory(db, collection))
    reactor.run()