import network
import time

class ClientTest(network.Client):
    def __init__(self, server_ip: str) -> None:
        super().__init__(server_ip, 5050)

    def ping(self):
        self.send("PING")
        time.sleep(3)

def main():
    c = ClientTest("25.55.1.84")
    while True:
        c.ping()

if __name__ == '__main__':
    main()