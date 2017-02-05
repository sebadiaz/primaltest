import csv,random,time
from datetime import datetime
from operator import itemgetter, attrgetter, methodcaller
import sklearn.preprocessing as preprocessing
import numpy as np
import keras
from keras.utils import np_utils
# from keras.layers.core import Dense, Activation, Dropout
#https://www.kaggle.com/liwste/digit-recognizer/simple-deep-mlp-with-keras/run/2666
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD

import pandas as pd
import numpy as np
class Action:
        def __init__(self, idref, date, ouverture,haut,bas,fermeture,nbTitre):
                self.idref = idref
                self.date = date
                self.mktime = time.mktime(date.timetuple())
                self.sortKey = idref +"-" + str(self.mktime)
                self.ouverture = float(ouverture.replace(",", "."))
                self.haut = float(haut.replace(",", "."))
                self.bas = float(bas.replace(",", "."))
                self.fermeture=float(fermeture.replace(",", "."))
                self.nbTitre=nbTitre
        def __repr__(self):
                return repr((self.idref, self.date, self.ouverture,self.haut,self.bas,self.fermeture,self.nbTitre))

def getKey(custom):
      return custom.sortKey

student_tuples = []
with open('complete.csv', 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')

     for row in spamreader:
         idref = row[0]
         datetime_object = datetime.strptime(row[1], '%d/%m/%y')
         ouverture=row[2]
         haut=row[3]
         bas=row[4]
         fermeture=row[5]
         nbTitre=row[6]
         student_tuples.append(Action(idref,datetime_object,ouverture,haut,bas,fermeture,nbTitre))
         if random.random() < 0.00001 :
                 print "."
         
print "sort alogo"
savedSorted=sorted(student_tuples, key=getKey)
input_dim = 30
nb_classes = 3
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
model.load_weights("weights.h5py")
sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])
refidref=""
listValues=[]
nbValue=30
decay=1
ecart=2
with open('selectedScoredSorted.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    head=["X{:02d}".format(x) for x in range(nbValue)]
    spamwriter.writerow(["id"]+head+["taux","score"])
    for row in savedSorted:
        if refidref=="":
                refidref=row.idref
        if refidref!=row.idref:
                if len(listValues)-nbValue>=0:
                        listValues[len(listValues)-nbValue:len(listValues)]
                        norm =np.array(listValues[len(listValues)-nbValue:len(listValues)]).astype('float32')
                        simul=preprocessing.scale(norm).reshape((1,nbValue))
                        predicte=model.predict( np.asarray(simul).astype('float32') , batch_size=32, verbose=1)
                        spamwriter.writerow([refidref]+predicte[0].tolist())                        
                refidref=row.idref               
        listValues.append(row.fermeture)
                
