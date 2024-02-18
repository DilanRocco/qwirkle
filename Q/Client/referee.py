import json
import sys

from Q.Client.client import Client
from Q.Player.player import Player
from Q.Player.player_funcs import PlayerFuncs
from Q.Util.util import Util

VOID = 'void'
class RefereeProxy:
    """
    Represents the proxy ref
    """
    def __init__(self, client: Client, player: Player):
        self.client = client
        self.player = player

    def listen(self):
        """
        listens for data, performs some function on that data, and sends that processed data back to the server
        """
        while True:
            data = self.client.recv()
            if data:
                ret = self.process(data)
                self.client.send(ret)
                if self.close_thread_after_win(data):
                    sys.exit()

    def close_thread_after_win(self, data):
        """
        close the thread if the win method is called
        :param data: the data given over the socket
        :return:
        """
        data = json.loads(data)
        func = data[0]
        if func == PlayerFuncs.WIN.value:
            return True


    def process(self, data: str) -> str:
        data = json.loads(data)
        func = data[0]
        args = data[1]

        if func == PlayerFuncs.WIN.value:
            return self.call_win(args)
        if func == PlayerFuncs.SETUP.value:
            return self.call_setup(args)
        if func == PlayerFuncs.TAKE_TURN.value:
            return self.call_take_turn(args)
        if func == PlayerFuncs.NEW_TILES.value:
            return self.call_new_tiles(args)

    def call_take_turn(self, args) -> str:
        ps = Util().convert_jpub_to_player_state(args[0])
        try:
            turn = self.player.take_turn(ps)
            return json.dumps(Util().convert_turn_to_j_turn(turn))
        except Exception as e:
            return "bad player"


    def call_new_tiles(self, args) -> str:
        tiles = Util().convert_jtiles_to_tiles(args)
        try:
            self.player.new_tiles(tiles)
            return VOID
        except Exception as e:
            return "bad player"


    def call_setup(self, args) -> str:
        ps = Util().convert_jpub_to_player_state(args[0])
        tiles = Util().convert_jtiles_to_tiles(args[1])
        try:
            self.player.setup(ps, tiles)
            return VOID
        except Exception as e:
            return "bad player"

    def call_win(self, args) -> str:
        b = args[0]
        try:
            self.player.win(b)
            return VOID
        except Exception as e:
            return "bad player"

