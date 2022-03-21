import pandas as pd
import librosa
import librosa.display
import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

import_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'new_mp3'))
export_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset', 'image'))
df = pd.read_csv(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset', 'train.csv')))

row_list = []
for i in tqdm(range(len(df))):
    row_list.append(dict(filename='{}.jpg'.format(df.filename[i]), english_name=df.english_name[i]))
    target = '{}\\{}'.format(import_path, df.filename[i])
    output = '{}\\{}.jpg'.format(export_path, df.filename[i])
    if os.path.exists(output):
        continue
    try:
        y, sr = librosa.load(target)
    except:
        continue

    mel_s = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr), ref=np.max)
    mel_img = librosa.display.specshow(mel_s)
    plt.tight_layout()
    plt.savefig(output, format='jpg', dpi=50)

    del y, sr, mel_s, mel_img

new_df = pd.DataFrame(row_list, columns=['file_name', 'english_name'])
new_df.to_csv('{}\\train.csv'.format(export_path), index=False)
