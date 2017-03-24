# streamlayer_ws
A websocket server (created using Autobahn|Python) that emits Esri json.   
The client and server were adapted from the [Autobahn|Python example code](https://github.com/crossbario/autobahn-python/tree/master/examples/asyncio/websocket/slowsquare).  
The sample map was adapted from [this blog post] (https://geonet.esri.com/blogs/nicogis/2014/08/05/websocket-with-streamlayer).

### Install and run   
#### On Linux with conda:
Run the following commands after cloning the repository:
```shell
$ conda env create
$ source activate websocket
$ python server.py
```
#### On all other systems:
(You'll still need pip and Python 3.4+, though)
```shell
$ pip install -r requirements.txt
$ python server.py
```

### Other resources
[WebSocket specification] (https://html.spec.whatwg.org/multipage/comms.html#network)  
[Autobahn|Python WebSocket programming tutorial] (http://autobahn.ws/python/websocket/programming.html)  
[WAMP] (http://wamp-proto.org/)  
