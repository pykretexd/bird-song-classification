from pydub import AudioSegment
import os
import pandas as pd

mp3_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'mp3'))
wav_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'wav'))

start_time = 0 # 0 sec
end_time = 30000 # 30 sec

for filename in os.listdir(mp3_path):
    name, ext = os.path.splitext(filename)
    if ext == ".mp3":
       mp3 = AudioSegment.from_mp3(mp3_path + "\\" + filename)
       mp3[start_time:end_time].export("{0}/{1}.wav".format(wav_path, name), format="wav")
       print("{0}/{1}.wav created.".format(wav_path, name))
    else:
        print(name, ext)

print("Finished mp3 -> wav conversion.")