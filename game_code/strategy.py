import random
from game_code import Perimeter
from game_code.b2d import Vec2


class Strategy:
    def next_move(self, player, other_player, table, world):
        pass


class Offensive(Strategy):
    def next_move(self, player, other_player, table, world):
        return 0


class Defensive(Strategy):
    def next_move(self, player, other_player, table, world):
        hit_point = player.body.transform * Perimeter.get_point(player.shape, random.random())
        target = Vec2(table.center[0] + random.random() * 5 - 2.5, table.center[1] + random.random() * 5 - 2.5)
        return target, hit_point


class Endurable(Strategy):
    def next_move(self, player, other_player, table, world):
        return 0


class Hybrid(Strategy):
    def __init__(self):
        self.offensive = Offensive()
        self.defensive = Defensive()
        self.endurable = Endurable()

    def next_move(self, player, other_player, table, word):
        return 0
