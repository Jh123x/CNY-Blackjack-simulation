from typing import List, Optional
from consts import Result
from enum import Enum


class Card(Enum):
    Ace = 'A'
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 'J'
    Queen = 'Q'
    King = 'K'

    def get_value(self, hand_size: int, curr_sum: int) -> int:
        """Get the value of the card"""
        # Normal Cards
        if type(self.value) == int:
            return self.value

        # Picture
        if self != Card.Ace:
            return 10

        # Handle Ace
        if hand_size >= 4:
            return 1

        if curr_sum == 11:
            return 10

        if curr_sum <= 10:
            return 11

        return 1


class Hand:
    def __init__(self, cards: List[Card] = []):
        self.cards = cards.copy()
        self.cached_value: Optional[int] = None

    def add_card(self, card: Card):
        if len(self.cards) >= 5:
            raise ValueError("Cannot add more than 5 cards")
        self.cards.append(card)
        self.cached_value = None
        
    def can_hit(self) -> bool:
        return self.get_value() <= 21 and len(self) < 5

    def __len__(self) -> int:
        return len(self.cards)

    def __repr__(self):
        return "[" + ','.join(map(lambda x: str(x.value), self.cards)) + "] (" + str(self.get_value()) + ")"

    def get_value(self) -> int:
        if self.cached_value is not None:
            return self.cached_value

        acc, no_ace = 0, 0
        for c in self.cards:
            if c == Card.Ace:
                no_ace += 1
                continue
            acc += c.get_value(len(self.cards), acc)

        for _ in range(no_ace):
            acc += Card.Ace.get_value(len(self.cards), acc)

        self.cached_value = acc
        return acc

    @staticmethod
    def get_banker_result(banker: 'Hand', player: 'Hand') -> Result:
        """Compare result from the banker perspective"""
        banker_sum = banker.get_value()
        player_sum = player.get_value()

        if banker_sum > 21 and player_sum > 21:
            return Result.Tie

        if banker_sum > 21:
            return Result.Lose

        if player_sum > 21:
            return Result.Win

        if len(player) >= 5:
            return Result.Lose
        
        if len(banker) >= 5:
            return Result.Win

        if banker_sum > player_sum:
            return Result.Win

        elif banker_sum == player_sum:
            return Result.Tie

        return Result.Lose
