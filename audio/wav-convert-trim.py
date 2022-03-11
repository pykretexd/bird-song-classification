from pydub import AudioSegment
import os
import pandas as pd
from tqdm import tqdm

mp3_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'mp3'))
wav_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'wav'))

start_time = 0 # 0 sec
end_time = 30000 # 30 sec

print("Beginning conversion of .mp3 to .wav:")

for filename in tqdm(os.listdir(mp3_path)):
    name, ext = os.path.splitext(filename)
    if ext == ".mp3" and os.path.exists(filename) == False:
       mp3 = AudioSegment.from_mp3(mp3_path + "\\" + filename)
       mp3[start_time:end_time].export("{0}/{1}.wav".format(wav_path, name), format="wav")

print("Finished .mp3 -> .wav conversion.")