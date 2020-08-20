import json
from resources import Resources
from enum import Enum
from game_code import NeuralNetwork


class AIDifficulty(Enum):
    EASY = 0
    NORMAL = 1
    HARD = 2


class AIData:
    all_ai = {}

    def __init__(self):
        self.pen_name = ""
        self.difficulty = -1
        self.neural_net = None

    @staticmethod
    def load_all_ais(json_data):
        dicts = json.loads(json_data)

        ai_list = [AIData.dict_to_ai(d) for d in dicts]
        for ai in ai_list:
            AIData.all_ai[(ai.pen_name, ai.difficulty)] = ai

    @staticmethod
    def dict_to_ai(d):
        p = AIData()
        p.pen_name = d["pen_name"]
        p.difficulty = AIDifficulty(d["difficulty"])
        p.neural_net = NeuralNetwork.from_array(d["neural_net"])
        return p

    @staticmethod
    def ai_to_dict(ai):
        return {
            "pen_name": ai.pen_name,
            "difficulty": ai.difficulty.value,
            "neural_net": NeuralNetwork.to_array(ai.neural_net)
        }
