import pandas as pd
import librosa
import librosa.display
import numpy as np
import os
import skimage.io
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

def scale_minmax(X, min=0.0, max=1.0):
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std * (max - min) + min
    return X_scaled

row_list = []
for i in tqdm(range(250)):
    audio_file = '{0}-{1}-{2}.{3}'.format(df.Genus[i], df.Specific_epithet[i], df.Recording_ID[i], audio_format)
    target = '{0}\\{1}'.format(path, audio_file)
    output = '{0}\\{1}.{2}'.format(mel_path, df.Recording_ID[i], image_format)
    if os.path.exists(output):
        row_list.append(dict(file_name='{0}.{1}'.format(df.Recording_ID[i], image_format), english_name=df.English_name[i]))
        continue
    try:
        y, sr = librosa.load(target)
    except:
        continue

    mel_s = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_s = np.log(mel_s + 1e-9)
    mel_img = librosa.display.specshow(mel_s)
    mel_img = scale_minmax(mel_s, 0, 255).astype(np.uint8)
    skimage.io.imsave(output, mel_img)

    row_list.append(dict(file_name='{0}.{1}'.format(df.Recording_ID[i], image_format), english_name=df.English_name[i]))

    del y, sr, mel_s, mel_img

new_df = pd.DataFrame(row_list, columns=['file_name', 'english_name'])
new_df.to_csv('{}\\train.csv'.format(mel_path), index=False)

print('.{0} -> {1} conversion completed.'.format(audio_format, image_format))
