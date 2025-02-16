from typing import List, Dict
from player import Player
from deck import Deck
from card import Hand
from move import Move
from consts import Result, BankerStats
from collections import defaultdict
import logging


class Game:
    def __init__(
        self,
        banker: Player,
        players: List[Player],
        deck: Deck = Deck.get_standard_deck(),
    ):
        self.banker: Player = banker
        self.players: List[Player] = players
        self.deck: Deck = deck
        self.reset()

    def run(self) -> BankerStats:
        """Run 1 round of blackjack"""
        self.__current_deck.shuffle()

        try:
            for _ in range(2):
                for i in range(len(self.__hands)):
                    self.__hands[i].add_card(self.__current_deck.draw())

            for idx, player in enumerate(self.players):
                self.make_player_move(player, self.__hands[idx])
                logging.debug(f"Player final hand:", self.__hands[idx])

            return self.make_banker_move(self.banker, self.__hands[-1], self.__hands[:-1])
        except Exception as e:
            logging.error(
                f"Hands: {self.__hands}, deck: {self.__current_deck}, error: {e}")
            return (0, 0, 0)

    def __make_forced_moves(self, player: Player, hand: Hand) -> None:
        while player.is_forced_move(hand):
            hand.add_card(self.__current_deck.draw())

    def make_banker_move(self, player: Player, hand: Hand, player_hands: List[Hand]) -> BankerStats:
        """Triggers the banker moves"""
        stat = defaultdict(int)
        self.__make_forced_moves(player, hand)

        while hand.can_hit() and len(player_hands) > 0:
            move = player.make_move(hand)
            logging.debug(f"Player {player.name} w {hand}:{move.name}")
            if move == Move.Hit:
                hand.add_card(self.__current_deck.draw())

            elif move == Move.Run:
                return BankerStats(ties=len(player_hands))

            elif move == Move.Stand:
                break

            elif move == Move.Open3:
                c = player_hands
                player_hands = []
                for p in c:
                    if len(p) < 3:
                        player_hands.append(p)
                        continue
                    res = Hand.get_banker_result(hand, p)
                    stat[res] += 1

                hand.add_card(self.__current_deck.draw())

            elif move == Move.Open4:
                c = player_hands
                player_hands = []
                for p in c:
                    if len(p) < 4:
                        player_hands.append(p)
                        continue
                    res = Hand.get_banker_result(hand, p)
                    stat[res] += 1

                hand.add_card(self.__current_deck.draw())

            else:
                raise ValueError("unexpected move from players")

        for p in player_hands:
            result = Hand.get_banker_result(hand, p)
            stat[result] += 1

        return BankerStats(
            wins=stat.get(Result.Win, 0),
            loses=stat.get(Result.Lose, 0),
            ties=stat.get(Result.Tie, 0),
        )

    def make_player_move(self, player: Player, hand: Hand) -> None:
        """Triggers the player moves"""
        self.__make_forced_moves(player, hand)

        while hand.can_hit():
            move = player.make_move(hand)
            logging.debug(f"Player {player.name} w {hand}: {move.name}")
            if move == Move.Hit:
                hand.add_card(self.__current_deck.draw())
            elif move == Move.Stand:
                break
            else:
                raise ValueError("unexpected move from players")

    def reset(self) -> None:
        self.__current_deck = self.deck.copy()
        self.__hands: List[Hand] = []
        for i in range(len(self.players) + 1):
            self.__hands.append(Hand())
