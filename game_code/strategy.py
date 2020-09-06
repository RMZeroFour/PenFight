import math, random
from game_code import Perimeter
from game_code.b2d import Vec2


def offensive_strategy(player, other_player, table):
    point = other_player.body.position
    target = Vec2(point[0] + random.random() * 2 - 1, point[1] + random.random() * 2 - 1)
    target = target * 0.8 + player.body.position * 0.2
    hit_point = player.body.transform * Perimeter.get_point(player.shape, random.random())

    while (target - player.body.position).dot(hit_point - player.body.position) > 0.0:
        hit_point = player.body.transform * Perimeter.get_point(player.shape, random.random())

    return target, hit_point


def defensive_strategy(player, other_player, table):
    point = table.center
    target = Vec2(point[0] + random.random() * 2 - 1, point[1] + random.random() * 2 - 1)
    target = target * 0.8 + player.body.position * 0.2
    hit_point = player.body.transform * Perimeter.get_point(player.shape, random.random())

    while (target - player.body.position).dot(hit_point - player.body.position) > 0.0:
        hit_point = player.body.transform * Perimeter.get_point(player.shape, random.random())

    return target, hit_point


def hybrid_strategy(player, other_player, table):
    width, height = random.random() * 5 + 27.5, random.random() * 5 + 12.5

    if ((player.body.position.x - table.center[0]) ** 2) / (width ** 2) + \
       ((player.body.position.y - table.center[1]) ** 2) / (height ** 2) <= 1:
        return offensive_strategy(player, other_player, table)
    else:
        return defensive_strategy(player, other_player, table)
