from data_helpers import *
import numpy as np

class ModelData(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.x_data = None
        self.y_data = None

    def read(self):
        data = read_from_file_to_arr(self.file_name)
        encodings_32 = generate_encodings(data)
        concatenated_encodings_64 = concatenate_encodings(encodings_32)
        digraph_vectors = generate_digraph_vectors(data)
        clean_encodings_64, clean_digraph_vectors = clean_data(concatenated_encodings_64, digraph_vectors)

        self.x_data = reshape(clean_encodings_64)
        self.y_data = reshape(clean_digraph_vectors)

    def get_training(self, num):
        return self.x_data[:num], self.y_data[:num]

    def get_testing(self, num):
        return self.x_data[num:], self.y_data[num:]

