# -*- coding: utf-8 -*-

import math
import numpy as np

# vary threshold and 
def huber_loss_no_tensor(y_true, y_pred, clip_delta=1.0):
  error = y_true - y_pred

  if(math.fabs(error) < clip_delta):
    squared_loss = 0.5 * (math.fabs(error**2))
    return squared_loss

  else:
    linear_loss  = clip_delta * (math.fabs(error) - 0.5 * clip_delta)
    return linear_loss

def ns_huber_loss_calc(y_true_vector, y_predict_vector):
  loss = 0
  for y_true, y_predict in zip(y_true_vector, y_predict_vector):
    loss += huber_loss_no_tensor(y_true, y_predict)

  return loss

def calculate_novelty_score(test_y, test_x_predictions):
  t = len(test_y)
  ns_sum = 0

  for i in range(t):
    ns_sum += ns_huber_loss_calc(test_y[i][0], test_x_predictions[i][0][0]) # TODO - explain indexing

  ns_sum /= (4*t)

  return ns_sum

def reshape(data):
  np_data = np.array(data)
  return np.reshape(np_data, (np_data.shape[0], 1, np_data.shape[1]))

def calculate_frr(novelty_scores, threshold):
    num_rejected = 0
    for score in novelty_scores:
      if score > threshold:
          num_rejected += 1

    return num_rejected / len(novelty_scores)

def calculate_far(novelty_scores, threshold):
    num_approved = 0
    for score in novelty_scores:
      if score < threshold:
          num_approved += 1

    return num_approved / len(novelty_scores)