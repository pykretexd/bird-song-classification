from pydub import AudioSegment
import os
import pandas as pd

path = "audio/wav/"

csv = pd.read_csv("audio/metadata.csv")

start_time = 0
end_time = 30000

i = 0
for filename in os.listdir(path):
    audio_file = str(csv.Genus[i]) + str("-") + str(csv.Specific_epithet[i]) + str("-") + str(csv.Recording_ID[i]) + str('.wav')

    try:
        audio = AudioSegment.from_wav(path + audio_file)
    except FileNotFoundError:
        print("Audio file not found. Continuing to next file.")
        i += 1
        continue

    extract = audio[start_time:end_time]

    extract.export(path + audio_file, format="wav")

    i += 1