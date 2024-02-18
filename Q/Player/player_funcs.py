from enum import Enum


class PlayerFuncs(Enum):
    """
    The function names that exist on the player API
    """
    TAKE_TURN = 'take-turn'
    SETUP = 'setup'
    NEW_TILES = 'new_tiles'
    WIN = 'win'



