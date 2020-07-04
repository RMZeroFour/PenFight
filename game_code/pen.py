import json
from resources import Resources


class Pen:
    all_pens = []
    current_pen = None

    def __init__(self):
        self.name = ""
        self.mass = 0.0
        self.friction = 0.0
        self.image_file = ""
        self.dimensions = (0.0, 0.0)
        self.cost = 0

    @staticmethod
    def load_all_pens():
        json_data = Resources.get("all_pens")
        dicts = json.loads(json_data)
        Pen.all_pens = [Pen.dict_to_pen(d) for d in dicts]

    @staticmethod
    def dict_to_pen(d):
        p = Pen()
        p.__dict__.update(d)
        return p
