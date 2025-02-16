from player import *
from game import Game
from typing import List, Any
from consts import Result
import logging
import argparse
from tqdm import tqdm
from typing import Dict
from pprint import pprint


player_fns: List[Player] = [
    RandomPlayer,
    DefaultPlayer,
    Conservative,
    Aggressive,
    HyperAggressive,
]


def build_dict(d: Dict[str, int]) -> str:
    return ", ".join((f"{k+':':<4} {v:<5}" for k, v in d.items()))


def build_table(res: Dict[str, Dict[str, int]]) -> List[List[Any]]:
    all_names = tuple(res.keys())
    mapping = {}
    for idx, n in enumerate(all_names):
        mapping[n] = idx

    rows = [[""] + list(all_names)]

    for banker_name in all_names:
        row = [banker_name]
        for player_name in all_names:
            row.append(build_dict(res[banker_name][player_name]))
        rows.append(row)

    return rows


def print_table(table: List[List[Any]]) -> None:
    for r in table:
        for v in r:
            print(f"{str(v):<30}", end="\t")
        print()


if __name__ == '__main__':
    logging.basicConfig(
        filename="messages.log",
        level=logging.WARNING,
        format='%(filename)s: %(levelname)s: %(lineno)d:\t%(message)s',
    )

    parser = argparse.ArgumentParser(
        description="Simulate Chinese New Year Blackjack")

    parser.add_argument("-i", "--iterations", type=int,
                        help="number of iterations to run")

    args = parser.parse_args()
    f = {}
    iterations = args.iterations
    progress = tqdm(total=len(player_fns) * iterations)
    players: List[Player] = [player_fn(False) for player_fn in player_fns]

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
