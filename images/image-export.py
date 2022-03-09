import pandas as pd
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

df = pd.read_csv("train/train_tp.csv")

i = 1
while i < 479:
    sample_num = i
    filename = df.recording_id[sample_num] + str('.flac')
    tstart = df.t_min[sample_num] 
    tend = df.t_max[sample_num]
    y, sr = librosa.load('train/' + str(filename))

    # Mel spectrogram
    s = librosa.feature.melspectrogram(y, sr)
    mel_spectrogram = librosa.power_to_db(s, ref=np.max)
    mel_img = librosa.display.specshow(mel_spectrogram)
    plt.tight_layout()
    plt.savefig("images/{}".format(df.recording_id[sample_num], dpi=100))

    print("Image exported.")
    i += 1

    del y, sr, s, mel_spectrogram, mel_img