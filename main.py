from player import *
from game import Game
from typing import List
from consts import Result
import logging
import argparse
from tqdm import tqdm
from pprint import pprint


player_fns: List[Player] = [
    RandomPlayer,
    DefaultPlayer,
    Conservative,
    Aggressive,
    HyperAggressive,
]

if __name__ == '__main__':
    logging.basicConfig(
        filename="messages.log",
        level=logging.WARNING,
        format='%(filename)s: %(levelname)s: %(lineno)d:\t%(message)s',
    )

    parser = argparse.ArgumentParser(
        description="Simulate Chinese New Year Blackjack",
    )

    parser.add_argument(
        "-i", "--iterations",
        type=int,
        help="number of iterations to run",
    )
    parser.add_argument(
        '-c', "--count",
        type=int,
        default=len(player_fns),
        help="the number of players",
    )

    args = parser.parse_args()
    f = {}
    iterations = args.iterations
    progress = tqdm(total=len(player_fns) * iterations)
    player_count = args.count

    players: List[Player] = [
        player_fns[i % len(player_fns)](False) for i in range(player_count)
    ]

    for banker_fn in player_fns:
        banker: Player = banker_fn(True)
        game = Game(banker, players)

        for _ in range(iterations):
            progress.update()
            stats = game.run()
            win, tie, loss = stats
            logging.info(f"{banker.get_name()}: {stats}")

            banker_name = banker.get_name()
            curr_val = f.get(banker_name, {
                Result.Win.value: 0,
                Result.Tie.value: 0,
                Result.Lose.value: 0,
            })

            curr_val[Result.Win.value] += win
            curr_val[Result.Tie.value] += tie
            curr_val[Result.Lose.value] += loss

            f[banker_name] = curr_val
            game.reset()

    pprint(f)
