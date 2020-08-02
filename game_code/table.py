from game_code.units import *
from game_code.b2d import *


class Table:
    def __init__(self, center, dimensions, world):
        self.center = center
        self.dimensions = dimensions

        self.body = world.CreateStaticBody(position=self.center)
        fixture = self.body.CreatePolygonFixture(box=self.dimensions)
        fixture.sensor = True

    def contains_point(self, point):
        return self.center[0] - self.dimensions[0] / 2 <= point[0] <= self.center[0] + self.dimensions[0] / 2 and \
               self.center[1] - self.dimensions[1] / 2 <= point[1] <= self.center[1] + self.dimensions[1] / 2
