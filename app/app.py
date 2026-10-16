"""Streamlit dashboard for the anemia benchmark model."""

from pathlib import Path

import pandas as pd
import streamlit as st

from utils import DEFAULT_MODEL_PATH, load_model_artifact, predict_risk
from iron5_calculator import (
    IRON5_QUESTION_KEYS,
    calculate_iron5_score,
    get_iron5_recommendation,
)

LOGO_PATH = Path(__file__).resolve().parent.parent / "MD_logo_mini.png"
IRON5_QUESTIONS = {
    "non_omnivore": "Are you a non-omnivore (vegetarian, vegan, or pescatarian)?",
    "does_not_use_iron_supplements": "Do you not use iron supplements?",
    "heavy_menstruation_discomfort": "Does heavy menstruation cause you physical discomfort?",
    "avoids_activities_due_to_menstruation": (
        "Do you avoid activities, trips, or leisure plans due to menstruation?"
    ),
    "does_not_use_hormonal_contraceptives": "Do you not use hormonal contraceptives?",
}


def render_lab_predictor() -> None:
    st.warning(
        "Research prototype only. This model predicts the Kaggle dataset's anemia label, "
        "not iron deficiency. CBC measurements may define that label, so estimates may "
        "reflect label construction rather than clinically useful prediction."
    )
    st.caption(
        "Not a medical device. Do not use for diagnosis or treatment decisions."
    )

    if not DEFAULT_MODEL_PATH.is_file():
        st.error(f"Model artifact not found: {DEFAULT_MODEL_PATH}")
        st.info(
            "Run all cells in `notebooks/anemia_dataset_eda_model_comparison.ipynb` "
            "to train and save the XGBoost model first."
        )
        return

    with st.sidebar.form("prediction_inputs"):
        st.subheader("Dataset inputs")
        gender_label = st.selectbox(
            "Gender (0 = male, 1 = female)", ["Male (0)", "Female (1)"]
        )
        hemoglobin = st.number_input(
            "Hemoglobin",
            value=13.2,
            step=0.1,
            help=(
                "A protein in red blood cells that carries oxygen to organs and tissues "
                "and transports carbon dioxide back to the lungs. The data card does not "
                "specify measurement units."
            ),
        )
        mch = st.number_input(
            "MCH",
            value=22.7,
            step=0.1,
            help=(
                "Mean corpuscular hemoglobin: the average amount of hemoglobin in each "
                "red blood cell. The data card does not specify measurement units."
            ),
        )
        mchc = st.number_input(
            "MCHC",
            value=30.4,
            step=0.1,
            help=(
                "Mean corpuscular hemoglobin concentration: the average concentration "
                "of hemoglobin inside a single red blood cell. The data card does not "
                "specify measurement units."
            ),
        )
        mcv = st.number_input(
            "MCV",
            value=85.3,
            step=0.1,
            help=(
                "Mean corpuscular volume: the average size of red blood cells. "
                "The data card does not specify measurement units."
            ),
        )
        submitted = st.form_submit_button("Estimate dataset label", type="primary")

    input_values = pd.DataFrame(
        [{
            "Gender": 0 if gender_label.startswith("Male") else 1,
            "Hemoglobin": hemoglobin,
            "MCH": mch,
            "MCHC": mchc,
            "MCV": mcv,
        }]
    )

    if submitted:
        try:
            probability = float(predict_risk(input_values).iloc[0])
        except (FileNotFoundError, TypeError, ValueError) as error:
            st.error(f"Could not run the saved model: {error}")
        else:
            st.metric("Estimated likelihood of anemia (dataset label)", f"{probability:.1%}")
            st.progress(probability)
            st.caption(
                "Target mapping from the Kaggle data card: Result = 0 (not anemic), "
                "Result = 1 (anemic). This estimates the dataset label, not an "
                "individual's clinical risk."
            )

    st.subheader("Model evaluation snapshot")
    artifact = load_model_artifact(DEFAULT_MODEL_PATH)
    metrics = artifact.get("test_metrics", {})
    metric_columns = st.columns(4)
    for column, key, label in zip(
        metric_columns,
        ["accuracy", "balanced_accuracy", "roc_auc", "auprc"],
        ["Accuracy", "Balanced accuracy", "ROC AUC", "AUPRC"],
    ):
        value = metrics.get(key)
        column.metric(label, f"{value:.3f}" if value is not None else "N/A")
    st.caption(
        "Held-out test metrics from one stratified split after exact duplicate removal. "
        "They are exploratory and may be inflated by target leakage."
    )

    with st.expander("Model details"):
        st.write("Selected inputs:", ", ".join(artifact.get("features", [])))
        st.write("Dataset: `biswaranjanrao/anemia-dataset` on Kaggle")


def render_iron5_screener() -> None:
    st.subheader("IRON-5 Lifestyle Risk Screener")
    st.warning(
        "This questionnaire and its score thresholds are not clinically validated. "
        "It is for educational and portfolio demonstration purposes only and does "
        "not constitute medical advice."
    )
    st.caption(
        "The five-question scoring framework has no not-applicable response. "
        "Menstruation-related questions may not apply to everyone."
    )

    with st.form("iron5_questionnaire"):
        responses = {}
        for question_key in IRON5_QUESTION_KEYS:
            responses[question_key] = st.radio(
                IRON5_QUESTIONS[question_key],
                options=("No", "Yes"),
                index=None,
                horizontal=True,
                key=f"iron5_{question_key}",
            )
        submitted = st.form_submit_button("Calculate Risk Score", type="primary")

    if not submitted:
        return

    if any(response is None for response in responses.values()):
        st.error("Please answer all five questions before calculating the score.")
        return

    answers = {question_key: response == "Yes" for question_key, response in responses.items()}
    score = calculate_iron5_score(answers)
    recommendation = get_iron5_recommendation(score)

    score_column, category_column = st.columns(2)
    score_column.metric("IRON-5 score", f"{score} / 5")
    score_column.progress(score / 5)

    category_message = (
        f"{recommendation['risk_category']}: {recommendation['description']}"
    )
    if score <= 1:
        category_column.success(category_message)
    elif score <= 3:
        category_column.warning(category_message)
    else:
        category_column.error(category_message)

    st.markdown("**Recommendation**")
    st.write(recommendation["recommendation"])
    st.caption(
        "Each Yes answer adds one point. This questionnaire is a lifestyle screener "
        "and does not diagnose anemia or iron deficiency."
    )


def main() -> None:
    st.set_page_config(page_title="Anemia Model Dashboard", page_icon="🩸", layout="wide")
    logo_column, title_column = st.columns([1, 11], vertical_alignment="center")
    with logo_column:
        st.image(str(LOGO_PATH), width=80)
    with title_column:
        st.title("Anemia Classification Prototype")
    st.write("Open-data research tools by Modus Data GmbH.")

    lab_tab, iron5_tab = st.tabs(
        ["Lab-Based Predictor", "IRON-5 Lifestyle Risk Screener"]
    )
    with lab_tab:
        render_lab_predictor()
    with iron5_tab:
        render_iron5_screener()


if __name__ == "__main__":
    main()