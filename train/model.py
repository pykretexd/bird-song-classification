from sklearn import preprocessing
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.callbacks import TensorBoard
import os
import numpy as np
import pandas as pd
import random
import time
import warnings
warnings.filterwarnings("ignore")

log_name = 'Bird-cnn-200x3-{}'.format(int(time.time()))
tensorboard = TensorBoard(log_dir='build/logs/{}'.format(log_name))

directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'dataset', 'image'))

categories = next(os.walk(directory, '.'))[1]
print(categories)
image_size = 200

training_data = []
def create_training_data():
    for category in categories:
        path = os.path.join(directory, category)
        class_num = categories.index(category)
        for image in os.listdir(path):
            try:
                image_array = tf.io.read_file(path + '\\' + image)
                image_array = tf.image.decode_image(image_array, channels=3, dtype=tf.float32, expand_animations=False)
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

X = np.array(X).reshape(-1, image_size, image_size, 3)
X = X / 255.0
y = np.array(y)

model = keras.Sequential(
    [
        layers.Input((image_size, image_size, 3)),

        layers.Conv2D(24, (5,5), activation='relu'),
        layers.MaxPooling2D(strides=(3,3)),

        layers.Conv2D(36, (4,4), activation='relu', padding='valid'),
        layers.MaxPooling2D(strides=(2,2)),

        layers.Conv2D(48, (3,3), activation='relu', padding='valid'),

        layers.Flatten(),

        layers.Dense(60, activation='relu'),
        layers.Dropout(.5),

        layers.Dense(3, activation='softmax')
    ]
)

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.0001),
    loss=[keras.losses.SparseCategoricalCrossentropy(from_logits=True),],
    metrics=["accuracy"],
)

model.fit(X, y, epochs=100, batch_size=5, callbacks=[tensorboard])
results = model.evaluate(X, y, batch_size=5)
print('test loss, test acc: ' + results)
