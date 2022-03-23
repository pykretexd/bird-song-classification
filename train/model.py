import tensorflow as tf
from tensorflow import keras
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

model.add(Conv2D(64, (3,3), input_shape=X.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D(64, (3,3), input_shape=X.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D((2,2)))

model.add(Flatten())
model.add(Dense(64))

model.add(Dense(len(np.unique(y))))
model.add(Activation('sigmoid'))

model.compile(
    optimizer=keras.optimizers.Adam(),
    loss=[keras.losses.BinaryCrossentropy(from_logits=False)],
    metrics=["accuracy"],
)

# log_name = 'BirdSpecies-{}x{}-{}'.format(image_size, len(np.unique(y)), int(time.time()))
# tensorboard = TensorBoard(log_dir='build/logs/{}'.format(log_name))

model.fit(X, y, epochs=10, batch_size=8, validation_split=0.1)
model.evaluate(X, y, batch_size=2)
