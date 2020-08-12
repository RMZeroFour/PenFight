from game_code.units import *
from game_code.b2d import *


class Pen:
    def __init__(self, data, position, table_body, world):
        self.data = data

        self.body = world.CreateDynamicBody(position=position)
        self.shape = PolyShape(vertices=data.mesh_points)

        fixture_def = FixtureDef(density=data.density, restitution=data.restitution)
        fixture_def.shape = self.shape
        self.fixture = self.body.CreateFixture(fixture_def)

        world.CreateFrictionJoint(bodyA=self.body, bodyB=table_body,
                                  maxForce=data.friction[0], maxTorque=data.friction[1])

    def apply_force(self, point, force):
        self.body.ApplyLinearImpulse(force, point, True)

    def get_position(self):
        return self.body.position

    def get_rotation(self):
        return self.body.angle

    def get_vertices(self):
        return [(self.body.transform * v) for v in self.body.fixtures[0].shape.vertices]
