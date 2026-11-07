from flask import Blueprint, request

from .common import error_response, validate_answers


dass_blueprint = Blueprint("dass", __name__, url_prefix="/api/score")

SUBSCALES = {
    "depression": (2, 4, 9, 12, 15, 16, 20),
    "anxiety": (1, 3, 6, 8, 14, 18, 19),
    "stress": (0, 5, 7, 10, 11, 13, 17),
}


def severity_for(subscale, score):
    thresholds = {
        "depression": (9, 13, 20, 27),
        "anxiety": (7, 9, 14, 19),
        "stress": (14, 18, 25, 33),
    }
    labels = ("Normal", "Mild", "Moderate", "Severe", "Extremely Severe")
    for threshold, label in zip(thresholds[subscale], labels):
        if score <= threshold:
            return label
    return labels[-1]


@dass_blueprint.post("/dass21")
def score_dass21():
    try:
        answers = validate_answers(request.get_json(silent=True), 21, 0, 3, "DASS-21")
    except ValueError as error:
        return error_response(str(error))

    scores = {}
    for name, indices in SUBSCALES.items():
        score = sum(answers[index] for index in indices) * 2
        scores[name] = {"score": score, "severity": severity_for(name, score)}

    return {
        "assessment": "DASS-21",
        "scores": scores,
        "disclaimer": "This screening result is not a diagnosis. Discuss persistent or concerning symptoms with a qualified mental-health professional.",
    }
