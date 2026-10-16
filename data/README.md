# Data

The first analysis uses the [Anemia Dataset on Kaggle](https://www.kaggle.com/datasets/biswaranjanrao/anemia-dataset). The expected file is `anemia.csv`; it is already present locally. The Kaggle page describes `Gender` as 0 = male / 1 = female and `Result` as 0 = not anemic / 1 = anemic. Its license metadata is unknown, so check the source terms before redistribution or commercial use.

To fetch it from the repository root, install and authenticate the Kaggle CLI using Kaggle's documented API-token setup, then run:

```bash
python -m pip install kaggle
kaggle datasets download -d biswaranjanrao/anemia-dataset -p data --unzip
```

Never commit Kaggle credentials. The CSV is ignored by Git. Record any data cleaning or changes to label interpretation in the notebook. This dataset is labeled for anemia, not iron deficiency, and the label construction and provenance should be verified before drawing conclusions.