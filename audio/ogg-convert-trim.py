from pydub import AudioSegment
import os
import pandas as pd
from tqdm import tqdm

mp3_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'mp3'))
ogg_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'ogg'))

start_time = 0 # 0 sec
end_time = 30000 # 30 sec

print("Beginning conversion of .mp3 to .ogg:")

for filename in tqdm(os.listdir(mp3_path)):
    name, ext = os.path.splitext(filename)
    if ext == '.mp3':
       mp3 = AudioSegment.from_mp3(mp3_path + '\\' + filename)
       mp3[start_time:end_time].export('{0}/{1}.ogg'.format(ogg_path, name), format='ogg')

print('Finished .mp3 -> .ogg conversion.')