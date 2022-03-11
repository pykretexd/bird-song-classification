import pandas as pd
import librosa
import librosa.display
import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

wav_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'wav'))
ogg_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'ogg'))
df = pd.read_csv(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'audio', 'metadata.csv')))

ogg_or_wav = input('Proceed with .ogg or .wav? (Enter "ogg" or "wav"): ')
print('.{} selected.'.format(ogg_or_wav))

if ogg_or_wav == 'ogg':
    file_path = ogg_path
    audio_file = '{0}-{1}-{2}.ogg'

elif ogg_or_wav == 'wav':
    file_path = wav_path
    audio_file = '{0}-{1}-{2}.wav'

else:
    print('Unknown input.')

for i, path in tqdm(enumerate(os.listdir(file_path))):
    target = '{0}/{1}'.format(file_path, audio_file.format(df.Genus[i], df.Specific_epithet[i], df.Recording_ID[i])) 
    output = 'images/mel/{0}/{1}.png'.format(df.English_name[i], df.Recording_ID[i])
    try:
        y = librosa.load(target)
        if os.path.exists(output):
            print("exists")
            continue
    except FileNotFoundError:
        print("not found", target, output)
        continue

    mel_s = librosa.feature.melspectrogram(y)
    mel_spectrogram = librosa.power_to_db(mel_s, ref=np.max)
    mel_img = librosa.display.specshow(mel_spectrogram)

    plt.tight_layout()
    try:
        plt.savefig(output)
    except FileNotFoundError:
        os.makedirs(output)
        plt.savefig(output)
        print("not found")
    
    print("saved")
    del y, mel_s, mel_spectrogram, mel_img

print('.{} to Mel-Spectrogram conversion completed.'.format(ogg_or_wav))