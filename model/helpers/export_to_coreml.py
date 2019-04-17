# -*- coding: utf-8 -*-

from keras.models import load_model
import tensorflow as tf
import coremltools

def huber_loss(y_true, y_pred, clip_delta=1.0):
  error = y_true - y_pred
  cond  = tf.keras.backend.abs(error) < clip_delta
  squared_loss = 0.5 * tf.keras.backend.square(error)
  linear_loss  = clip_delta * (tf.keras.backend.abs(error) - 0.5 * clip_delta)
  return tf.where(cond, squared_loss, linear_loss)

# in main, model.save('model.h5')
model = load_model('model.h5', custom_objects={'huber_loss': huber_loss})
coreml_model = coremltools.converters.keras.convert(model)
coreml_model.save('model.mlmodel')