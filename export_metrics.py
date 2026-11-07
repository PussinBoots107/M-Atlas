import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split


PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "data" / "dass_tipi_clean.csv"
MODELS_DIR = PROJECT_DIR / "models"
TARGET_NAMES = ["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]

data_frame = pd.read_csv(DATA_PATH)
features = data_frame[[f"TIPI{number}" for number in range(1, 11)]].values
target = data_frame["depression_band"].values
_, test_features, _, test_target = train_test_split(
    features, target, test_size=0.20, random_state=42, stratify=target
)

random_forest = joblib.load(MODELS_DIR / "random_forest.joblib")
logistic_regression = joblib.load(MODELS_DIR / "logistic_regression.joblib")
scaler = joblib.load(MODELS_DIR / "scaler.joblib")
dummy = DummyClassifier(strategy="most_frequent").fit(features, target)

predictions = {
    "Dummy baseline": dummy.predict(test_features),
    "Logistic regression": logistic_regression.predict(scaler.transform(test_features)),
    "Random forest": random_forest.predict(test_features),
}

metrics = []
for name, prediction in predictions.items():
    metrics.append(
        {
            "name": name,
            "accuracy": round(float(accuracy_score(test_target, prediction)), 4),
            "macro_f1": round(float(f1_score(test_target, prediction, average="macro", zero_division=0)), 4),
        }
    )

payload = {
    "labels": TARGET_NAMES,
    "models": metrics,
    "confusion_matrix": confusion_matrix(test_target, predictions["Random forest"], labels=TARGET_NAMES).tolist(),
    "notes": "Held-out 80/20 stratified test split (random state 42). These results are research benchmarks, not diagnostic accuracy.",
}

with (MODELS_DIR / "evaluation_metrics.json").open("w", encoding="utf-8") as metrics_file:
    json.dump(payload, metrics_file, indent=2)

print("Exported models/evaluation_metrics.json")
