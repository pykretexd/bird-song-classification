from pydub import AudioSegment
import os
import pandas as pd
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

# Opening message
print('This process will assist in trimming every audio file in the dataset.')

# User input
time = int(input('Input the desired length in seconds of the audio file: (Enter 0 to keep the original length) ')) * 1000

# Paths
mp3_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset', 'audio'))
path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'new_mp3'))

print('Beginning process...')
if time == 0:
    print('Length: unchanged')
else:
    print("Length: {} seconds".format(time / 1000))

for filename in tqdm(os.listdir(mp3_path)):
    name, ext = os.path.splitext(filename)
    if os.path.exists('{0}/{1}.mp3'.format(path, name)):
        continue
    if ext == '.mp3':
        mp3 = AudioSegment.from_mp3(mp3_path + '\\' + filename)
        if time > 0:
           mp3[0:time].export('{0}/{1}.mp3'.format(path, name), format='mp3')
        else:
            mp3.export('{0}/{1}.{2}'.format(path, name, format), format=format)

print('Finished trimming.')
