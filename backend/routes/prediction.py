from pathlib import Path

import joblib
from flask import Blueprint, current_app, request

from .common import error_response, validate_answers


prediction_blueprint = Blueprint("prediction", __name__, url_prefix="/api/predict")
PROJECT_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_DIR / "models" / "random_forest.joblib"


def get_model():
    model = current_app.extensions.get("tipi_model")
    if model is None:
        model = joblib.load(MODEL_PATH)
        current_app.extensions["tipi_model"] = model
    return model


@prediction_blueprint.post("/tipi-depression")
def predict_tipi_depression():
    try:
        answers = validate_answers(request.get_json(silent=True), 10, 1, 7, "TIPI")
    except ValueError as error:
        return error_response(str(error))

    try:
        model = get_model()
        probabilities = model.predict_proba([answers])[0]
        probability_by_label = {
            label: round(float(probability) * 100, 2)
            for label, probability in zip(model.classes_, probabilities)
        }
        prediction = model.predict([answers])[0]
    except (OSError, ValueError) as error:
        current_app.logger.exception("Could not load or run the local TIPI model")
        return error_response(f"The local research model is unavailable: {error}", 503)

    return {
        "model": "Random Forest (TIPI to DASS-42 depression severity)",
        "predicted_band": prediction,
        "probabilities": probability_by_label,
        "disclaimer": "Research-only estimate. A personality questionnaire cannot diagnose depression or replace clinical assessment.",
    }
