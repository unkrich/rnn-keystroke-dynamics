# -*- coding: utf-8 -*-

from helpers.test_helpers import *
from random import randint

class ModelTest(object):
    def __init__(self, x_valid_test, y_valid_test, x_imposters, y_imposters, test_size, num_samples=50):
        self.x_valid_test = x_valid_test
        self.y_valid_test = y_valid_test

        self.x_imposters = x_imposters
        self.y_imposters = y_imposters

        self.x_valid_test_sets = []
        self.y_valid_test_sets = []

        self.x_imposter_test_sets = []
        self.y_imposter_test_sets = []

        self.test_size = test_size
        self.num_samples = num_samples

    def setup(self):
        self.generate_valid_test_sets()
        self.generate_imposter_test_sets()

    def generate_valid_test_sets(self):
        for i in range(0, len(self.x_imposters) * self.num_samples): # generate 3 * len(imposters)
            random = randint(0, len(self.x_valid_test) - self.test_size)
            self.x_valid_test_sets.append(self.x_valid_test[random:random+self.test_size])
            self.y_valid_test_sets.append(self.y_valid_test[random:random+self.test_size])

    def generate_imposter_test_sets(self):
        for x_imposter, y_imposter in zip(self.x_imposters, self.y_imposters): # generate 3 * len(imposters) random sets
            for i in range(0, self.num_samples):
                random = randint(0, len(x_imposter) - self.test_size)
                self.x_imposter_test_sets.append(x_imposter[random:random+self.test_size])
                self.y_imposter_test_sets.append(y_imposter[random:random+self.test_size])


    def calculate_eer(self, model):
        valid_novelty_scores = []
        for x_valid, y_valid in zip(self.x_valid_test_sets, self.y_valid_test_sets):
            y_predictions = []
            i = 0
            for encoding in x_valid:
                y_prediction = model.predict(reshape(encoding))
                y_predictions.append(y_prediction)
                i += 1
            score = calculate_novelty_score(y_valid, y_predictions)
            valid_novelty_scores.append(score)

        imposter_novelty_scores = []
        for x_imposter, y_imposter in zip(self.x_imposter_test_sets, self.y_imposter_test_sets):
            y_predictions = []
            for encoding in x_imposter:
                y_predictions.append(model.predict(reshape(encoding)))
            score = calculate_novelty_score(y_imposter, y_predictions)
            imposter_novelty_scores.append(score)

        threshold = 0
        num_total_sets = len(valid_novelty_scores) + len(imposter_novelty_scores)
        frr = calculate_frr(valid_novelty_scores, threshold)
        far = calculate_far(imposter_novelty_scores, threshold)

        while(frr > far and threshold < 1000): # with threshold 0, frr will be 100% beginning, when theyre equal the ratio will change
            threshold += 1
            frr = calculate_frr(valid_novelty_scores, threshold)
            far = calculate_far(imposter_novelty_scores, threshold)

        return frr, far, threshold

