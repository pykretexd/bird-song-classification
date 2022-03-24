from numpy import number
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
        if os.path.exists('{}\\1-{}'.format(path, file)):
            list.append(dict(file_name='1-{}'.format(file), label=folder))
            continue
        elif os.path.exists('{}\\2-{}'.format(path, file)):
            list.append(dict(file_name='2-{}'.format(file), label=folder))
            continue
        elif os.path.exists('{}\\3-{}'.format(path, file)):
            list.append(dict(file_name='3-{}'.format(file), label=folder))
            continue
        elif os.path.exists('{}\\4-{}'.format(path, file)):
            list.append(dict(file_name='4-{}'.format(file), label=folder))
            continue
        elif os.path.exists('{}\\5-{}'.format(path, file)):
            list.append(dict(file_name='5-{}'.format(file), label=folder))
            continue
        elif os.path.exists('{}\\6-{}'.format(path, file)):
            list.append(dict(file_name='6-{}'.format(file), label=folder))
            continue
        elif os.path.exists('{}\\7-{}'.format(path, file)):
            list.append(dict(file_name='7-{}'.format(file), label=folder))
            continue
        elif os.path.exists('{}\\8-{}'.format(path, file)):
            list.append(dict(file_name='8-{}'.format(file), label=folder))
            continue
        
        
        mp3 = AudioSegment.from_mp3(file_path)
        number_of_exports = round(mp3.duration_seconds / time)
        print(number_of_exports)
        
        i = 1
        while i <= number_of_exports:
            end = time * i
            start = end - time
            mp3[start:end].export('{}\\{}-{}'.format(path, i, file), format='mp3')
            list.append(dict(file_name='{}-{}'.format(i, file), label=folder))
            i += 1

df = pd.DataFrame(list)
df.to_csv(path + '\\' + 'audio.csv', index=False)
