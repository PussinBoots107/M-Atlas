import json
from pathlib import Path

from flask import Blueprint

from .common import error_response


research_blueprint = Blueprint("research", __name__, url_prefix="/api/research")
METRICS_PATH = Path(__file__).resolve().parents[2] / "models" / "evaluation_metrics.json"


@research_blueprint.get("/metrics")
def research_metrics():
    try:
        with METRICS_PATH.open(encoding="utf-8") as metrics_file:
            return json.load(metrics_file)
    except FileNotFoundError:
        return error_response("Research metrics have not been exported. Run export_metrics.py locally.", 503)
    except json.JSONDecodeError:
        return error_response("Research metrics file is invalid.", 500)
