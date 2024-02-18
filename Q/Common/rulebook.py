from typing import Dict, Set, Callable, List

from Q.Common.referee_state_config import RefereeStateConfig
from Q.Util.pos_funcs import PosFuncs
from Q.Common.Board.tile import Tile
from Q.Common.map import Map
from Q.Common.Board.pos import Pos


config = RefereeStateConfig(qbo=6, fbo=6)

class Rulebook:
    def __init__(self, rsc: RefereeStateConfig = config):
        self.rsc = rsc

    """
    Represents the game rules which the referee and players may consult
    Source of truth of all dynamically changeable items of the game
    """

    def get_legal_positions(self, given_map: Map, given_tile: Tile, placed_positions: List[Pos],
                            break_early: bool = False) -> Set[Pos]:
        """
        Computes all of the legal positions to place the given tile onto the given map
        :param placed_positions: the positions that have already been placed
        :param given_map: the map searched for valid positions
        :param given_tile: the tile that is placed
        :return: a set of valid positions
        """
        valid_positions: Set[Pos] = set()
        for p, tile in given_map.tiles.items():
            if tile.shape != given_tile.shape and tile.color != given_tile.color:
                continue
            neighbors: Dict[Pos, Tile] = given_map.get_neighbors(p)
            valid_neighbor_positions = self.filter_adjacent_positions(neighbors, given_tile, given_map)
            for neighbor in valid_neighbor_positions:
                potential_positions = placed_positions.copy()
                potential_positions.append(neighbor)
                if self.all_same_row_or_col(potential_positions):
                    valid_positions.add(neighbor)
                    if break_early:
                        return valid_positions

        return valid_positions

    def get_legal_hand(self, given_map: Map, hand: List[Tile], already_placed: List[Pos]) -> List[Tile]:
        """
        Gets the legal hand based on some rulebook
        """
        return list(filter(lambda tile: len(self.get_legal_positions(given_map, tile, already_placed)) != 0, hand))

    def filter_adjacent_positions(self, neighbors: Dict[Pos, Tile], given_tile: Tile, map: Map) -> Set[Pos]:
        """
        Filters out the neighbors of a specific tile which the given tile can be placed
        :param neighbors: potential tile placements
        :param given_tile: the tile being placed
        :param map: the map at which we inspect for valid placements
        :return: the set of valid positions
        """
        valid_positions = set()
        for pos, tile in neighbors.items():
            if tile:
                continue
            is_valid: bool = self.is_valid_space(map, pos, given_tile)
            if is_valid:
                valid_positions.add(pos)

        return valid_positions

    def is_valid_space(self, given_map: Map, pos: Pos, given_tile: Tile) -> bool:
        """
        Is this given tile allowed to be placed at the given position on the given map according to the rulebook?
        :param given_map: the map at which we insect for a valid placement
        :param pos: the position of the potentially valid space
        :param given_tile: the tile we are trying to place
        :return: true if the tile can be placed
        """
        nbrs: Dict[Pos, Tile] = given_map.get_neighbors(pos)
        if all(x is None for x in nbrs.values()):
            return False

        def compare_features(call1: Callable[[Pos], Pos], call2: Callable[[Pos], Pos], p: Pos,
                             comparator: Callable[[Tile, Tile], bool]) -> bool:
            if p is None:
                return False
            return comparator(given_tile, nbrs[call1(p)]) and comparator(given_tile, nbrs[call2(p)])

        shapes_same_vert = compare_features(PosFuncs.above, PosFuncs.below, pos, self.compatible_shapes)
        shapes_same_hor = compare_features(PosFuncs.left, PosFuncs.right, pos, self.compatible_shapes)
        colors_same_vert = compare_features(PosFuncs.above, PosFuncs.below, pos, self.compatible_colors)
        colors_same_hor = compare_features(PosFuncs.left, PosFuncs.right, pos, self.compatible_colors)

        return (shapes_same_vert or colors_same_vert) and (shapes_same_hor or colors_same_hor)

    def valid_replacement(self, num_of_ref_tiles: int, player_hand: List[Tile]):
        """
        is this a valid replacement move
        :param num_of_ref_tiles: the number of ref tiles
        :param player_hand: the players current hand
        :return: true if a replacement is possible
        """
        return len(player_hand) <= num_of_ref_tiles

    def valid_placements(self, given_map: Map, placements: Dict[Pos, Tile]):
        for pos, tile in placements.items():
            if not self.is_valid_space(given_map, pos, tile):
                return False
            given_map.add_tile_to_board(tile, pos)
        if not self.all_same_row_or_col(list(placements.keys())):
            return False
        return True

    def valid_placement(self, given_map: Map, pos: Pos, tile: Tile, tiles_placed: Dict[Pos, Tile]) -> bool:
        """
        if the given tiles can be placed according to the rules of the Q game
        :param given_map: the given map we are placing tiles at
        :param tiles_placed: the tiles attempting to be placed
        returns true if the tiles can be placed
        """
        if not self.is_valid_space(given_map, pos, tile):
            return False
        tiles_down = list(tiles_placed.keys()) + [pos]
        if not self.all_same_row_or_col(tiles_down):
            return False
        given_map.add_tile_to_board(tile, pos)
        return True

    def compatible_shapes(self, tile1: Tile, tile2: Tile):
        return tile1 is None or tile2 is None or tile1.compatible_shape(tile2)

    def compatible_colors(self, tile1: Tile, tile2: Tile):
        return tile1 is None or tile2 is None or tile1.compatible_color(tile2)

    # SCORING

    def score_turn(self, tiles: Dict[Pos, Tile], curr_map: Map, player_hand: List[Tile], end_game=False) -> int:
        """
        Calculates the points scored on a given turn
        Note: Everything has already been placed before scoring. So it's fine if the player hand is empty.
        :param tiles: the tiles placed which is a mapping from position to tile
        :param end_game: is the game over which add the end bonus points
        :param player_hand: Player's current hand
        :param curr_map: Current map to score turn
        :return: the points scored on a turn
        """
        points_in_turn = 0
        points_in_turn += self.score_place_tiles(tiles)
        positions = [pos for pos in tiles.keys()]
        points_in_turn += self.get_contiguous_sequence_points(curr_map, positions)
        points_in_turn += self.get_completing_q_points(curr_map, positions)
        if end_game:
            points_in_turn += self.score_end_bonus_points(player_hand)
        return points_in_turn

    def score_place_tiles(self, tiles: Dict[Pos, Tile]) -> int:
        """
        calculates the score for placing tiles
        :param tiles: the tiles that are placed to be scored
        :return the points valued to be scored
        """
        return len(tiles)

    def score_end_bonus_points(self, player_hand: List[Tile]) -> int:
        """
        calculates the score for the end bonus points if the player places all their tiles
        :param player_hand: the tiles that are placed on the board to be scored
        :return the points to be scored
        """
        if not len(player_hand):
            return self.rsc.fbo
        else:
            return 0

    def get_contiguous_sequence_points(self, curr_map: Map, positions: List[Pos]) -> int:
        """
        From instructions: A Player receives one point per tile in a contiguous sequence of tiles (in a row or column)
        that contains at least one of its newly placed tiles.
        :param positions: List of positions played in a given turn
        :return: number of points to be added for this rule
        """
        row_items = curr_map.get_seen_contiguous_items(curr_map.get_contiguous_row, positions)
        col_items = curr_map.get_seen_contiguous_items(curr_map.get_contiguous_col, positions)
        return len(row_items) + len(col_items)

    def __get_seen_components_points(self, curr_map: Map, contiguous_positions: Set[Pos]) -> int:
        """
        Gets points for seen components for a list of positions contiguous rows/cols
        :param contiguous_positions: list of contiguous positions
        :return: points to be added
        """
        points = 0
        seen_component_shape = set()
        seen_component_color = set()
        for position in contiguous_positions:
            seen_component_shape.add(curr_map.tiles.get(position).shape)
            seen_component_color.add(curr_map.tiles.get(position).color)
            if (len(seen_component_shape) == 6 and len(seen_component_color) == 1) or \
                    (len(seen_component_color) == 6 and len(seen_component_shape) == 1):
                points += self.rsc.qbo
        return points

    def get_completing_q_points(self, curr_map: Map, positions: List[Pos]) -> int:
        """
        :param positions: determines the points for completing some number of q's
        :return: the points for completing q's
        """
        seen_contiguous = set()
        points = 0

        for position in positions:
            contiguous_row = curr_map.get_contiguous_row(position)
            contiguous_col = curr_map.get_contiguous_col(position)
            if contiguous_row not in seen_contiguous:
                points += self.__get_seen_components_points(curr_map, contiguous_row)
                seen_contiguous.add(frozenset(contiguous_row))

            if contiguous_col not in seen_contiguous:
                points += self.__get_seen_components_points(curr_map, contiguous_col)
                seen_contiguous.add(frozenset(contiguous_col))
        return points

    def all_same_row_or_col(self, tiles: List[Pos]) -> bool:
        """
        are all the tiles in the same row xor the same col?
        param: tiles: a list of pos which are checked if they are same row or col
        return: true if tiles are same row or col, else false
        """
        return len(set(pos.x for pos in tiles)) == 1 or \
               len(set(pos.y for pos in tiles)) == 1
