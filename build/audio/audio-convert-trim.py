from pydub import AudioSegment
import os
import pandas as pd
from tqdm import tqdm

print('This process will assist in converting and/or trimming every audio file in the dataset.')
print('Please make sure the dataset exists in: "build/audio/mp3"')

format = input('Input the desired format to convert the mp3 files to: (e.g. mp3, wav, ogg, aac, wma) ')
time = int(input('Input the desired length in seconds of the audio file: (Enter 0 to keep the original length) ')) * 1000

mp3_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'mp3'))
if format == 'mp3':
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'new_mp3'))
else:
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), format))

print('Beginning process...')
print('Output format: {}'.format(format))
if time == 0:
    print('Length: unchanged')
else:
    print("Length: {} seconds".format(time / 1000))

for filename in tqdm(os.listdir(mp3_path)):
    name, ext = os.path.splitext(filename)
    if not os.path.exists(path):
        if format == 'mp3':
            try:
                os.mkdir(os.path.realpath(os.path.join(os.path.dirname(__file__))) + '/' + 'new_mp3')
            except FileExistsError:
                pass
        else:
            try:
                os.mkdir(os.path.realpath(os.path.join(os.path.dirname(__file__))) + '/' + format)
            except FileExistsError:
                pass
    if os.path.exists('{0}/{1}.{2}'.format(path, name, format)):
        continue
    if ext == '.mp3':
        mp3 = AudioSegment.from_mp3(mp3_path + '\\' + filename)
        if time > 0:
           mp3[0:time].export('{0}/{1}.{2}'.format(path, name, format), format=format)
        else:
            mp3.export('{0}/{1}.{2}'.format(path, name, format), format=format)

print('Finished .mp3 -> {} conversion.'.format(format))
