import json
import socketserver
import threading
from threading import Timer
from typing import Any, Callable, Tuple, Dict

from Q.Referee.ref_with_config import RefereeWithConfig
from Q.Referee.referee_config import RefereeConfig
from Q.Server.player import ProxyPlayer
from Q.Server.server_config import ServerConfig


class Server(socketserver.ThreadingTCPServer):
    """
    represents the server that holds all of the connectoions of players and starts the game
    """
    def __init__(self, server_config: ServerConfig, server_address: Tuple[str, int],
                 RequestHandlerClass: Callable[..., socketserver.BaseRequestHandler]):
        super().__init__(server_address, RequestHandlerClass)
        self.__slots__ = "names, server_config"
        self.daemon_threads = True
        self.server_config = server_config
        self.names = {}
        self.server_tries = self.server_config.server_tries

    def serve_forever(self, poll_interval=0.5):
        self.t = Timer(self.server_config.server_wait, self.check_players)
        self.t.daemon = True
        self.t3 = threading.Thread(target=self.should_start_game)
        self.t3.daemon = True
        self.t.start()
        self.t3.start()
        super().serve_forever(poll_interval)

    def start_game(self, names: Dict, ref_config: RefereeConfig):
        """
        start the Q game with some given config and player names mapped to connections
        :param names: the string names mapped to connections
        :param ref_config: the config of the referee
        """
        self.t.cancel()
        ref = RefereeWithConfig(ref_config)
        player_list = [ProxyPlayer(name, conn) for name, conn in names.items()]
        if not ref_config.quiet:
            print(player_list)
        res = ref.main(player_list)
        print(json.dumps(res))
        self.shutdown()
        self.server_close()

    def check_players(self):
        """
        checks if the length of the players is greater than two, if so starts the game else calls some timer to run again.
        """

        if len(self.names) >= 2:
            self.start_game(self.names, self.server_config.ref_spec)
            return
        self.timer()

    def should_start_game(self):
        """
        continues to check if there are four players to start the game
        """

        while True:
            if len(self.names) == 4:
                if not self.server_config:
                    print("Starting game with four players")
                self.start_game(self.names, self.server_config.ref_spec)

    def timer(self):
        """
        a method that is called after each successive server-tries call.
        """

        self.server_tries -= 1
        if self.server_tries == 0:
            end_result = json.dumps([[], []])
            print(end_result)
            self.shutdown()
            self.server_close()
        else:
            Timer(self.server_config.server_wait, self.check_players).start()

