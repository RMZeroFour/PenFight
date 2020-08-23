import numpy as np


class NeuralNetwork:
    def __init__(self, wih, bh, who, bo):
        self.weights_ih, self.bias_h = wih, bh
        self.weights_ho, self.bias_o = who, bo

    @staticmethod
    def create(inputs, hiddens, outputs):
        wih = np.random.random((hiddens, inputs)) * 2.0 - 1.0
        bh = np.random.random((hiddens, 1)) * 2.0 - 1.0
        who = np.random.random((outputs, hiddens)) * 2.0 - 1.0
        bo = np.random.random((outputs, 1)) * 2.0 - 1.0
        return NeuralNetwork(wih, bh, who, bo)

    @staticmethod
    def clone(nn):
        wih = nn.weights_ih.copy()
        bh = nn.bias_h.copy()
        who = nn.weights_ho.copy()
        bo = nn.bias_o.copy()
        return NeuralNetwork(wih, bh, who, bo)

    def predict(self, input_values):
        def activation(v):
            return 1 / (1 + np.exp(-v))
        input_mat = np.array(input_values).reshape(len(input_values), 1)
        hidden_mat = activation(np.dot(self.weights_ih, input_mat) + self.bias_h)
        output_mat = activation(np.dot(self.weights_ho, hidden_mat) + self.bias_o)
        return output_mat.flatten()

    def mutate(self, probability, max_delta):
        for mat in (self.weights_ih, self.bias_h, self.weights_ho, self.bias_h):
            for element in np.nditer(mat, op_flags=['readwrite']):
                if probability > np.random.random():
                    element += (np.random.random() * 2 - 1) * max_delta

