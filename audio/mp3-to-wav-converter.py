from pydub import AudioSegment
import os

path = "C:/Users/elev/Documents/GitHub/CNN-audio-classification/audio/mp3"
os.chdir(path)
audio_files = os.listdir()

for file in audio_files:
    name, ext = os.path.splitext(file)
    if ext == ".mp3":
       mp3 = AudioSegment.from_mp3(file)
       mp3.export("C:/Users/elev/Documents/GitHub/CNN-audio-classification/audio/wav/{0}.wav".format(name), format="wav")