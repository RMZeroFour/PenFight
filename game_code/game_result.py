from numpy import random
from enum import Enum


class GameResult:

    WIN_COIN_REWARD = (25, 75)
    TIE_COIN_REWARD = (10, 25)

    def __init__(self, state):
        self.state = state

        self.coins = 0
        if self.state == GameResult.VictoryState.WIN:
            self.coins = random.randint(GameResult.WIN_COIN_REWARD[0], GameResult.WIN_COIN_REWARD[1], dtype=int)
        elif self.state == GameResult.VictoryState.TIE:
            self.coins = random.randint(GameResult.TIE_COIN_REWARD[0], GameResult.TIE_COIN_REWARD[1], dtype=int)

    class VictoryState(Enum):
        WIN = 0
        LOSE = 1
        TIE = 2
