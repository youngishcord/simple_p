from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ReconnectingClientFactory as ClFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
import json

test_1 = {
    "name": "FRIENDS",
    "year": 1994
}


test_2 = {
    "name": "BBT",
    "year": 2000
}

test_3 = {
    "func": "add",
    "body":{
        "name": "FRIENDS",
        "year": 1994
    }
}

test_3 = {"func": "add","body":{"_id": 1, "name": "test","year": 1234}}#####добавить можно что угодно и как угодно в body
test_4 = {"func": "del","body":{"name": "BBT","year": 2000}}###пример, можно удолять по имени, году, id или по комбинации

class Client(Protocol):
    def __init__(self):
        reactor.callInThread(self.send_data)

    def dataReceived(self, data):
        data = data.decode()
        print(data)

    def connectionMade(self):
        pass

    def send_data(self):
        while True:
            self.transport.write(input().encode())

class ClientFactory(ClFactory):
    def buildProtocol(self, addr):
        return Client()

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        ClFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print(reason)
        ClFactory.clientConnectionLost(self, connector, reason)


if __name__ == '__main__':
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 2345)
    endpoint.connect(ClientFactory())
    reactor.run()



