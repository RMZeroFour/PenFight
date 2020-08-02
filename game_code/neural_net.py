import numpy as np


class NeuralNetwork:
    def __init__(self, wih, bh, who, bo):
        self.weights_ih, self.bias_h = wih, bh
        self.weights_ho, self.bias_o = who, bo

        self.hidden_activation = lambda v: 1 / (1 + np.exp(-v))
        self.output_activation = lambda v: np.tanh(v)

    @staticmethod
    def create(inputs, hiddens, outputs):
        wih = np.random.random((hiddens, inputs)) * 2.0 - 1.0
        bh = np.random.random((hiddens, 1)) * 2.0 - 1.0
        who = np.random.random((outputs, hiddens)) * 2.0 - 1.0
        bo = np.random.random((outputs, 1)) * 2.0 - 1.0
        return NeuralNetwork(wih, bh, who, bo)

    def predict(self, input_values):
        input_mat = np.array(input_values).reshape(len(input_values), 1)
        hidden_mat = self.hidden_activation(np.dot(self.weights_ih, input_mat) + self.bias_h)
        output_mat = self.output_activation(np.dot(self.weights_ho, hidden_mat) + self.bias_o)
        return output_mat.flatten()

    @staticmethod
    def crossover(first, second):
        def cross_matrix(a, b):
            pivot = int(np.random.random() * (a.size - 1) + 1)
            mask = ([0] * pivot) + ([1] * (a.size - pivot))
            mask = np.array(mask).reshape(a.shape)
            return (a * mask) + (b * (mask ^ 1))

        return NeuralNetwork(cross_matrix(first.weights_ih, second.weights_ih),
                             cross_matrix(first.bias_h, second.bias_h),
                             cross_matrix(first.weights_ho, second.weights_ho),
                             cross_matrix(first.bias_o, second.bias_o))

    def mutate(self, probability):
        for mat in (self.weights_ih, self.bias_h, self.weights_ho, self.bias_h):
            for element in np.nditer(mat, op_flags=['readwrite']):
                if probability > np.random.random():
                    element += np.random.random() * 2 - 1
