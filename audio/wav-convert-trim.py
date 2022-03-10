from pydub import AudioSegment
import os
import pandas as pd

# Convert
path = "audio/mp3"
os.chdir(path)
mp3_files = os.listdir()

for file in mp3_files:
    name, ext = os.path.splitext(file)
    if ext == ".mp3":
       mp3 = AudioSegment.from_mp3(file)
       mp3.export("audio/wav/{0}.wav".format(name), format="wav")

# Trim
wav_path = "audio/wav/"
csv = pd.read_csv("audio/metadata.csv")

start_time = 0
end_time = 30000

i = 0
for filename in os.listdir(wav_path):
    wav_file = str(csv.Genus[i]) + str("-") + str(csv.Specific_epithet[i]) + str("-") + str(csv.Recording_ID[i]) + str('.wav')

    try:
        audio = AudioSegment.from_wav(wav_path + wav_file)
    except FileNotFoundError:
        print("Audio file not found. Continuing to next file.")
        i += 1
        continue

    extract = audio[start_time:end_time]

    extract.export(wav_path + wav_file, format="wav")

    i += 1