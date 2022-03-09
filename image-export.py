import pandas as pd
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

filename = str('test.mp3')
y, sr = librosa.load('train/' + str(filename))

# Mel spectrogram
s = librosa.feature.melspectrogram(y, sr)
mel_spectrogram = librosa.power_to_db(s, ref=np.max)
mel_img = librosa.display.specshow(mel_spectrogram)
plt.tight_layout()
plt.savefig("images/{}".format(filename, dpi=100))

print("Image exported.")