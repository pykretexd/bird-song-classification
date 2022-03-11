import pandas as pd
import librosa
import librosa.display
import numpy as np
import os
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt

wav_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'wav'))
df = pd.read_csv(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'metadata.csv')))

for i, path in enumerate(os.listdir(wav_path)):
    audio_file = '{0}-{1}-{2}.wav'.format(df.Genus[i], df.Specific_epithet[i], df.Recording_ID[i])
    output = "images/mel/{0}/{1}.png".format(df.English_name[i], df.Recording_ID[i])

    try:
        y, sr = librosa.load(wav_path + "\\" + audio_file)
        if os.path.exists(output):
            print("{} already exists. Continuing.".format(output))
            continue
        else:
            pass

    except FileNotFoundError:
        print("{} not found. Continuing.".format(audio_file))
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