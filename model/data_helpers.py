# -*- coding: utf-8 -*-
import numpy as np
from keycodes import keycode_obj

def read_from_file_to_arr(file_name):
  data = open(file_name, 'r').read()
  data_arr = data.split("|")
  # TODO - clean_data(): remove data points over 1000ms
  data_arr.pop(0) # remove metadata

  return data_arr

def generate_encodings(data):
  all_one_hot_encodings = []
  for keystroke in data:
    one_hot_encoding = np.zeros(32)
    keystroke_data = keystroke.split(',')

    keystroke_keycode = int(keystroke_data[3])
    index_val = 31
    
    if keystroke_keycode in keycode_obj:
      index_val = keycode_obj[keystroke_keycode]['arr_val']
      one_hot_encoding[index_val] = 1
      all_one_hot_encodings.append(one_hot_encoding)
    # else:
      # throw away - note: THIS CORRUPTS DATA

  return all_one_hot_encodings

def concatenate_encodings(encodings):
  all_concatenated_encodings = []

  num_encodings = len(encodings) - 1
  for i in range(num_encodings):
    current_encoding = encodings[i]
    next_encoding = encodings[i+1]
    all_concatenated_encodings.append(np.concatenate([current_encoding, next_encoding]))

  return all_concatenated_encodings

def ks_seek_press(keystroke):
  keystroke_data = keystroke.split(',')
  keystroke_seek_time = int(keystroke_data[1])
  keystroke_press_time = int(keystroke_data[2])
  return keystroke_seek_time, keystroke_press_time

def calc_between_ks_timings(ks_init_seek, ks_init_press, ks_next_seek, ks_next_press):
  dd = ks_next_seek
  ud = ks_next_seek - ks_init_press
  uu = (ks_next_seek - ks_init_press) + ks_next_press
  du = ks_next_seek + ks_next_press

  return dd, ud, uu, du

def generate_digraph_vectors(data):
  digraph_data = []

  num_keystrokes = len(data) - 1
  for i in range(num_keystrokes):
    ks_init = data[i]
    ks_init_seek, ks_init_press = ks_seek_press(ks_init)

    ks_next = data[i+1]
    ks_next_seek, ks_next_press = ks_seek_press(ks_next)

    dd, ud, uu, du = calc_between_ks_timings(ks_init_seek, ks_init_press, ks_next_seek, ks_next_press)
    digraph_data.append([dd, ud, uu, du])

  return digraph_data

def reshape(data):
  np_data = np.array(data)
  return np.reshape(np_data, (np_data.shape[0], 1, np_data.shape[1]))

def clean_data(encodings, digraph_vectors):
  clean_encodings = []
  clean_digraph_vectors = []

  for i in range(len(digraph_vectors)):
    if digraph_vectors[i][0] < 1000: # seek time
      clean_encodings.append(encodings[i])
      clean_digraph_vectors.append(digraph_vectors[i])

  return clean_encodings, clean_digraph_vectors


