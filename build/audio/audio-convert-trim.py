from pydub import AudioSegment
import os
import pandas as pd
from tqdm import tqdm

format = input('Please enter the format you would like to convert the mp3 files to: (wav, ogg, aac, wma) ')
mp3_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'mp3'))
path = os.path.realpath(os.path.join(os.path.dirname(__file__), format))

end_time = int(input('Please enter the desired length of the audio file: (Enter 0 to keep the original length) '))

print("Beginning conversion of .mp3 to .ogg:")

for filename in tqdm(os.listdir(mp3_path)):
    name, ext = os.path.splitext(filename)
    if not os.path.exists(path):
        os.mkdir(format)
    if os.path.exists('{0}/{1}.{2}'.format(path, name, format)):
        continue
    if ext == '.mp3':
        mp3 = AudioSegment.from_mp3(mp3_path + '\\' + filename)
        if end_time > 0:
           mp3[0:end_time].export('{0}/{1}'.format(path, name), format=format)
        else:
            mp3.export('{0}/{1}.{2}'.format(path, name, format), format=format)

print('Finished .mp3 -> {} conversion.'.format(format))
