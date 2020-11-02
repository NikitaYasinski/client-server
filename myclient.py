import socket
import time


class ClientError(Exception):
    pass

class Client:
    def __init__(self, host, port, timeout = None):
        self.sock = socket.socket()
        self.sock.connect((host, port))


    def get(self, key):
        try:
            self.sock.sendall(f"get {key}\n".encode("utf-8"))
            data = self.sock.recv(1024).decode("utf-8")
            if data == "ok\n\n":
                return {}
            data_list = data.split("\n")
            for i in range(2):
                data_list.pop()
            data_list.pop(0)
            d = {}
            l = []
            for i in data_list:
                key_list = i.split(" ")
                d[key_list[0]] = []
            for i in data_list:
                key_list = i.split(" ")
                d[key_list[0]].append((int(key_list[2]), float(key_list[1])))
                d[key_list[0]].sort(key=lambda tup: tup[0])
        except IndexError:
            raise ClientError(Exception)


        if key == "*":
            return d
        else:
            return {key : d[key]}


    def put(self, key, value, timestamp = None):
        if timestamp is None:
            timestamp = int(time.time())
        self.sock.sendall(f"put {key} {value} {timestamp}\n".encode("utf-8"))
        data = self.sock.recv(1024).decode("utf-8")
        if data[0:3] != "ok\n":
            raise ClientError(Exception)




