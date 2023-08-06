import asyncio
import sys
import thriftpy

from aiothrift.server import make_server

pingpong_thrift = thriftpy.load('tests/test.thrift', module_name='test_thrift')


class Dispatcher:
    def ping(self):
        return "pong"

    async def add(self, a, b):
        return a + b


loop = asyncio.get_event_loop()

server = loop.run_until_complete(
    make_server(pingpong_thrift.Test, Dispatcher(), ('127.0.0.1', 6000), loop=loop, timeout=10))

print('server is listening on host {} and port {}'.format('127.0.0.1', 6000))
sys.stdout.flush()

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
