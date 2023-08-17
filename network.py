import socket
from _thread import *
import requests

def getLocalIp():
    return socket.gethostbyname(socket.gethostname())

class Server:
    def __init__(self, server_ip: str, server_port: int, device_number: int) -> None:
        self.devices = []

        self.server_ip = server_ip
        self.server_port = server_port
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.server_ip, self.server_port))
        except socket.error as e:
            print(str(e))
        self.server.listen(device_number)
    
    def threadedClient(self, client: socket.socket, addr) -> None:
        self.devices.append((client, addr))
        client.send(str.encode(f" -> CLIENT {addr[0]}:{addr[1]} CONNECTED TO {self.server_ip}:{self.server_port}"))
        reply = "NONE"
        while True:
            try:
                data = client.recv(2048)
                received = data.decode("utf-8")

                if not data:
                    print(f" -> DECONNECTION WITH: {addr[0]}:{addr[1]}")
                    self.devices.remove((client, addr))
                    break

                else:
                    print(f" -> {addr[1]} DATA RECEIVED : {received}")

                    reply = self.commandHandler(received, client, addr)

                    print(f" -> {addr[1]} DATA SENT : {reply}")

                client.send(str.encode(reply))

            except ConnectionResetError: 
                print(f" -> CONNECTION LOST TO: {addr[0]}:{addr[1]}")
                self.devices.remove((client, addr))
                client.close()
                break
    
    def commandHandler(self, received: str, client: socket.socket, addr) -> str:
        return "NONE"
    
    def serverTemp(self) -> None:
        start_new_thread(self.serverLoop, ())

    def serverOn(self) -> None:
        self.serverLoop()
    
    def serverLoop(self):
        print(f" -> SERVER LISTENING ON {self.server_ip}:{self.server_port}")
        while True:
            client, addr = self.server.accept()
            print(f" -> ACCEPTED CONNECTION FROM {addr[0]}:{addr[1]}")

            start_new_thread(self.threadedClient, (client, addr,))

class Client:
    def __init__(self, server_ip: str, server_port: int) -> None:
        self.server_ip = server_ip
        self.server_port = server_port
        self.addr = (self.server_ip, self.server_port)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            print("CONNECTED TO SERVER")
            return self.client.recv(2048).decode("utf-8")
        except:
            print("CONNECTION TO SERVER FAILED")
    
    def send(self, data):
        try:
            self.client.sendall(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
