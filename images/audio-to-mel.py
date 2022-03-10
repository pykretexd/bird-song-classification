import pandas as pd
import librosa
import librosa.display
import numpy as np
import os
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt

wav_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'wav'))

csv = pd.read_csv(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'metadata.csv')))

i = 0
for filename in os.listdir(wav_path):
    audio_file = str(csv.Genus[i]) + str("-") + str(csv.Specific_epithet[i]) + str("-") + str(csv.Recording_ID[i]) + str('.wav')
    output = "images/mel/{0}/{1}.png".format(csv.English_name[i], csv.Recording_ID[i])

    try:
        y, sr = librosa.load(wav_path + "\\" + audio_file)
    except FileNotFoundError:
        print(wav_path + "\\" + audio_file + " not found. Continuing.")
        i += 1
        continue

    mel_s = librosa.feature.melspectrogram(y, sr)
    mel_spectrogram = librosa.power_to_db(mel_s, ref=np.max)

    mel_img = librosa.display.specshow(mel_spectrogram)
    plt.tight_layout()
    try:
        plt.savefig(output)
    except FileNotFoundError:
        print("Creating {}".format(output))
        os.makedirs(output)
        plt.savefig(output)

    print("Conversion of {} successful.".format(output))
    del y, sr, mel_s, mel_spectrogram, mel_img
    i += 1