import tensorflow as tf
import pandas as pd
import keras
from keras import layers

directory = 'images/mel'
csv = pd.read_csv('audio/metadata.csv')
csv = csv.astype({'Genus': 'float32', 'Specific_epithet': 'float32', 'English_name': 'float32', 'Vocalization_type': 'float32'})

batch_size = 32
epochs = 10

file_path = []
for value in csv['Recording_ID'].values:
    file_path.append(str(value) + '.png')

label = csv['English_name'].values
ds_train = tf.data.Dataset.from_tensor_slices((file_path, label))
# train_ds = tf.keras.preprocessing.image_dataset_from_directory(dataset_path, labels=None, image_size=(640, 480), validation_split=0.1, subset='training')
# val_ds = tf.keras.preprocessing.image_dataset_from_directory(dataset_path, labels=None, image_size=(640, 480), validation_split=0.1, subset='validation')

def read_image(image_file, label):
    image = tf.io.read_file(directory + image_file)
    image = tf.image.decode_image(image, channels=1, dtype=tf.float32)
    return image, label

def augment(image, label):
    # data augmentation here
    return image, label

ds_train = ds_train.map(read_image).map(augment).batch(2)

model = keras.Sequential([
    layers.Input(shape=(640, 480, 3), batch_size=batch_size),
    layers.Conv2D(24, 5, padding='valid', activation='relu', name='L1'), # Remove padding
    layers.Conv2D(36, 4, padding='valid', activation='relu', name='L2'),
    layers.Conv2D(48, 3, padding='valid', activation='relu', name='L3'),
    layers.Dense(60, activation='relu', name='L4'),
    layers.Dense(50, activation='softmax', name='L5'), # Output units are the amount of categories used.
])

model.compile(
    optimizer='adam',
    loss=[keras.losses.SparseCategoricalCrossentropy(from_logits=True)],
    metrics=["accuracy"]
)

model.fit(ds_train, epochs=epochs)
