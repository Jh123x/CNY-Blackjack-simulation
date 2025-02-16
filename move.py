from enum import Enum


class Move(Enum):
    Hit = "hit"
    Stand = "stand"  # = to all open for banker

    # Banker only moves
    Run = "run"
    Open3 = "open_3"  # Those with 3 or 4 open
    Open4 = "open_4"  # Those with 4 open
