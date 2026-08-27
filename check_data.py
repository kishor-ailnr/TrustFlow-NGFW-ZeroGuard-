import pandas as pd
import glob

files = glob.glob("data/*.csv")
print("Found files:", files)

df = pd.read_csv(files[0])
print("Shape:", df.shape)
print("Columns:", list(df.columns)[:10])