import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

# 1. Load Clean Dataset
DATA_PATH = "data/dass_tipi_clean.csv"
print(f"Loading {DATA_PATH} ...")
df = pd.read_csv(DATA_PATH)

tipi_cols = [f"TIPI{i}" for i in range(1, 11)]
X = df[tipi_cols].values
y = df["depression_band"].values

# Standard severity order for evaluation display
target_names = ["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]

# 2. Stratified 80/20 Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Dataset Split: {len(X_train)} train samples, {len(X_test)} test samples.")

# 3. Model 1: Baseline (Most Frequent Class)
dummy = DummyClassifier(strategy="most_frequent")
dummy.fit(X_train, y_train)
y_pred_dummy = dummy.predict(X_test)
dummy_acc = accuracy_score(y_test, y_pred_dummy)
dummy_f1_macro = f1_score(y_test, y_pred_dummy, average="macro", zero_division=0)

print("\n==========================================")
print("1. BASELINE: DUMMY CLASSIFIER (Most Frequent)")
print("==========================================")
print(f"Test Accuracy    : {dummy_acc:.4f} ({dummy_acc*100:.2f}%)")
print(f"Test Macro F1    : {dummy_f1_macro:.4f}")

# 4. Model 2: Logistic Regression (with Scaler)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train_scaled, y_train)
y_pred_lr = log_reg.predict(X_test_scaled)
lr_acc = accuracy_score(y_test, y_pred_lr)
lr_f1_macro = f1_score(y_test, y_pred_lr, average="macro")

print("\n==========================================")
print("2. CANDIDATE: LOGISTIC REGRESSION")
print("==========================================")
print(f"Test Accuracy    : {lr_acc:.4f} ({lr_acc*100:.2f}%)")
print(f"Test Macro F1    : {lr_f1_macro:.4f}")
print("\nClassification Report (Logistic Regression):")
print(classification_report(y_test, y_pred_lr, labels=target_names, zero_division=0))

# 5. Model 3: Random Forest Classifier
rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
rf_acc = accuracy_score(y_test, y_pred_rf)
rf_f1_macro = f1_score(y_test, y_pred_rf, average="macro")

print("\n==========================================")
print("3. CANDIDATE: RANDOM FOREST (max_depth=10)")
print("==========================================")
print(f"Test Accuracy    : {rf_acc:.4f} ({rf_acc*100:.2f}%)")
print(f"Test Macro F1    : {rf_f1_macro:.4f}")
print("\nClassification Report (Random Forest):")
print(classification_report(y_test, y_pred_rf, labels=target_names, zero_division=0))

# 6. Confusion Matrix Comparison
print("\n==========================================")
print("CONFUSION MATRIX (Logistic Regression)")
print(f"Labels: {target_names}")
print("==========================================")
cm_lr = confusion_matrix(y_test, y_pred_lr, labels=target_names)
print(pd.DataFrame(cm_lr, index=[f"Actual {n}" for n in target_names], columns=[f"Pred {n}" for n in target_names]))

# 7. Save model artifacts and test metrics for backend/dashboard
os.makedirs("models", exist_ok=True)
joblib.dump(log_reg, "models/logistic_regression.joblib")
joblib.dump(scaler, "models/scaler.joblib")
joblib.dump(rf, "models/random_forest.joblib")

print("\nModels successfully saved to 'models/' folder.")