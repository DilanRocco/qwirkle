import json
import socketserver
from threading import Timer
from typing import Any

from Q.Server.states import States


class Connection(socketserver.StreamRequestHandler):
    """
    Represents a single connection between a client over the wire
    """
    def __init__(self, request: Any, client_address: Any, server: socketserver.BaseServer):
        self.latest = ""
        self.state = States.SIGNUP
        self.server = server
        self.quiet = self.server.server_config.quiet
        self.check_for_name_thread = Timer(self.server.server_config.server_wait, self.check_for_name)
        super().__init__(request, client_address, server)

    def check_for_name(self):
        """
        checks if there was a name given over the wire and changes some state if so.
        """

        if self.state == States.SIGNUP:
            self.state = States.NO_NAME_GIVEN

    def get_latest_message(self):
        """
        returns the latest message
        """
        new = self.latest
        if new:
            self.latest = ""
        return new

    def write_method(self, func, args):
        """
        writes this message over the wire for this specific connection
        :param func: the func you are writing about
        :param args: the args you are writing about
        """
        data = json.dumps([func, args])
        if not self.quiet:
            print(data, "writing")
        self.wfile.write(data.encode())

    def handle(self):
        """
        redefined method of stremRequestHandler that is called when data is recieved.
        """

        while True:
            msg = self.rfile.readline().strip().decode()
            if msg and self.state == States.SIGNUP and msg not in self.server.names.keys():
                if not self.quiet:
                    print("CONNECTION MADE")
                self.server.names[msg] = self
                self.state = States.RUNGAME
                continue

            if msg and self.state == States.RUNGAME:
                self.latest = msg
                if not self.quiet:
                    print(msg, "received")
