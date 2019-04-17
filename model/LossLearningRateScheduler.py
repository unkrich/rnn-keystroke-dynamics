# -*- coding: utf-8 -*-

import keras
from keras import backend as K
import numpy as np
from statistics import median 

# ref: https://www.kaggle.com/fergusoci/keras-loss-based-learning-rate-scheduler
class LossLearningRateScheduler(keras.callbacks.History):
    """
    A learning rate scheduler that relies on changes in loss function
    value to dictate whether learning rate is decayed or not.
    LossLearningRateScheduler has the following properties:
    base_lr: the starting learning rate
    lookback_epochs: the number of epochs in the past to compare with the loss function at the current epoch to determine if progress is being made.
    """

    def __init__(self, base_lr, lookback_epochs, decay_multiple = 0.5, loss_type = 'val_loss'):
        super(LossLearningRateScheduler, self).__init__()
        self.base_lr = base_lr
        self.lookback_epochs = lookback_epochs
        self.decay_multiple = decay_multiple
        self.loss_type = loss_type
        self.stored_loss = []
        self.epochs_since_halved = 0


    def on_epoch_begin(self, epoch, logs=None):
        
        if epoch >= self.lookback_epochs:
            current_lr = K.get_value(self.model.optimizer.lr)

            ''' 
            Store loss every 10 iterations
            When the median of the most recent 20 stored losses is 
            greater than the median of the most recent five stored losses,
            half the learning rate 

            For some reason, self.history is empty.
            '''

            # target_loss = self.history[self.loss_type] 

            # if epoch % self.lookback_epochs == 0:
            #     self.stored_loss.append(target_loss[-1])
            
            if len(self.stored_loss) % 20 == 0 and len(self.stored_loss) != 0: # never true atm
                if median(self.stored_loss[-20:]) > median(self.stored_loss[-(self.lookback_epochs):]):
                    self.epochs_since_halved = 0
                    K.set_value(self.model.optimizer.lr, current_lr * self.decay_multiple)

            if (self.epochs_since_halved >= 150):
                self.epochs_since_halved = 0
                K.set_value(self.model.optimizer.lr, current_lr * self.decay_multiple)

        else:
            K.set_value(self.model.optimizer.lr, self.base_lr)

        self.epochs_since_halved += 1

        return K.get_value(self.model.optimizer.lr)

