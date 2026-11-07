import os
import zipfile
import urllib.request
import pandas as pd

DATA_DIR = "data"
ZIP_PATH = os.path.join(DATA_DIR, "DASS_data_21.02.19.zip")
URL = "https://openpsychometrics.org/_rawdata/DASS_data_21.02.19.zip"

os.makedirs(DATA_DIR, exist_ok=True)

# 1. Download dataset once and cache it locally
if not os.path.exists(ZIP_PATH):
    print(f"Downloading dataset from {URL} ...")
    urllib.request.urlretrieve(URL, ZIP_PATH)
    print(f"Saved to {ZIP_PATH}")
else:
    print(f"Using cached dataset at {ZIP_PATH}")

# 2. Open archive, read codebook.txt, and load data.csv with sep="\t"
with zipfile.ZipFile(ZIP_PATH, "r") as archive:
    print("\nFiles in archive:", archive.namelist())

    with archive.open("DASS_data_21.02.19/codebook.txt") as f:
        codebook = f.read().decode("utf-8", errors="replace")

    with archive.open("DASS_data_21.02.19/data.csv") as f:
        df = pd.read_csv(f, sep="\t", low_memory=False)

print("\n=== CODEBOOK ===")
print(codebook)

print("\n=== SHAPE ===")
print(df.shape)

print("\n=== FIRST 5 ROWS (Selected Columns) ===")
print(df.iloc[:5, :12])

print("\n=== ALL COLUMNS ===")
cols = df.columns.tolist()
print(f"Total columns: {len(cols)}")
print("First 30 columns:", cols[:30])
print("Remaining columns (from index 126 onwards):", cols[126:])

print("\n=== TOP 20 COLUMNS WITH MISSING VALUES ===")
print(df.isna().sum().sort_values(ascending=False).head(20))