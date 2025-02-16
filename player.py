from card import Hand
from move import Move
from random import choice
from typing import List


class Player:
    def __init__(self, name: str, is_banker: bool):
        """Represents the player"""
        self.name = name
        self.is_banker = is_banker
        return super().__init__()

    def get_name(self) -> str:
        return self.name

    def is_forced_move(self, hand: Hand) -> bool:
        if len(hand) >= 5:
            return False

        hand_value = hand.get_value()
        if self.is_banker:
            return hand_value != 15 and hand_value < 17
        else:
            return hand_value < 16

    def make_move(self, _: Hand) -> Move:
        """Makes a move based on the cards"""
        raise NotImplementedError(
            "Please implement the method for the player class")


class DefaultPlayer(Player):
    def __init__(self, is_banker: bool):
        return super().__init__("Stand", is_banker)

    def make_move(self, _: Hand) -> Move:
        return Move.Stand


class RandomPlayer(Player):
    def __init__(self, is_banker: bool):
        return super().__init__("Random", is_banker)

    def make_move(self, hand: Hand) -> Move:
        possible_moves: List[Move] = [Move.Stand, Move.Hit]
        if self.is_banker:
            if hand.get_value() == 15:
                possible_moves.append(Move.Run)
            possible_moves.append(Move.Open3)
            possible_moves.append(Move.Open4)

        return choice(possible_moves)


class Conservative(Player):
    def __init__(self, is_banker: bool):
        return super().__init__("Conservative", is_banker)

    def make_move(self, hand: Hand) -> Move:
        if self.is_banker:
            return self.__parse_banker(hand)

        return self.__parse_move(hand)

    def __parse_banker(self, hand: Hand) -> Move:
        value = hand.get_value()
        if value == 15:
            return Move.Run

        if value <= 17:
            return Move.Open3

        return Move.Stand

    def __parse_move(self, hand: Hand) -> Move:
        value = hand.get_value()
        if value <= 16:
            return Move.Hit
        return Move.Stand


class Aggressive(Player):
    def __init__(self, is_banker: bool):
        return super().__init__("Aggressive", is_banker)

    def make_move(self, hand: Hand) -> Move:
        if self.is_banker:
            return self.__parse_banker(hand)

        return self.__parse_move(hand)

    def __parse_banker(self, hand: Hand) -> Move:
        value = hand.get_value()
        if value == 15:
            return Move.Run

        if value <= 18:
            return Move.Open3

        return Move.Stand

    def __parse_move(self, hand: Hand) -> Move:
        value = hand.get_value()
        if value <= 17:
            return Move.Hit
        return Move.Stand


class HyperAggressive(Player):
    def __init__(self, is_banker: bool):
        return super().__init__("HyperAggressive", is_banker)

    def make_move(self, hand: Hand) -> Move:
        if self.is_banker:
            return self.__parse_banker(hand)

        return self.__parse_move(hand)

    def __parse_banker(self, hand: Hand) -> Move:
        value = hand.get_value()
        if value == 15:
            return Move.Run

        if value <= 18:
            return Move.Open3

        return Move.Stand

    def __parse_move(self, hand: Hand) -> Move:
        value = hand.get_value()
        if value <= 18:
            return Move.Hit
        return Move.Stand
