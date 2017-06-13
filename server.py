from tornado import gen, ioloop
from tornado.netutil import bind_sockets
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError


class DanmakuServer(TCPServer):
    def __init__(self):
        super().__init__()

        self.conn_list = list()

    @gen.coroutine
    def handle_stream(self, stream, address):

        while True:
            print(stream, ' ', address)
            info = {'stream': stream,
                    'address': address}
            try:
                data = yield stream.read_until(b"\n")
                stri = data.decode('utf-8')

                if stri[:-1] == 'conn':
                    self.conn_list.append(info)
                    yield stream.write('accept'.encode('utf-8'))

                elif stri[:5] == 'ika__':
                    yield stream.write((stri[5:] + 'sucess').encode('utf-8'))
                    for item in self.conn_list:
                        yield item['stream'].write(stri.encode('utf-8'))

            except StreamClosedError:
                if info in self.conn_list:
                    print('before', self.conn_list)
                    self.conn_list.remove(info)
                    print('after', self.conn_list)
                break

sockets = bind_sockets(8888)
server = DanmakuServer()
server.add_sockets(sockets)
ioloop.IOLoop.current().start()
