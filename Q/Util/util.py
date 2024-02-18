import json
from collections import defaultdict
from typing import Set, Dict, List, Union

from Q.Client.client_config import ClientConfig
from Q.Common.player_game_state import PlayerGameState
from Q.Common.referee_state_config import RefereeStateConfig
from Q.Common.rulebook import Rulebook
from Q.Common.game_state import GameState
from Q.Common.Board.pos import Pos
from Q.Common.map import Map
from Q.Common.Board.tile import Tile
from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Player.cheat_player import CheatPlayer
from Q.Player.dag import Dag
from Q.Player.ldasg import LDasg
from Q.Player.loop_player import LoopPlayer
from Q.Player.player import Player
from Q.Player.public_player_data import PublicPlayerData
from Q.Player.strategy import PlayerStrategy
from Q.Player.in_housep_player import InHousePlayer
from Q.Player.player_state import PlayerState
from Q.Player.turn import Turn
from Q.Player.turn_outcome import TurnOutcome
from Q.Player.exn_player import ExnPlayer
from Q.Referee.pair_results import Results
from Q.Referee.referee_config import RefereeConfig
from Q.Server.server_config import ServerConfig


class Util:
    """
    # Represents a utility class used mainly for json parsing
    """
    def convert_jserver_config_to_server_config(self, jserver_config) -> ServerConfig:
        port = jserver_config["port"]
        server_tries = jserver_config["server-tries"]
        server_waits = jserver_config["server-wait"]
        wait_for_signup = jserver_config["wait-for-signup"]
        quiet = jserver_config["quiet"]
        ref_spec = self.convert_j_ref_spec_to_ref_spec(jserver_config["ref-spec"])
        return ServerConfig(port, server_tries, server_waits, wait_for_signup, quiet, ref_spec)

    def convert_j_ref_spec_to_ref_spec(self, jref_spec) -> RefereeConfig:
        state0 = self.convert_jstate_to_gamestate(jref_spec["state0"])
        quiet = jref_spec["quiet"]
        config_s = self.convert_j_ref_state_to_ref_state(jref_spec["config-s"])
        per_turn = jref_spec["per-turn"]
        observe = jref_spec["observe"]
        return RefereeConfig(state0, quiet, config_s, per_turn, observe)

    def convert_j_ref_state_to_ref_state(self, j_ref) -> RefereeStateConfig:
        qbo = j_ref["qbo"]
        fbo =j_ref["fbo"]
        return RefereeStateConfig(qbo, fbo)

    def convert_j_client_config_to_client_config(self, j_client_config) -> ClientConfig:
        port = j_client_config["port"]
        host = j_client_config["host"]
        wait = j_client_config["wait"]
        quiet = j_client_config["quiet"]
        players = self.jactors_to_players(j_client_config["players"])
        return ClientConfig(port, host, wait, quiet, players)




    def convert_turn_to_j_turn(self, turn: Turn):
        if turn.turn_outcome == TurnOutcome.PASSED or turn.turn_outcome == TurnOutcome.REPLACED:
            return turn.turn_outcome.value
        if turn.turn_outcome == TurnOutcome.PLACED:
            return self.convert_placements_to_jplacements(turn.placements)

    def convert_jaction_to_turn(self, jaction):
        if jaction == "pass":
            return Turn(TurnOutcome.PASSED)
        if jaction == "replace":
            return Turn(TurnOutcome.REPLACED)

        tiles = self.convert_j_placements_to_placements(jaction)

        return Turn(TurnOutcome.PLACED, tiles)

    def convert_j_placements_to_placements(self, jplacements) -> Dict[Pos, Tile]:
        placements = {}
        for placement in jplacements:
            coord = self.convert_coorindate_to_pos(placement["coordinate"])
            tile = self.json_to_tile(placement["1tile"])
            placements[coord] = tile
        return placements

    def pair_results_to_jresults(self, pair_results: Results):
        jwinners = sorted(list(pair_results.winners))
        jmisbehaved = sorted(list(pair_results.misbehaved))
        jresults = [jwinners, jmisbehaved]
        return jresults

    def jactors_to_players(self, jactors) -> List[Player]:
        players = []
        for jactorspec in jactors:
            jname = jactorspec[0]
            strategy = self.convert_jstrategy_to_strategy(jactorspec[1])
            if len(jactorspec) == 4 and jactorspec[2] == "a cheat":
                jcheat = jactorspec[3]
                players.append(CheatPlayer(name=jname, strategy=strategy, cheat=jcheat))
            elif len(jactorspec) == 4:
                jexn = jactorspec[2]
                jcount = jactorspec[3]
                players.append(LoopPlayer(name=jname,exn=jexn,count=jcount,strategy=strategy))
            elif len(jactorspec) == 3:
                jexn = jactorspec[2]
                players.append(ExnPlayer(name=jname, strategy=strategy, exn=jexn))
            else:
                players.append(InHousePlayer(jname, strategy))
        return players

    def convert_tiles_to_jtiles(self, tiles):
        return [self.convert_tile_to_json(tile) for tile in tiles]

    def convert_player_game_states_to_jplayers(self, players: Dict[str, PlayerGameState]):
        j_players = []
        for name, pgs in players.items():
            jhand = self.convert_tiles_to_jtiles(pgs.hand)
            j_players.append({"score":pgs.points, "name": name, "tile*": jhand})
        return j_players

    def convert_gamestate_to_jstate(self, state: GameState):
        jmap = self.convert_map_to_jmap(state.map)
        tiles = self.convert_tiles_to_jtiles(state.referee_deck)
        players = self.convert_player_game_states_to_jplayers(state.players)
        return {"map": jmap, "tile*": tiles, "players": players}

    def convert_jstate_to_gamestate(self, jstate) -> GameState:
        """
         { "map"      : JMap,

        "tile*"    : [JTile, ..., JTile],

        "players"  : [JPlayer, ..., JPlayer] }

        :param jstate:
        :param new: does the players now include a name field
        :return:
        """
        map = self.convert_json_to_map(jstate["map"])
        tiles = [self.json_to_tile(t) for t in jstate["tile*"]]
        players = self.convert_jplayers_to_dict_name_player_game_state(jstate["players"])
        return GameState(given_map=map, tiles=tiles, player_game_states=players)

    def convert_jplayers_to_playergamestates(self, jplayers) -> List[PlayerGameState]:
        """"
        Used for backwards compatibility when player did not have a name field
        """
        players = []
        for player in jplayers:
            score = player["score"]
            hand = [self.json_to_tile(t) for t in player["tile*"]]
            players.append(PlayerGameState(hand, score, False, None))
        return players

    def convert_jtiles_to_tiles(self, tiles):
        return [self.json_to_tile(t) for t in tiles]


    def convert_jplayers_to_dict_name_player_game_state(self, jplayers) -> Dict[str, PlayerGameState]:
        players = {}
        for player in jplayers:
            score = player["score"]
            hand = self.convert_jtiles_to_tiles(player["tile*"])
            pgs = PlayerGameState(hand, score, False, None)
            name = player["name"]
            players.update({name: pgs})
        return players


    def convert_single_turn_to_j_action(self, outcome: TurnOutcome, placement: Dict[Pos, Tile]):
        """
        converts a single turn to a jaction with the given outcome and given placement
        :param outcome the outcome of the turn
        :param placement: the placement
        :return: A j_action which is either pass, replace, or a 1Placement
        """
        if outcome == TurnOutcome.PASSED:
            return "pass"
        if outcome == TurnOutcome.REPLACED:
            return "replace"
        if outcome == TurnOutcome.PLACED:
            return self.convert_placements_to_jplacements(placement)

    def convert_placements_to_jplacements(self, placements: Dict[Pos, Tile]):
        jplacements = []
        for pos, tile in placements.items():
            jplacement = {"coordinate": self.__create_json_pos(pos), "1tile": self.convert_tile_to_json(tile)}
            jplacements.append(jplacement)
        return jplacements

    def convert_placement_to_jplacement(self, placement: Dict[Pos, Tile]) -> dict:
        """
        convert placement to a jplacement of the given placement
        :param placement: the given placements to be converted to a jplacement
        :return the j_placement
        """
        if len(placement) != 1:
            raise Exception("Placements must be of length 1")
        pos = list(placement.keys())[0]
        tile = list(placement.values())[0]
        jpos = self.__create_json_pos(pos)
        jtile = self.convert_tile_to_json(tile)
        return {"coordinate": jpos, "1tile": jtile}

    def convert_jplacements_to_tiles(self, python_json) -> Dict[Pos, Tile]:
        """
        Converts jplacements to dict from pos to tile
        JPlacements is an array of the following shape:
        [{"coordinate": JCoordinate, "1tile": JTile}, ...]
        """
        pos_to_tile = {}
        for placement in python_json:
            pos = self.convert_coorindate_to_pos(placement["coordinate"])
            tile = self.json_to_tile(placement["1tile"])
            pos_to_tile[pos] = tile
        return pos_to_tile

    def convert_coorindate_to_pos(self, python_json) -> Pos:
        return Pos(python_json["column"], python_json["row"])

    def convert_jstrategy_to_strategy(self, strat_string: str) -> PlayerStrategy:
        """
        converts a string representation of a strategy to a player strategy
        :param strat_string the given strategy to be converted to a playerstrategy
        """
        if strat_string == "dag":
            return Dag()
        if strat_string == "ldasg":
            return LDasg()


    def convert_json_to_map(self, python_json: List[Union[int, List[Union[int, Dict[str, str]]]]]) -> Map:

        """
        Converts python_json from a list of json
        :param python_json: json that will be parsed into
        :return: a default dict from positions to their corresponding tiles
        """
        map_rep = defaultdict()
        for row in python_json:
            for i in range(1, len(row)):
                ci, tile = row[i]
                map_tile = Util.json_to_tile(tile)
                pos = Pos(x=ci, y=row[0])
                map_rep[pos] = map_tile
        return Map(config=map_rep)

    def convert_jplayer_to_public_player_data(self, jplayer):
        score = jplayer['score']
        name = jplayer['name']
        tiles = self.convert_jtiles_to_tiles(jplayer['tile*'])

        return PublicPlayerData(score, name, tiles)

    def convert_pubic_player_data_to_jplayer(self, player: PublicPlayerData):
        score = player.score
        name = player.name
        jtiles = self.convert_tiles_to_jtiles(player.tiles)
        return {"score": score, "name": name, "tile*": jtiles}

    def convert_player_state_to_jpub(self, s: PlayerState):
        jmap = self.convert_map_to_jmap(s.current_map)
        tiles_left = s.num_ref_tiles
        player = self.convert_pubic_player_data_to_jplayer(player=s.player_data)
        player_points = s.scores
        return {"map": jmap, "tile*": tiles_left, "players": [player] + player_points}

    def convert_jpub_json_to_game_state(self, python_json) -> GameState:
        """
        JPub is an object with three fields:
        {
            "map": JMap,
            "tile*": Natural,
            "players": [JPlayer, Natural, ..., Natural]
        }
        We take this information and return a GameState object with it.
        """
        names = self.create_names(len(python_json["players"]))
        player_public_data = self.convert_jpub_to_player_state(python_json, names)
        game_state = GameState(config=player_public_data)
        return game_state

    def convert_game_state_to_false_or_j_map(self, game_state: GameState, tiles: [Pos, Tile]) -> str:
        """
        Returns expected output:
        The expected output is either false or the newly constructed JMap if the placement is legal.
        """
        try:
            game_state.place_tiles(tiles)
        except:
            return json.dumps(False)
        j_map = self.convert_map_to_jmap(game_state.map)
        return json.dumps(j_map)

    def convert_map_to_jmap(self, given_map: Map):
        """
        Converts map object into json readable JMap such as:
        [[row, [col, {"color":  color, "shape":  shape}], [col, {...}], ...], [row, [col, {...}, ...]]]
        """
        j_map_dict: [int, List[Dict[str, str]]] = defaultdict(list)
        for pos, tile in sorted(given_map.tiles.items(), key=lambda item: item[0].x):
            json_tile = self.convert_tile_to_json(tile)
            if pos.y not in j_map_dict:
                j_map_dict[pos.y] = []
            j_cells = j_map_dict.get(pos.y)
            j_cells.append([pos.x, json_tile])

        j_map = []
        for y, jcell in sorted(j_map_dict.items()):
            jcell.insert(0, y)
            j_map.append(jcell)

        return j_map

    def convert_jpub_to_player_state(self, python_json) -> PlayerState:
        """
        converts player json to the public player data representation
        :param python_json: JSON representation of Q players
        :param names: All player names
        :return: Public information that the player can know about the game
        """
        map_board = self.convert_json_to_map(python_json["map"])
        referee_deck_length = python_json["tile*"]
        score = python_json["players"][0]["score"]
        other_points = python_json["players"][1:]
        other_points.insert(0, score)
        curr_player = python_json["players"][0]
        player = self.convert_jplayer_to_public_player_data(curr_player)

        ppd = PlayerState(referee_deck_length, map_board, player, other_points)
        return ppd

    def create_names(self, num_of_players: int):
        """
        Automatically creates player names
        :param num_of_players: Number of players to create names for
        """
        return [i for i in range(num_of_players)]

    @staticmethod
    def convert_jplayer_to_player(python_json, strategy: PlayerStrategy, name: str) -> InHousePlayer:
        """
        Converts JSON representation of a player into an actual Q player
        :param python_json: JSON representation of a player
        :param strategy: Strategy to create player with
        :param name: Name of player to be created
        """
        player_tiles = [Util.json_to_tile(tile) for tile in python_json["tile*"]]
        return InHousePlayer(name=name, strategy=strategy, hand=player_tiles)

    @staticmethod
    def write_legal_json_coordinates(given_map: Map, tile: Tile) -> str:
        """
        Determines legal moves for a tile and outputs the data as json formatted JCoordinates
        :param given_map: the map for where valid positions are to be searched
        :param tile: the tile which will be placed on the map
        :return: json of the valid JCoordinates
        """
        positions = Rulebook.get_legal_positions(given_map, tile)
        dict_positions = Util.__convert_positions_to_sorted_dicts(positions)
        return json.dumps(dict_positions)

    @staticmethod
    def json_to_tile(python_json_tile: Dict[str, str]) -> Tile:
        """
        Converts a json tile to an internal representation of a tile
        :param python_json_tile: the tile to be converted
        :return: Tile conversion result
        """
        color = TileColor.get_color_by_name(python_json_tile["color"])
        shape = TileShape.get_shape_by_name(python_json_tile["shape"])
        return Tile(shape, color)

    def convert_tile_to_json(self, tile: Tile) -> Dict[str, str]:
        """
        Converts internal representation of a tile to JSON representation
        """
        return {"color": tile.color.get_name(), "shape": tile.shape.get_name()}

    @staticmethod
    def __convert_positions_to_sorted_dicts(positions: Set[Pos]) -> List[Dict[str, int]]:
        """
        Converts given positions into row-column json coordinates
        :param positions: positions to be converted
        :return: the converted positions in json coordinate form
        """
        row_col_positions = sorted(positions, key=lambda pos: (pos.y, pos.x))
        positions = [Util.__create_json_pos(pos) for pos in row_col_positions]
        return positions

    @staticmethod
    def __create_json_pos(pos: Pos) -> Dict[str, int]:
        """
        Converts a pos into a dictionary pos
        :param pos: the pos that will be converted
        :return: the converted pos
        """
        return {"row": pos.y, "column": pos.x}
