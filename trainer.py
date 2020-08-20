import json
import numpy
import io
from game_code import AIData, PenData, NeuralNetwork
from game_code.ai_data import AIDifficulty


def load_text(filename):
    with open(filename, "r") as file:
        return file.read()


def save_text(filename, data):
    with open(filename, "w") as file:
        return file.write(data)


def main():
    PenData.load_all_pens(load_text("assets/pens.json"))
    pen_diff_pairs = [(pen_data, diff) for diff in list(AIDifficulty) for pen_data in PenData.all_pens]

    template = NeuralNetwork.create(15, 8, 2)
    template = NeuralNetwork(numpy.zeros_like(template.weights_ih),
                             numpy.zeros_like(template.bias_h),
                             numpy.zeros_like(template.weights_ho),
                             numpy.zeros_like(template.bias_o))

    all_ai_data = []
    for (pen_data, diff) in pen_diff_pairs:
        ai_data = AIData()
        ai_data.pen_name = pen_data.name
        ai_data.difficulty = diff
        ai_data.neural_net = NeuralNetwork.clone(template)
        all_ai_data.append(ai_data)

    ai_json = json.dumps([AIData.ai_to_dict(ai_data) for ai_data in all_ai_data])

    print("This is th PenFight trainer!")


main()
