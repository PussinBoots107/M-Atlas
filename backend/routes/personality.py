from flask import Blueprint, request

from .common import error_response, validate_answers


personality_blueprint = Blueprint("personality", __name__, url_prefix="/api/score")

TRAITS = {
    "Extraversion": {"items": (1, 6, 11, 16, 21, 26, 31, 36, 41, 46), "reverse": (6, 21, 31)},
    "Agreeableness": {"items": (2, 7, 12, 17, 22, 27, 32, 37, 42, 47), "reverse": (2, 12, 27, 42)},
    "Conscientiousness": {"items": (3, 8, 13, 18, 23, 28, 33, 38, 43, 48), "reverse": (8, 18, 23, 43)},
    "Emotional Stability": {"items": (4, 9, 14, 19, 24, 29, 34, 39, 44, 49), "reverse": (4, 14, 24, 34)},
    "Openness": {"items": (5, 10, 15, 20, 25, 30, 35, 40, 45, 50), "reverse": (35,)},
}

MBTI_DIMENSIONS = (
    ("E", "I"),
    ("E", "I"),
    ("E", "I"),
    ("E", "I"),
    ("S", "N"),
    ("S", "N"),
    ("S", "N"),
    ("S", "N"),
    ("T", "F"),
    ("T", "F"),
    ("T", "F"),
    ("T", "F"),
    ("J", "P"),
    ("J", "P"),
    ("J", "P"),
    ("J", "P"),
)

DIMENSION_NAMES = {
    "E": "Extraversion",
    "I": "Introversion",
    "S": "Sensing",
    "N": "Intuition",
    "T": "Thinking",
    "F": "Feeling",
    "J": "Judging",
    "P": "Perceiving",
}


@personality_blueprint.post("/personality")
def score_personality():
    try:
        answers = validate_answers(request.get_json(silent=True), 50, 1, 5, "IPIP-50")
    except ValueError as error:
        return error_response(str(error))

    traits = {}
    for name, configuration in TRAITS.items():
        adjusted_scores = []
        for item_number in configuration["items"]:
            score = answers[item_number - 1]
            adjusted_scores.append(6 - score if item_number in configuration["reverse"] else score)
        total = sum(adjusted_scores)
        traits[name] = {"total": total, "average": round(total / len(adjusted_scores), 2)}

    return {
        "assessment": "IPIP-50 Big Five",
        "traits": traits,
        "disclaimer": "Personality scores describe self-reported traits, not mental-health conditions or diagnoses.",
    }


@personality_blueprint.post("/mbti")
def score_mbti():
    try:
        answers = validate_answers(request.get_json(silent=True), 16, 1, 5, "MBTI-style preference quiz")
    except ValueError as error:
        return error_response(str(error))

    scores = {letter: 0 for letter in DIMENSION_NAMES}
    for answer, (left, right) in zip(answers, MBTI_DIMENSIONS):
        scores[left] += answer
        scores[right] += 6 - answer

    pairs = (("E", "I"), ("S", "N"), ("T", "F"), ("J", "P"))
    letters = [left if scores[left] >= scores[right] else right for left, right in pairs]
    dimensions = [
        {
            "left": DIMENSION_NAMES[left],
            "left_score": scores[left],
            "right": DIMENSION_NAMES[right],
            "right_score": scores[right],
        }
        for left, right in pairs
    ]
    return {
        "assessment": "MBTI-style preference quiz",
        "type": "".join(letters),
        "dimensions": dimensions,
        "disclaimer": "This is an informal preference reflection, not the official Myers-Briggs Type Indicator assessment or a diagnosis.",
    }


@personality_blueprint.post("/enneagram")
def score_enneagram():
    try:
        answers = validate_answers(request.get_json(silent=True), 18, 1, 5, "Enneagram reflection")
    except ValueError as error:
        return error_response(str(error))

    styles = [
        {"number": number, "score": answers[(number - 1) * 2] + answers[(number - 1) * 2 + 1]}
        for number in range(1, 10)
    ]
    styles.sort(key=lambda style: style["score"], reverse=True)
    return {
        "assessment": "Enneagram reflection",
        "leading_style": styles[0]["number"],
        "styles": styles,
        "disclaimer": "This informal reflection is not a clinical assessment or a definitive Enneagram typing system.",
    }


@personality_blueprint.post("/social-energy")
def score_social_energy():
    try:
        answers = validate_answers(request.get_json(silent=True), 12, 1, 5, "social-energy quiz")
    except ValueError as error:
        return error_response(str(error))

    extraversion = sum(answers[index] for index in (0, 2, 4, 6, 8, 10))
    introversion = sum(answers[index] for index in (1, 3, 5, 7, 9, 11))
    difference = extraversion - introversion
    if difference >= 5:
        style = "Extrovert-leaning"
    elif difference <= -5:
        style = "Introvert-leaning"
    else:
        style = "Ambivert"

    return {
        "assessment": "Social-energy reflection",
        "style": style,
        "scores": {"extraversion": extraversion, "introversion": introversion},
        "disclaimer": "This is a self-reflection on social energy, not a fixed label or mental-health diagnosis.",
    }
