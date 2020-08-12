import json
from resources import Resources


class PenData:
    all_pens = []

    current_pen = None
    current_enemy_pen = None

    def __init__(self):
        self.name = ""
        self.density = 0.0
        self.restitution = 0.0
        self.friction = (0.0, 0.0)
        self.image_file = ""
        self.cost = 0
        self.description = []
        self.mesh_points = []

    @staticmethod
    def load_all_pens():
        json_data = Resources.get("all_pens")
        dicts = json.loads(json_data)
        PenData.all_pens = [PenData.dict_to_pen(d) for d in dicts]

    @staticmethod
    def dict_to_pen(d):
        p = PenData()
        p.__dict__.update(d)
        return p
