from dataclasses import dataclass

from Q.Common.game_state import GameState
from Q.Common.referee_state_config import RefereeStateConfig


@dataclass
class RefereeConfig:
    """
    represents the config for the referee
    """
    state0: GameState
    quiet: bool
    config_s: RefereeStateConfig
    per_turn: int
    observe: bool
