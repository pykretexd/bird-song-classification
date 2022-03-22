import pandas as pd
import librosa
import librosa.display
import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

import_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'audio'))
export_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'image'))
df = pd.read_csv(os.path.realpath(os.path.join(os.path.dirname(__file__), 'audio', 'audio.csv')))

list = []
for i in tqdm(range(len(df))):
    name, ext = os.path.splitext(df.file_name[i])
    image = name + '.jpg'
    list.append(dict(file_name=image, label=df.label[i]))
    target = '{}\\{}'.format(import_path, df.file_name[i])
    if os.path.exists('{}\\{}'.format(export_path, image)):
        continue
    try:
        y, sr = librosa.load(target)
    except:
        continue

    mel_s = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr), ref=np.max)
    mel_img = librosa.display.specshow(mel_s)
    plt.tight_layout()
    plt.savefig('{}\\{}'.format(export_path, image), format='jpg')

    del y, sr, mel_s, mel_img

new_df = pd.DataFrame(list)
new_df.to_csv('{}\\train.csv'.format(export_path), index=False)