from typing import Set
from dataclasses import dataclass


@dataclass
class Results:
    """
    Represents a pair of names of the winning player(s) and the names those players that misbehaved - from specs webpage
    """
    winners: Set[str]
    losers: Set[str]
    misbehaved: Set[str]
