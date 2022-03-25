import keras
import tensorflow as tf
import os
import numpy as np
import librosa
import librosa.display
import cv2
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

bird_names = ['Common Chaffinch', 'Great Tit']

audio_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), 'audio'))
image_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), 'image'))
image_format = '.jpg'
image_size = 256

for audio_file in os.listdir(audio_folder):
    name, ext = os.path.splitext(audio_file)
    image = name + image_format
    if os.path.exists('{}\\{}'.format(image_folder, image)):
        continue

    y, sr = librosa.load('{}\\{}'.format(audio_folder, audio_file))
    mel = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr), ref=np.max)
    mel = librosa.display.specshow(mel)
    plt.tight_layout()
    plt.savefig('{}\\{}'.format(image_folder, image), format=image_format, dpi=50)

def prepare(file_path):
    image = cv2.imread('{}\\{}'.format(image_folder, file_path))
    image = image[10:230, 10:310]
    image = cv2.resize(image, (image_size, image_size))
    image = image / 255.0
    return image.reshape(-1, image_size, image_size, 1)

model = keras.models.load_model(os.path.realpath(os.path.join(os.path.dirname(__file__), 'saved-models', 'BirdSpecies-256x2-1648129701')))

prediction = model.predict([prepare('talgoxe2.jpg')])
label = bird_names[int(prediction[0][0])]
print(prediction)
print(label)
