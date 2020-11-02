import asyncio

met_store = {}

class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, str):
        comm = str.strip("\n").split(" ")
        if comm[0] == "get":
            self.get(comm[1])
        elif comm[0] == "put":
            self.put(comm[1], comm[2], comm[3])
        else:
            return 'error\nwrong command\n\n'

    def get(self, key):
        ans = "ok\n"
        if key == "*":
            if met_store == {}:
                return "ok\n\n"
            for key, values in met_store.items():
                for value in values:
                    ans = ans + key + " " + value[1] + " " + value[0] + "\n"
        else:
            if key in met_store:
                for value in met_store[key]:
                    ans = ans + key + " " + value[1] + " " + value[0] + "\n"
        return ans + "\n"

    def put(self, key, value, timestamp):
        if key in met_store:
            met_store[key].append(tuple(timestamp, value))
        else:
            met_store[key] = []
            met_store[key].append(tuple(timestamp, value))
            met_store[key].sort(key=lambda tup: tup[0])
        return "ok\n\n"

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
    ClientServerProtocol,
    host, port
)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

run_server("127.0.0.1", 8888)