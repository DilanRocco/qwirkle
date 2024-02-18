from dataclasses import dataclass

from Q.Referee.referee_config import RefereeConfig

@dataclass
class ServerConfig:
    """
    config values for the server
    """

    port: int
    server_tries: int
    server_wait: int
    wait_for_signup: int
    quiet: bool
    ref_spec: RefereeConfig
