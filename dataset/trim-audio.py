import pandas as pd
import os
from pydub import AudioSegment
from pathlib import Path
from tqdm import tqdm

path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'audio'))
time = 15000

list = []
for folder in next(os.walk(path, '.'))[1]:
    print('\n' + folder)
    folder_path = path + '\\' + folder
    for file in tqdm(os.listdir(folder_path)):
        file_path = '{}\\{}'.format(folder_path, file)
        export_file = '{}\\{}'.format(path, file)
        list.append(dict(file_name=file, label=folder))
        if os.path.exists(export_file):
            # os.remove(file_path)
            continue
        mp3 = AudioSegment.from_mp3(file_path)
        mp3[0:time].export(export_file, format='mp3')

df = pd.DataFrame(list)
df.to_csv(path + '\\' + 'audio.csv', index=False)