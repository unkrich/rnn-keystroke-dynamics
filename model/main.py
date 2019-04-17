# -*- coding: utf-8 -*-

import sys
from KerasModel import KerasModel
from ModelData import ModelData
from ModelTest import ModelTest

def main():
    # Import and shape data
    users = ['data/keystrokes/participant_1.txt',
             'data/keystrokes/participant_2.txt', 
             'data/keystrokes/participant_3.txt',
             'data/keystrokes/participant_4.txt',
             'data/keystrokes/participant_5.txt',
             'data/keystrokes/participant_6.txt',
             'data/keystrokes/participant_7.txt',
             'data/keystrokes/participant_8.txt']

    for user in users:
        temp_arr = users.copy()
        temp_arr.remove(user)

        valid_user_text = user
        imposter_users_text = temp_arr

        valid_data = ModelData(valid_user_text)
        valid_data.read()
        imposter_data = {'x': [], 'y': []}
        for imposter in imposter_users_text:
            imposter_data_temp = ModelData(imposter)
            imposter_data_temp.read()
            imposter_data['x'].append(imposter_data_temp.x_data)
            imposter_data['y'].append(imposter_data_temp.y_data)

        # Train model
        TRAIN_SIZE = 7000
        training_x, training_y = valid_data.get_training(TRAIN_SIZE)
        testing_x, testing_y = valid_data.get_testing(TRAIN_SIZE)
        model = KerasModel(training_x, training_y, testing_x, testing_y)
        model.create()
        model.train()

        # Test model
        QUERY_SIZE = 100
        test = ModelTest(testing_x, testing_y, imposter_data['x'], imposter_data['y'], QUERY_SIZE)
        test.setup()
        frr, far, threshold = test.calculate_eer(model.model)
        print("For " + user + " training size " + str(TRAIN_SIZE) + " and testing size " + str(QUERY_SIZE) + " the FRR, FAR, and threshold are: " + str(frr) + " " + str(far) + " " + str(threshold))


if __name__ == '__main__':
    main()