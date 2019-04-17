# -*- coding: utf-8 -*-

from keras import optimizers
from keras.layers import Dense, LSTM
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential
from KerasBatchGenerator import *
from LossLearningRateScheduler import *
import tensorflow as tf

# ref: https://adventuresinmachinelearning.com/keras-lstm-tutorial/
class KerasModel(object):
    def __init__(self, train_x, train_y, test_x, test_y, epochs=1200, num_steps=64, batch_size=16, output_size=4):
        # Throw error if X & Y are different lengths
        self.model = None
        self.train_x = train_x
        self.train_y = train_y
        self.test_x = test_x
        self.test_y = test_y
        self.epochs = epochs
        self.num_steps = num_steps
        self.batch_size = batch_size
        self.output_size = output_size
        self.train_data_gen = KerasBatchGenerator(train_x, train_y, num_steps, batch_size, output_size)
        self.test_data_gen = KerasBatchGenerator(test_x, test_y, num_steps, batch_size, output_size)

    def create(self):
        input_shape = self.train_x.shape[1:]
        hidden_size = self.num_steps * 2

        model = Sequential()
        model.add(LSTM(hidden_size, return_sequences=True, input_shape=(input_shape))) # LSTM 128
        model.add(LSTM(hidden_size, return_sequences=True)) # LSTM 128
        model.add(BatchNormalization())
        # model.add(Flatten())
        model.add(Dense(hidden_size,activation='relu')) # fully connected ReLu 
        model.add(Dense(hidden_size,activation='relu')) # fully connected ReLu
        model.add(Dense(self.output_size)) # fully connected
        
        self.model = model

    def train(self):
        rms_prop = optimizers.RMSprop(lr=0.1)
        steps_per_epoch = int(len(self.train_x)/(self.batch_size*self.num_steps))
        validation_steps = int(len(self.test_x)/(self.batch_size*self.num_steps))
        loss_scheduler = LossLearningRateScheduler(base_lr=0.1, lookback_epochs=5)

        # self.model.compile(loss=tf.losses.huber_loss, optimizer=rms_prop, metrics=['accuracy'])
        self.model.compile(loss=huber_loss, optimizer=rms_prop, metrics=['accuracy'])

        self.model.fit_generator(self.train_data_gen.generate(), 
                      steps_per_epoch=(steps_per_epoch),
                      epochs=self.epochs, 
                      validation_data=self.test_data_gen.generate(),
                      validation_steps=(validation_steps), 
                      callbacks=[keras.callbacks.History(), loss_scheduler], 
                      verbose=0)


def huber_loss(y_true, y_pred, clip_delta=1.0):
  error = y_true - y_pred
  cond  = tf.keras.backend.abs(error) < clip_delta

  squared_loss = 0.5 * tf.keras.backend.square(error)
  linear_loss  = clip_delta * (tf.keras.backend.abs(error) - 0.5 * clip_delta)

  return tf.where(cond, squared_loss, linear_loss)

