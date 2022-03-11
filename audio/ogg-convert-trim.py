from pydub import AudioSegment
import os
import pandas as pd

# Convert
mp3_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'mp3'))
ogg_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'ogg'))

# Export
for filename in os.listdir(mp3_path):
    name, ext = os.path.splitext(filename)
    if ext == ".mp3":
       mp3 = AudioSegment.from_mp3(mp3_path + "\\" + filename)
       mp3.export("{0}/{1}.ogg".format(ogg_path, name), format="ogg")
       print("{0}/{1}.ogg created.".format(ogg_path, name))
    else:
        print(name, ext)

print("Finished mp3 -> ogg conversion.")

# Trim
csv = pd.read_csv("audio/metadata.csv")

start_time = 0 # 0 sec
end_time = 30000 # 30 sec

# Export
for filename, path in enumerate(os.listdir(ogg_path)):
    ogg_file = "{0}-{1}-{2}.ogg".format(csv.Genus[filename], csv.Specific_epithet[filename], csv.Recording_ID[filename])
    audio = "{0}/{1}".format(ogg_path, ogg_file)
    try:
        audio = AudioSegment.from_ogg(audio)
    except FileNotFoundError:
        print("{} not found for trimming. Continuing to next file.".format(audio))
        continue

    if audio.duration_seconds > 30:
        audio[start_time:end_time].export(audio, format="ogg")
    else:
        print("{} already trimmed. Continuing.".format(ogg_path + "/" + ogg_file))

print("Finished trimming.")