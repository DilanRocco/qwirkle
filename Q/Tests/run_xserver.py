import sys

from jsonstream import loads

from Q.Server.connection import Connection
from Q.Server.server import Server

from Q.Util.util import Util
address = "localhost"


def main():
    stream = loads(sys.stdin.read())
    config = Util().convert_jserver_config_to_server_config(next(stream))
    TCPServerInstance = Server(config, (address, get_port()), Connection)
    TCPServerInstance.serve_forever()
    sys.exit()

def get_port() -> int:
    try:
        return int(sys.argv[1])
    except Exception:
        raise Exception("no port number provided")


if __name__ == "__main__":
    main()
