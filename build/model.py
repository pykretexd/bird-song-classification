import tensorflow as tf
from tensorflow import keras
from keras import layers
import os
import numpy as np
import cv2
import pandas as pd

directory = '{}\\'.format(os.path.realpath(os.path.join(os.path.dirname(__file__), 'images', 'mel')))
df = pd.read_csv(directory + '\\train.csv')

X = df["file_name"].values
labels = df["english_name"].values

y = []
for category in labels:
    class_num = labels.tolist().index(category)
    y.append(class_num)
y = np.array(y)

ds_train = tf.data.Dataset.from_tensor_slices((X, y))

def read_image(image_file, label):
    image = tf.io.read_file(directory + image_file)
    image = tf.image.decode_image(image, channels=1, dtype=tf.float32)
    return image, label

ds_train = ds_train.map(read_image).batch(2)

model = keras.Sequential(
    [
        layers.Input((160, 120, 1)),
        layers.Conv2D(24, (5,5), activation='relu'),
        layers.Conv2D(36, (4,4), activation='relu'),
        layers.Conv2D(48, (3,3), activation='relu', padding='valid'),
        layers.Flatten(),
        layers.Dense(60, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(len(np.unique(labels)), activation='softmax')
    ]
)

model.compile(
    optimizer=keras.optimizers.Adam(),
    loss=[keras.losses.SparseCategoricalCrossentropy(from_logits=True),],
    metrics=["accuracy"],
)

model.fit(ds_train, epochs=3)
