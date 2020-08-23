from game_code import AIData, PenData, NeuralNetwork
from game_code.ai_data import AIDifficulty
import pickle


training_generations = {
    AIDifficulty.EASY: 1000,
    AIDifficulty.NORMAL: 2000,
    AIDifficulty.HARD: 3000,
}


def main():
    with open("assets/pens.json", 'r') as data_file:
        PenData.load_all_pens(data_file.read())

    pen_diff_pairs = [(pen_data, diff) for diff in list(AIDifficulty) for pen_data in PenData.all_pens]

    all_ai_data = {(pen_data.name, diff): AIData(pen_data.name, diff, train(pen_data, diff))
                   for (pen_data, diff) in pen_diff_pairs}

    with open("assets/ai.dat", 'wb') as save_file:
        pickle.dump(all_ai_data, save_file)


def train(pen, diff):
    generations = training_generations[diff]
    return NeuralNetwork.create(15, 8, 3)


main()
