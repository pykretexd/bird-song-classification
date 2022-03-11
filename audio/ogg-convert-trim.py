from pydub import AudioSegment
import os
import pandas as pd

# Convert
path = "audio/mp3"
os.chdir(path)
mp3_files = os.listdir()

# Export
for file in mp3_files:
    name, ext = os.path.splitext(file)
    if ext == ".mp3":
       mp3 = AudioSegment.from_mp3(file)
       mp3.export("audio/wav/{0}.ogg".format(name), format="ogg")

# Trim
ogg_path = "audio/ogg/"
csv = pd.read_csv("audio/metadata.csv")

start_time = 0 # 0 sec
end_time = 30000 # 30 sec

# Export
for filename in os.listdir(ogg_path):
    ogg_file = "{0}-{1}-{2}.ogg".format(csv.Genus[filename], csv.Specific_epithet[filename], csv.Recording_ID[filename])

    try:
        audio = AudioSegment.from_wav(ogg_path + ogg_file)
    except FileNotFoundError:
        print("Audio file not found. Continuing to next file.")
        continue

    extract = audio[start_time:end_time]

    extract.export(ogg_path + ogg_file, format="ogg")