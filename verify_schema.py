import zipfile
import pandas as pd

ZIP_PATH = "data/DASS_data_21.02.19.zip"

with zipfile.ZipFile(ZIP_PATH, "r") as archive:
    with archive.open("DASS_data_21.02.19/data.csv") as f:
        df = pd.read_csv(f, sep="\t", low_memory=False)

depression_cols = [
    "Q3A", "Q5A", "Q10A", "Q13A", "Q16A", "Q17A", "Q21A",
    "Q24A", "Q26A", "Q31A", "Q34A", "Q37A", "Q38A", "Q42A"
]
tipi_cols = [f"TIPI{i}" for i in range(1, 11)]
fake_vcl_cols = ["VCL6", "VCL9", "VCL12"]

print("=== 1. DASS-42 DEPRESSION ITEMS VALUE CHECK (Expected: 1 to 4) ===")
dass_vals = pd.unique(df[depression_cols].values.ravel())
print("Unique values across DASS depression items:", sorted(dass_vals))
invalid_dass_rows = (df[depression_cols] < 1).any(axis=1) | (df[depression_cols] > 4).any(axis=1)
print("Rows with out-of-range DASS depression answers:", invalid_dass_rows.sum())

print("\n=== 2. TIPI ITEMS VALUE CHECK (Expected: 1 to 7; 0 = skipped/missing) ===")
tipi_vals = pd.unique(df[tipi_cols].values.ravel())
print("Unique values across TIPI1-TIPI10:", sorted(tipi_vals))
invalid_tipi_rows = (df[tipi_cols] < 1).any(axis=1) | (df[tipi_cols] > 7).any(axis=1)
print("Rows with skipped/0 or invalid TIPI answers:", invalid_tipi_rows.sum())
print("Per-column count of 0s in TIPI:")
print((df[tipi_cols] == 0).sum())

print("\n=== 3. FAKE WORD VALIDITY CHECK (VCL6, VCL9, VCL12) ===")
failed_vcl_rows = (df[fake_vcl_cols] == 1).any(axis=1)
print("Rows that checked at least one fake word:", failed_vcl_rows.sum())

print("\n=== 4. DUPLICATE CHECK ===")
print("Exact duplicate rows (all columns):", df.duplicated().sum())

# Preview how many clean rows remain if we require valid DASS, valid TIPI (1-7), and passing VCL check
clean_mask = (~invalid_dass_rows) & (~invalid_tipi_rows) & (~failed_vcl_rows)
df_clean = df[clean_mask].copy()
print(f"\nTotal initial rows : {len(df)}")
print(f"Clean valid rows   : {len(df_clean)} ({len(df_clean)/len(df)*100:.1f}%)")

# Compute DASS-42 Depression Score (subtracting 1 from each 1-4 item so each is 0-3)
df_clean["depression_score"] = (df_clean[depression_cols] - 1).sum(axis=1)
print("\n=== 5. DEPRESSION SCORE SUMMARY (Clean Rows, Range 0-42) ===")
print(df_clean["depression_score"].describe())

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
band_order = ["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]
print("\n=== 6. TARGET CLASS DISTRIBUTION (5-Class Severity Bands) ===")
counts = df_clean["depression_band"].value_counts().reindex(band_order)
pcts = (counts / len(df_clean) * 100).round(2)
print(pd.DataFrame({"Count": counts, "Percentage (%)": pcts}))