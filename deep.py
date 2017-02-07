# from keras.models import Sequential
from keras.utils import np_utils
# from keras.layers.core import Dense, Activation, Dropout
#https://www.kaggle.com/liwste/digit-recognizer/simple-deep-mlp-with-keras/run/2666
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD

import pandas as pd
import numpy as np

loader = pd.read_csv('alignedSorted.csv',delimiter=";")
nbValue=30
msk = np.random.rand(len(loader.index)) < 0.8
print len(msk)


labels = loader.ix[:,nbValue+2].values.astype('int32')

X_train = (loader.ix[:,1:nbValue+1].values).astype('float32')[msk]
X_test = (loader.ix[:,1:nbValue+1].values).astype('float32')[~msk]
# convert list of labels to binary class matrix
y_train = np_utils.to_categorical(labels)[msk]
y_test = np_utils.to_categorical(labels)[~msk]

input_dim = X_train.shape[1]
nb_classes = y_train.shape[1]

model = Sequential()
# Dense(64) is a fully-connected layer with 64 hidden units.
# in the first layer, you must specify the expected input data shape:
# here, 20-dimensional vectors.
model.add(Dense(500, input_dim=input_dim, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.6))
model.add(Dense(250, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))
model.add(Dense(50, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(nb_classes, init='uniform'))
model.add(Activation('softmax'))

sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])
print("Training...")
model.fit(X_train, y_train, nb_epoch=20, batch_size=100, validation_split=0.1, verbose=2)

score = model.evaluate(X_test, y_test, batch_size=10000)
print score
print("%s: %.2f%%" % (model.metrics_names[1], score[1]*100))
model.save("model.keras")
model.save_weights("weights.h5py")
