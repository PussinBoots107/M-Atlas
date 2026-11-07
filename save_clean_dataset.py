import os
import zipfile
import pandas as pd

ZIP_PATH = "data/DASS_data_21.02.19.zip"
CLEAN_CSV_PATH = "data/dass_tipi_clean.csv"

# 1. Load raw dataset
with zipfile.ZipFile(ZIP_PATH, "r") as archive:
    with archive.open("DASS_data_21.02.19/data.csv") as f:
        df = pd.read_csv(f, sep="\t", low_memory=False)

depression_cols = [
    "Q3A", "Q5A", "Q10A", "Q13A", "Q16A", "Q17A", "Q21A",
    "Q24A", "Q26A", "Q31A", "Q34A", "Q37A", "Q38A", "Q42A"
]
tipi_cols = [f"TIPI{i}" for i in range(1, 11)]
fake_vcl_cols = ["VCL6", "VCL9", "VCL12"]

# 2. Filter invalid rows
valid_dass = (df[depression_cols] >= 1).all(axis=1) & (df[depression_cols] <= 4).all(axis=1)
valid_tipi = (df[tipi_cols] >= 1).all(axis=1) & (df[tipi_cols] <= 7).all(axis=1)
passed_vcl = (df[fake_vcl_cols] == 0).all(axis=1)

clean_mask = valid_dass & valid_tipi & passed_vcl
df_clean = df.loc[clean_mask].copy()

# 3. Calculate DASS-42 depression score (shift 1-4 to 0-3)
df_clean["depression_score"] = (df_clean[depression_cols] - 1).sum(axis=1)

# 4. Map score to standard DASS-42 severity band
def assign_severity_band(score):
    if score <= 9:
        return "Normal"
    elif score <= 13:
        return "Mild"
    elif score <= 20:
        return "Moderate"
    elif score <= 27:
        return "Severe"
    else:
        return "Extremely Severe"

df_clean["depression_band"] = df_clean["depression_score"].apply(assign_severity_band)

# 5. Keep only features and target variables
export_cols = tipi_cols + ["depression_score", "depression_band"]
df_clean = df_clean[export_cols]

# 6. Save clean file
df_clean.to_csv(CLEAN_CSV_PATH, index=False)

print(f"Clean dataset saved to: {CLEAN_CSV_PATH}")
print(f"Shape: {df_clean.shape}")
print("\nFirst 3 rows:")
print(df_clean.head(3))