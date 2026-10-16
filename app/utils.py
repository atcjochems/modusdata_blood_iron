"""Utilities for saved model inference."""

from pathlib import Path
from typing import Any, Mapping

import joblib
import pandas as pd


DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parent.parent / "models" / "anemia_xgb_pipeline.joblib"
)


def load_model_artifact(model_path: Path = DEFAULT_MODEL_PATH) -> Mapping[str, Any]:
    """Load and validate the model artifact created by the training notebook."""
    if not model_path.is_file():
        raise FileNotFoundError(f"No trained model found at {model_path}")

    artifact = joblib.load(model_path)
    if not isinstance(artifact, Mapping):
        raise TypeError("The saved artifact must be a mapping with model metadata.")
    if artifact.get("model") is None or not hasattr(artifact["model"], "predict_proba"):
        raise TypeError("The saved artifact must contain a model supporting predict_proba().")
    if not isinstance(artifact.get("features"), list) or not artifact["features"]:
        raise ValueError("The saved artifact must contain a non-empty feature list.")
    return artifact


def predict_risk(
    features: pd.DataFrame,
    model_path: Path = DEFAULT_MODEL_PATH,
) -> pd.Series:
    """Return probabilities for the artifact's positive class."""
    artifact = load_model_artifact(model_path)
    model = artifact["model"]
    model_features = artifact["features"]

    missing_features = sorted(set(model_features) - set(features.columns))
    if missing_features:
        raise ValueError(f"Missing required model features: {missing_features}")

    positive_class = artifact.get("positive_class", 1)
    classes = list(model.classes_)
    if positive_class not in classes:
        raise ValueError(f"Positive class {positive_class!r} is not in model classes {classes}.")

    probabilities = model.predict_proba(features.loc[:, model_features])
    if probabilities.ndim != 2 or probabilities.shape[1] != len(classes):
        raise ValueError("Model returned probabilities with an unexpected shape.")

    positive_index = classes.index(positive_class)
    return pd.Series(
        probabilities[:, positive_index],
        index=features.index,
        name="positive_class_probability",
    )