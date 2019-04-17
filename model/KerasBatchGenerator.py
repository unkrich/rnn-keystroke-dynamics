# -*- coding: utf-8 -*-

import numpy as np

# ref: https://adventuresinmachinelearning.com/keras-lstm-tutorial/
class KerasBatchGenerator(object):
    def __init__(self, x_data, y_data, num_steps, batch_size, output_size):
        self.x_data = x_data
        self.y_data = y_data
        self.num_steps = num_steps
        self.batch_size = batch_size
        self.output_size = output_size
        self.current_idx = -num_steps

    def generate(self):
        x = np.zeros((self.batch_size, 1, self.num_steps))
        y = np.zeros((self.batch_size, 1, self.output_size))
        while True:
            self.current_idx += self.num_steps

            if self.current_idx + self.num_steps >= len(self.x_data):
                self.current_idx = 0

            x = self.x_data[self.current_idx:self.current_idx + self.batch_size]
            y = self.y_data[self.current_idx:self.current_idx + self.batch_size]

            yield x, y
