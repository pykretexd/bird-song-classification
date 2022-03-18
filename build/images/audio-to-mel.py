import pandas as pd
import librosa
import librosa.display
import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

mel_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'mel'))
df = pd.read_csv(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'metadata.csv')))

audio_format = input('Specify the desired AUDIO format: ')
if audio_format == 'mp3' and os.path.exists(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'new_mp3'))):
    mp3_check = input('Do you want to use the modified mp3 files in "audio/new_mp3"? (y/n): ')
audio_format = audio_format.lower()
image_format = input('Specify the desired IMAGE format (jpeg, jpg, png, raw, tif, tiff): ')
image_format = image_format.lower()

if mp3_check == 'y':
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'new_mp3'))
else:
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', '{}'.format(audio_format)))

print('{0} -> {1} selected.'.format(audio_format, image_format))
print('Converting every file in {}'.format(path))

row_list = []
for i in tqdm(range(100)):
    row_list.append(dict(file_name='{0}.{1}'.format(df.Recording_ID[i], image_format), english_name=df.English_name[i]))
    audio_file = '{0}-{1}-{2}.{3}'.format(df.Genus[i], df.Specific_epithet[i], df.Recording_ID[i], audio_format)
    target = '{0}\\{1}'.format(path, audio_file)
    output = '{0}\\{1}.{2}'.format(mel_path, df.Recording_ID[i], image_format)
    if os.path.exists(output):
        continue
    try:
        y, sr = librosa.load(target)
    except:
        continue

    mel_s = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr), ref=np.max)
    mel_img = librosa.display.specshow(mel_s)
    plt.tight_layout()
    plt.savefig(output, format=image_format, dpi=50)

    del y, sr, mel_s, mel_img

new_df = pd.DataFrame(row_list, columns=['file_name', 'english_name'])
new_df.to_csv('{}\\train.csv'.format(mel_path), index=False)

print('.{0} -> {1} conversion completed.'.format(audio_format, image_format))
