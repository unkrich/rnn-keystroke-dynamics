import sys

import KerasModel
import ModelData

def main():
    valid_user_text = 'data/keystrokes/participant_1.txt'
    imposter_users_text = ['data/keystrokes/participant_2.txt', 
                           'data/keystrokes/participant_3.txt',
                           'data/keystrokes/participant_4.txt',
                           'data/keystrokes/participant_5.txt',
                           'data/keystrokes/participant_6.txt',
                           'data/keystrokes/participant_7.txt',
                           'data/keystrokes/participant_8.txt']

    valid_data = ModelData(valid_user_text).read()
