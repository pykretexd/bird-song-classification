from sre_parse import CATEGORIES
import pandas as pd
import numpy as np
import os
import cv2
import random
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D

df = pd.read_csv(os.path.realpath(os.path.join(os.path.dirname(__file__), 'audio', 'metadata.csv')))
df = df.drop_duplicates(subset='English_name', keep='first')

CATEGORIES = df['English_name'].values
CATEGORIES = CATEGORIES.tolist()
DATADIR = os.path.realpath(os.path.join(os.path.dirname(__file__), 'images', 'mel'))
IMG_SIZE = 480

training_data = []

def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR,category)
        class_num = CATEGORIES.index(category)
        try:
            for img in os.listdir(path):
                try:
                    img_array = cv2.imread(os.path.join(path, img))
                    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                    training_data.append([new_array, class_num])
                except:
                    pass
        except FileNotFoundError:
            CATEGORIES.remove(category)

create_training_data()
random.shuffle(training_data)
X = []
y = []

for features,label in training_data:
    X.append(features)
    y.append(label)

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

X = X/255.0

model = Sequential()

model.add(Conv2D(256, (3, 3), input_shape=X.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(256, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())

model.add(Dense(64))

model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='category_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X, y, batch_size=32, epochs=3, validation_split=0.1)
