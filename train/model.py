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

log_name = 'Bird-cnn-200x200-{}'.format(int(time.time()))
tensorboard = TensorBoard(log_dir='build/logs/{}'.format(log_name))
directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'dataset', 'image')) + '\\'

df = pd.read_csv(directory + 'train.csv')

X = df["file_name"].values
random.shuffle(X)

labels = df["label"].values
y = []
for category in labels:
    class_num = labels.tolist().index(category)
    y.append(class_num)
y = np.array(y)
y = np.divide(y, 65) # Divide by number per label
print(y.shape)

ds_train = tf.data.Dataset.from_tensor_slices((X, y))

def read_image(image_file, label):
    image = tf.io.read_file(directory + image_file)
    image = tf.image.decode_image(image, channels=3, dtype=tf.float32, expand_animations=False)
    return image, label

def augment(image, label):
    image = tf.image.central_crop(image, 0.95)
    image = tf.image.resize(image, (200, 200))
    return image, label

ds_train = ds_train.map(read_image).map(augment).batch(2)

model = keras.Sequential(
    [
        layers.Input((200, 200, 3)),

        layers.Conv2D(24, (5,5), activation='relu'),
        layers.MaxPooling2D(strides=(3,3)),

        layers.Conv2D(36, (4,4), activation='relu', padding='valid'),
        layers.MaxPooling2D(strides=(2,2)),

        layers.Conv2D(48, (3,3), activation='relu', padding='valid'),

        layers.Flatten(),

        layers.Dense(60, activation='relu'),
        layers.Dropout(.5),

        layers.Dense(len(np.unique(labels)), activation='softmax')
    ]
)

model.compile(
    optimizer=keras.optimizers.RMSprop(learning_rate=0.00001),
    loss=[keras.losses.SparseCategoricalCrossentropy(from_logits=True),],
    metrics=["accuracy"],
)

model.fit(ds_train, epochs=100, batch_size=32, callbacks=[tensorboard])
model.evaluate(ds_train, batch_size=32)
