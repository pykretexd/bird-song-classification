import pandas as pd
import librosa
import librosa.display
import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

mel_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'mel'))
df = pd.read_csv(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'metadata.csv')))

audio_format = input('Specify the desired AUDIO format: ')
if audio_format == 'mp3' and os.path.exists(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'new_mp3'))):
    mp3_check = input('Do you want to use the modified mp3 files in "audio/new_mp3"? (y/n): ')
audio_format = audio_format.lower()
image_format = input('Specify the desired IMAGE format (eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff): ')
image_format = image_format.lower()

if mp3_check == 'y':
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'new_mp3'))
else:
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', '{}'.format(audio_format)))

print('{0} -> {1} selected.'.format(audio_format, image_format))
print('Converting every file in {}'.format(path))

for i in tqdm(range(len(df))):
    audio_file = '{0}-{1}-{2}.{3}'.format(df.Genus[i], df.Specific_epithet[i], df.Recording_ID[i], audio_format)
    target = '{0}\\{1}'.format(path, audio_file)
    output = '{0}\\{1}\\{2}.png'.format(mel_path, df.English_name[i], df.Recording_ID[i])
    if os.path.exists(output):
        continue
    try:
        y, sr = librosa.load(target)
    except FileNotFoundError:
        continue

    mel_s = librosa.feature.melspectrogram(y, sr)
    mel_spectrogram = librosa.power_to_db(mel_s, ref=np.max)
    mel_img = librosa.display.specshow(mel_spectrogram)

    plt.tight_layout()
    try:
        plt.savefig(output, format=image_format)
    except FileNotFoundError:
        os.makedirs('{0}\\{1}'.format(mel_path, df.English_name[i]))
        plt.savefig(output, format=image_format)
    
    del y, sr, mel_s, mel_spectrogram, mel_img

print('.{0} -> {1} conversion completed.'.format(audio_format, image_format))
