from flask import jsonify


def error_response(message, status=400):
    return jsonify({"error": message}), status


def validate_answers(payload, expected_count, minimum, maximum, label):
    if not isinstance(payload, dict):
        raise ValueError("A JSON object is required.")

    answers = payload.get("answers")
    if not isinstance(answers, list) or len(answers) != expected_count:
        raise ValueError(f"{label} requires exactly {expected_count} answers.")

    if any(isinstance(answer, bool) or not isinstance(answer, int) for answer in answers):
        raise ValueError("All answers must be whole numbers.")

    if any(answer < minimum or answer > maximum for answer in answers):
        raise ValueError(f"Each answer must be between {minimum} and {maximum}.")

    return answers
