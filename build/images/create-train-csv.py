import pandas as pd
import os

dir = os.path.realpath(os.path.join(os.path.dirname(__file__), 'metadata.csv'))
export_destination = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'images', 'mel'))
df = pd.read_csv(dir, usecols=[0, 3])
df.to_csv("{}\\train.csv".format(export_destination), index=False)
