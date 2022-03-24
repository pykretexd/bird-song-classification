import tensorflow as tf
from tensorflow import keras
from keras import regularizers
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split
import os
import numpy as np
import random
import time
import warnings
warnings.filterwarnings("ignore")

directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'dataset', 'image'))
categories = next(os.walk(directory, '.'))[1]
image_size = 256

training_data = []
def create_training_data():
    for category in categories:
        path = os.path.join(directory, category)
        class_num = categories.index(category)
        for image in os.listdir(path):
            try:
                image_array = tf.io.read_file(path + '\\' + image)
                image_array = tf.image.decode_image(image_array, channels=1, dtype=tf.float32, expand_animations=False)
                image_array = tf.image.central_crop(image_array, 0.95)
                image_array = tf.image.resize(image_array, (image_size, image_size))
                training_data.append([image_array, class_num])
            except:
                pass

create_training_data()
random.shuffle(training_data)

X = []
y = []
for features, label in training_data:
    X.append(features)
    y.append(label)

X = np.array(X).reshape(-1, image_size, image_size, 1)
X = X / 255.0
y = np.array(y)

model = Sequential()

model.add(Conv2D(24, (5,5), input_shape=X.shape[1:], kernel_regularizer=regularizers.l2(0.001)))
model.add(Activation('relu'))
model.add(MaxPooling2D(strides=(3,3)))

model.add(Conv2D(36, (4,4), padding='valid', kernel_regularizer=regularizers.l2(0.001)))
model.add(Activation('relu'))
model.add(MaxPooling2D(strides=(2,2)))

model.add(Conv2D(48, (3,3), padding='valid'))
model.add(Activation('relu'))

model.add(Flatten())
model.add(Dense(60))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(
    optimizer=keras.optimizers.Adam(lr=0.0001),
    loss=[keras.losses.BinaryCrossentropy(from_logits=False)],
    metrics=["accuracy"],
)

name = 'BirdSpecies-{}x{}-{}'.format(image_size, len(np.unique(y)), int(time.time()))
tensorboard = TensorBoard(log_dir='build/logs/{}'.format(name))

model.fit(X, y, epochs=100, batch_size=32, validation_split=0.1, callbacks=[tensorboard])
model.evaluate(X, y, batch_size=32)
model.save('train/saved-models/{}'.format(name))
