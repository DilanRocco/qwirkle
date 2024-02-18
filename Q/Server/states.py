from enum import Enum


class States(Enum):
    """
    The different states the server may be in 
    """
    SIGNUP = 'signup'
    NO_NAME_GIVEN = 'no_name_given'
    RUNGAME = 'rungame'
