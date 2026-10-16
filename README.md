# Iron Deficiency Risk App

An open-data portfolio project from Modus Data GmbH exploring whether routinely collected health measurements can help identify anemia and low iron status. The project is intended to demonstrate a careful, reproducible machine-learning workflow, from public data exploration through model evaluation and a small interactive application.

This is a research and demonstration project, not a medical device. It does not diagnose anemia or iron deficiency, and it must not be used to make decisions about an individual's care. The notebook runs exploratory baseline models, but no clinically validated or app-ready model exists.

## Repository Outline

```text
.
├── data/              # Data acquisition notes; keep downloaded data out of Git
├── notebooks/         # EDA and model comparison notebooks
├── models/            # Locally generated model artifacts
├── app/
│   ├── app.py              # Streamlit tabs for CBC prediction and IRON-5
│   ├── iron5_calculator.py # IRON-5 score and interpretation logic
│   └── utils.py            # Saved-model prediction wrapper
├── requirements.txt
└── README.md
```

## Data and Methodology

The first exploratory dataset is the [Anemia Dataset on Kaggle](https://www.kaggle.com/datasets/biswaranjanrao/anemia-dataset). Its six columns are `Gender`, `Hemoglobin`, `MCH`, `MCHC`, `MCV`, and `Result`. The initial analysis is in [the EDA and model comparison notebook](notebooks/anemia_dataset_eda_model_comparison.ipynb). The Kaggle page reports `Result` as 0 = not anemic and 1 = anemic, and lists its license as unknown; verify provenance and reuse terms before redistribution or commercial use.

This dataset is an anemia dataset, not a dataset specifically labeled for iron deficiency. Since the label may be defined from the CBC values also present as predictors, target leakage is a major risk. The notebook treats its scores as exploratory only. The broader project workflow is:

1. Verify dataset provenance, license, label construction, and intended population.
2. Explore missingness, class balance, distributions, duplicates, and potential sources of leakage.
3. Compare baseline models using separate train, validation, and test partitions.
4. Evaluate calibration, subgroup performance, and limitations on appropriate external data.
5. Save a documented model artifact and connect it to the app only after evaluation is reviewed.

To download the Kaggle dataset, configure the Kaggle CLI credentials securely and run `kaggle datasets download -d biswaranjanrao/anemia-dataset -p data --unzip`. See [data/README.md](data/README.md) for details. Downloaded CSVs are excluded from Git.

## Run Locally

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# In VS Code, open the notebook and choose Run All to write the model artifact.
streamlit run app/app.py
```

The Streamlit dashboard provides a lab-based anemia predictor and an IRON-5 lifestyle questionnaire. The model is an exploratory anemia-label demonstration, not a validated iron-deficiency model. The IRON-5 score bands are implemented as a portfolio demonstration and are not clinically validated. The questionnaire does not constitute medical advice.

## Project Status

- [x] Repository scaffold and Streamlit entry point
- [x] Create first-pass EDA and LR/XGBoost comparison notebook
- [x] Add IRON-5 questionnaire scoring demo and Streamlit tab
- [x] Show score bands and recommendations in the dashboard
- [ ] Verify data provenance, label construction, and license
- [ ] Review leakage risk and identify an appropriate iron-deficiency dataset
- [ ] Validate models on an independent, clinically relevant cohort
- [ ] Clinically validate the IRON-5 questions and score thresholds
- [ ] Integrate a reviewed model artifact into the app

## Responsible Use

Predictions from observational survey data may be affected by sampling, missingness, measurement error, and population differences. Any future results should be presented with their intended population, uncertainty, validation limits, and a clear statement that they are not a substitute for laboratory testing or professional medical advice.