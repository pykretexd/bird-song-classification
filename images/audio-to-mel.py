import pandas as pd
import librosa
import librosa.display
import numpy as np
import os
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt

wav_path = "C:/Users/elev/Documents/GitHub/CNN-audio-classification/audio/wav/"

csv = pd.read_csv("C:/Users/elev/Documents/GitHub/CNN-audio-classification/audio/metadata.csv")

i = 0
for filename in os.listdir(wav_path):
    audio_file = str(csv.Genus[i]) + str("-") + str(csv.Specific_epithet[i]) + str("-") + str(csv.Recording_ID[i]) + str('.wav')
    
    try:
        y, sr = librosa.load(wav_path + str(audio_file))
    except FileNotFoundError:
        print("Audio file not found. Continuing to next file.")
        i += 1
        continue

    s = librosa.feature.melspectrogram(y, sr)
    mel_spectrogram = librosa.power_to_db(s, ref=np.max)

    mel_img = librosa.display.specshow(mel_spectrogram)
    plt.tight_layout()
    plt.savefig("C:/Users/elev/Documents/GitHub/CNN-audio-classification/images/mel/{}".format(csv.Recording_ID[i]), dpi=200)

    print("Audio file converted to image.")
    del y, sr, s, mel_spectrogram, mel_img
    i += 1