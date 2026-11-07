import importlib
import pandas as pd

print("--- 1. Testing Pandas Compiled Extensions ---")
try:
    df_test = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    print("[OK] Pandas DataFrame creation & C-engine working")
except Exception as e:
    print(f"[BLOCKED] Pandas runtime -> {type(e).__name__}: {e}")

print("\n--- 2. Testing Scikit-Learn Compiled Submodules ---")
sklearn_submodules = [
    "sklearn.utils.murmurhash",
    "sklearn.model_selection",
    "sklearn.preprocessing",
    "sklearn.metrics",
    "sklearn.linear_model",
    "sklearn.ensemble",
    "sklearn.naive_bayes"
]

for mod in sklearn_submodules:
    try:
        importlib.import_module(mod)
        print(f"[OK]      {mod}")
    except Exception as e:
        print(f"[BLOCKED] {mod} -> {type(e).__name__}: {e}")