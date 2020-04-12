import numpy as np
import keras
from keras.models import Sequential 
from keras.layers import Dense, Dropout, LSTM, CuDNNLSTM, ConvLSTM2D
from keras.layers.core import Activation, Flatten
import matplotlib.pyplot as plt
from keras.optimizers import SGD,RMSprop,adam
from keras.models import load_model
from keras.utils import np_utils
import os, os.path
from scipy.io import wavfile
from keras.models import Model
from keras import backend as K
from random import random
from keras.callbacks import EarlyStopping, ModelCheckpoint
from  copy import deepcopy

class predict(object):

    def __init__(self, anchor, test, model_loaded, f_start, f_stop, n_chan_width):
        self.anchor = anchor
        self.test = test
        self.encoder_injected = model_loaded
        self.f_start = f_start
        self.f_stop = f_stop 
        self.n_chan_width = n_chan_width
        self.values= np.zeros(self.test.shape[0])

    def compute_distance(self):
        """
        Method helps compute the MSE between two N-d vectors and is used to make the
        Helps facilitate fast computation.                 
        """
        check = self.encoder_injected.predict(self.test)
        anchor = self.encoder_injected.predict(self.anchor)
        for j in range(0, self.test.shape[0]-1):
            # index = int(random()*10)
            index = 0
            self.values[j]=(np.square(np.subtract(anchor[index:index+1,:], check[j:j+1,:]))).mean()   
        return self.values
    
    def max_index(self, top=3):
        top_hits = []
        f_chan_low = [1190,2290]
        f_chan_high = [1350, 2360]
        copy = deepcopy(self.values)
        i=0
        while i <top:
            hit = np.argmax(copy)
            if hit< f_chan_low[0] or (hit> f_chan_high[0] and hit< f_chan_low[1]) or hit>f_chan_high[1]:
                top_hits.append(hit)
                i+=1
            copy[hit]=0
        return top_hits

    def min_index(self, top=3):
        """
        This method finds the minimum distance - used for reverse image search for signals.
        This implements the same logic as the max_index search.
        """
        top_hits = []
        copy = deepcopy(self.values)
        for i in range(0, top):
            hit = np.argmin(copy)
            top_hits.append(hit)
            copy[hit]=0
        return top_hits