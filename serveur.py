import network

class ServeurTest(network.Server):
    def __init__(self) -> None:
        super().__init__(network.getLocalIp(), 9000, 2)

def main():
    s = ServeurTest()
    s.serverOn()

if __name__ == '__main__':
    main()