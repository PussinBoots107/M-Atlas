# MATLAS

MATLAS is a local Flask application for DASS-21 self-screening, IPIP-50 Big Five trait exploration, and a research-only TIPI-to-DASS depression severity model.

## Run locally on Windows

From this project folder, run:

```powershell
.\.venv\Scripts\python.exe export_metrics.py
.\.venv\Scripts\python.exe backend\app.py
```

Open `http://127.0.0.1:5000` in a browser. To use a different local port, set `PORT` before launching, for example `$env:PORT=5051`.

## Checks

```powershell
.\.venv\Scripts\python.exe verify_setup.py
.\.venv\Scripts\python.exe -m compileall backend export_metrics.py
```

The bundled Chart.js file is served locally from `frontend/vendor`, so the dashboard has no runtime CDN dependency.

## Scope and safety

The DASS-21 and TIPI results are screening and research outputs, not diagnoses. MATLAS does not store submitted questionnaire responses. For persistent or urgent mental-health concerns, seek support from a qualified professional or local emergency services.
