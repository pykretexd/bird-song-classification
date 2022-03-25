import keras
import os
import numpy as np
import pandas as pd
import librosa
import librosa.display
import cv2
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

bird_names = pd.read_csv('test/bird_names.csv')
bird_names = bird_names['English_name'].values.tolist()

audio_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), 'audio'))
image_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), 'image'))
image_format = 'jpg'
image_size = 256

for audio_file in os.listdir(audio_folder):
    y, sr = librosa.load('{}\\{}'.format(audio_folder, audio_file))
    mel = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr), ref=np.max)
    mel = librosa.display.specshow(mel)

    name, ext = os.path.splitext(audio_file)
    plt.tight_layout()
    plt.savefig('{}\\{}.{}'.format(image_folder, name, image_format), format=image_format, dpi=50)

def prepare(file_path):
    image = cv2.imread('{}\\{}'.format(image_folder, file_path))
    image = image[10:230, 10:310]
    image = cv2.resize(image, (image_size, image_size))
    return image.reshape(-1, image_size, image_size, 1)

model = keras.models.load_model(os.path.realpath(os.path.join(os.path.dirname(__file__), 'saved_model', 'BirdSpecies-256x2-1648129701')))

prediction = model.predict([prepare('talgoxe2.jpg')])
print(bird_names[np.argmax(prediction[0])])
