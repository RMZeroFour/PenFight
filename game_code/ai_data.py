import pickle
from enum import Enum


class AIDifficulty(Enum):
    EASY = 0
    NORMAL = 1
    HARD = 2


class AIData:
    all_ai = {}

    def __init__(self, name="", diff=-1, neural_net=None):
        self.pen_name = name
        self.difficulty = diff
        self.neural_net = neural_net

    @staticmethod
    def load_all_ais():
        with open("assets/ai.dat", 'rb') as data_file:
            AIData.all_ai = pickle.load(data_file)

