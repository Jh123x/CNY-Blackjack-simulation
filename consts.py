from enum import Enum
from typing import NamedTuple


# From the banker perspective.
class BankerStats(NamedTuple):
    wins: int = 0
    ties: int = 0
    loses: int = 0


class Result(Enum):
    Tie = "TIE"
    Win = "WIN"
    Lose = "LOSE"
