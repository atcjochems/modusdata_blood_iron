"""Scoring and interpretation for the five-question IRON-5 screener."""

IRON5_QUESTION_KEYS = (
    "non_omnivore",
    "does_not_use_iron_supplements",
    "heavy_menstruation_discomfort",
    "avoids_activities_due_to_menstruation",
    "does_not_use_hormonal_contraceptives",
)


def calculate_iron5_score(answers: dict[str, bool]) -> int:
    """Return one point for each affirmative IRON-5 risk-factor answer."""
    if not isinstance(answers, dict):
        raise TypeError("answers must be a dictionary of five boolean responses.")

    missing_keys = set(IRON5_QUESTION_KEYS) - answers.keys()
    unexpected_keys = answers.keys() - set(IRON5_QUESTION_KEYS)
    if missing_keys:
        raise ValueError(f"Missing IRON-5 answers: {sorted(missing_keys)}")
    if unexpected_keys:
        raise ValueError(f"Unexpected IRON-5 answer keys: {sorted(unexpected_keys)}")
    if any(type(answers[key]) is not bool for key in IRON5_QUESTION_KEYS):
        raise TypeError("Every IRON-5 response must be True or False.")

    return sum(answers.values())


def get_iron5_recommendation(score: int) -> dict[str, str]:
    """Return the score category, description, and recommended next step."""
    if isinstance(score, bool) or not isinstance(score, int):
        raise TypeError("score must be an integer from 0 to 5.")
    if not 0 <= score <= 5:
        raise ValueError("score must be between 0 and 5.")

    if score <= 1:
        return {
            "risk_category": "Low Risk",
            "description": "Minimal lifestyle-driven risk factors identified.",
            "recommendation": (
                "Continue a balanced diet. Seek medical advice if you have symptoms "
                "or concerns about iron levels."
            ),
        }
    if score <= 3:
        return {
            "risk_category": "Moderate Risk",
            "description": "Several risk factors are present.",
            "recommendation": (
                "Consider monitoring dietary iron intake or consulting a healthcare "
                "professional for routine screening."
            ),
        }
    return {
        "risk_category": "High Risk",
        "description": "Multiple significant risk factors are present.",
        "recommendation": (
            "It is highly recommended that you consult a physician for professional "
            "evaluation and ferritin/CBC lab testing."
        ),
    }
