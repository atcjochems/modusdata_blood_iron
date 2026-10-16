# Models

`anemia_xgb_pipeline.joblib` is the exploratory XGBoost artifact loaded by `app/app.py`. It is intentionally included in Git so Streamlit Community Cloud can load it when deploying the repository. The app resolves the file relative to its source path at `models/anemia_xgb_pipeline.joblib`.

Regenerate the artifact by running all cells in `notebooks/anemia_dataset_eda_model_comparison.ipynb`. Other generated `.joblib` and `.pkl` files remain excluded from Git. This artifact is for demonstration only and is not clinically validated.