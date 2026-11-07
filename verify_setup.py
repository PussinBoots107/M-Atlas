"""
Phase 0 Verification Script
Run this to confirm all required libraries import correctly.
Usage: venv\\Scripts\\python verify_setup.py
"""
import importlib.metadata

print("Checking Python environment for MATLAS...\n")

checks = []

def get_version(package_name):
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return "not found"

try:
    import flask
    checks.append(("Flask", get_version("flask"), "OK"))
except ImportError as e:
    checks.append(("Flask", str(e), "FAIL"))

try:
    import flask_cors
    checks.append(("Flask-CORS", get_version("flask-cors"), "OK"))
except ImportError as e:
    checks.append(("Flask-CORS", str(e), "FAIL"))

try:
    import pandas as pd
    checks.append(("pandas", pd.__version__, "OK"))
except ImportError as e:
    checks.append(("pandas", str(e), "FAIL"))

try:
    import numpy as np
    checks.append(("NumPy", np.__version__, "OK"))
except ImportError as e:
    checks.append(("NumPy", str(e), "FAIL"))

try:
    import sklearn
    checks.append(("scikit-learn", sklearn.__version__, "OK"))
except ImportError as e:
    checks.append(("scikit-learn", str(e), "FAIL"))

try:
    import joblib
    checks.append(("joblib", get_version("joblib"), "OK"))
except ImportError as e:
    checks.append(("joblib", str(e), "FAIL"))

# Print results
print(f"{'Library':<15} {'Version':<12} {'Status'}")
print("-" * 42)
for name, version, status in checks:
    icon = "+" if status == "OK" else "X"
    print(f"{icon} {name:<14} {version:<12} {status}")

all_ok = all(s == "OK" for _, _, s in checks)
print()
if all_ok:
    print("All checks passed. Phase 0 complete - ready to proceed to Phase 1.")
else:
    print("Some checks FAILED. Please re-run: venv\\Scripts\\pip install -r requirements.txt")
