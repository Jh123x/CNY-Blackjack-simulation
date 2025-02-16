from card import Card
from typing import List, Iterable
from random import shuffle
from copy import deepcopy


class Deck:
    def __init__(self, cards: Iterable[Card]):
        """Represents a deck of cards"""
        self.cards = list(cards)

    @staticmethod
    def get_standard_deck() -> 'Deck':
        return Deck((Card(i) for i in ['A', 'J', 'Q', 'K', 2, 3, 4, 5, 6, 7, 8, 9, 10] for _ in range(4)))

    def shuffle(self):
        """Shuffles the deck"""
        shuffle(self.cards)
        
    def __len__(self) -> int:
        return len(self.cards)

    def draw(self) -> Card:
        """Draws the top of the deck"""
        if len(self) <= 0:
            raise ValueError("deck ran out of cards")

        return self.cards.pop()

    def copy(self) -> 'Deck':
        return Deck(deepcopy(self.cards))

    def __repr__(self) -> str:
        return ','.join(map(lambda x: x.value, self.cards))
