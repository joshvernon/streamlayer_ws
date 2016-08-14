###############################################################################
#
# The MIT License (MIT)
#
# Original work Copyright (c) Tavendo GmbH
# Modified work Copyright (c) 2016 Joshua David Vernon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import collections
import json
import random
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
     WebSocketServerFactory

try:
    import asyncio
except ImportError:
    # Trollius >= 0.3 was renamed
    import trollius as asyncio

def create_random_esri_json_feature():
    rand_lat = random.uniform(-55.0, 62.0)
    rand_long = random.uniform(-180.0, 180.0)
    point_geom = (("x", rand_long),
                  ("y", rand_lat),
                  ("spatialReference", {"wkid":4326}))
    point_geom = collections.OrderedDict(point_geom)
    attrs = tuple([("some_attr{}".format(i), "value{0}".format(i)) for i in range(5)])
    attrs = collections.OrderedDict(attrs)
    feature = (("geometry", point_geom),
               ("attributes", attrs))
    feature = collections.OrderedDict(feature)
    return feature

class EsriJsonServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        
    @asyncio.coroutine
    def onOpen(self):
        print("WebSocket connection open.")
        # Start emitting features every second
        while True:
            features = [create_random_esri_json_feature()
                        for i in range(random.randint(1, 15))]
            payload = json.dumps(features, ensure_ascii = False).encode('utf8')
            self.sendMessage(payload, isBinary=False)
            yield from asyncio.sleep(1)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Result received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

if __name__ == '__main__':

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = EsriJsonServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '127.0.0.1', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
