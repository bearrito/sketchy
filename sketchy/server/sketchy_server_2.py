import asyncio

from existence.bloom_filters import BloomFilter
from sketchy.protocols.messages_pb2 import BloomUpdate


class Viewthing(object):
    def __init__(self,mergeable,deser):
        self.mergeable = mergeable
        self.deser = deser

    def datagram_received(self, data):
        pass


class SketchyProtocol:
    def __init__(self, mergeable, peers=[]):
        self.mergeable=mergeable
        self.deser = deser

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):

        try:
            pass
        except:
            pass
        update = self.deser(data)
        self.mergeable.merge(update)

        print('Received %r from %s' % (data, addr))
        print('Send %r to %s' % (data, addr))
        self.transport.sendto(data, addr)

bloomFilter = BloomFilter(10000, 9)
loop = asyncio.get_event_loop()

def protocol_factory():
    return SketchyProtocol(bloomFilter, bloom_update_deserializer)
def bloom_update_deserializer(message: str):

    update = BloomUpdate()
    update.ParseFromString(message)
    return update


print("Starting UDP server")
# One protocol instance will be created to serve all client requests
listen = loop.create_datagram_endpoint(
    protocol_factory, local_addr=('127.0.0.1', 9999))
transport, protocol = loop.run_until_complete(listen)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass