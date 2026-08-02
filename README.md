# Healthcare Scam / Phishing Detector

An end-to-end machine learning project by **Anmol Rathod** that classifies healthcare-related SMS, emails, and short messages as `legit` or `scam`.

## Problem Statement

Healthcare scams often use urgency, fake insurance or Medicare claims, credential theft, and payment pressure. Missing a scam is more costly than flagging a suspicious message, so this project prioritizes scam recall while keeping the model lightweight and explainable.

## Solution

The project combines a documented public SMS spam dataset with a curated healthcare seed dataset, cleans and validates messages, compares classical NLP models, selects the best model, and serves predictions through Streamlit.

## Tech Stack

Python, pandas, scikit-learn, TF-IDF, Logistic Regression, Multinomial Naive Bayes, Linear SVM, Random Forest, joblib, Streamlit, pytest.

## Dataset

Primary public source: UCI SMS Spam Collection, a public set of 5,574 English SMS messages labeled ham/spam. The training script downloads it when internet access is available. A healthcare-focused seed dataset is included at `data/processed/healthcare_seed_messages.csv` so the project remains runnable offline.

Label mapping:

- `ham`, `legitimate`, `legit`, `safe` -> `legit`
- `spam`, `smishing`, `phishing`, `scam`, `fraud` -> `scam`

More details are in `docs/dataset.md`.

## Installation

```bash
python -m pip install -r requirements.txt
```

## Usage

Train and save the model:

```bash
python -m src.train --rebuild-data
```

Run command-line prediction:

```bash
python -m src.predict "Urgent Medicare refund, click to verify your SSN"
```

Launch the UI:

```bash
streamlit run app/streamlit_app.py
```

## Vercel Deployment

The repository includes a Vercel-ready browser frontend and Python inference API:

- Static frontend source: `public/`
- Build output: `dist/`
- Python API: `api/index.py`
- Prediction endpoint: `/api/predict`

Import the GitHub repository into Vercel and click Deploy. Vercel reads `vercel.json`, runs `npm run build`, serves `dist/`, and routes predictions to the Python Function.

## Results

Training writes `models/metrics.json` with model comparison, class balance, and selected model metrics. The selector ranks models by scam recall first, then scam F1-score and accuracy.

## Project Structure

```text
app/                 Streamlit interface
data/                Raw and processed datasets
docs/                Dataset and project notes
models/              Saved model and metrics
notebooks/           Notebook placeholder for EDA
presentation/        Beamer presentation
report/              Report copy
src/                 Training, evaluation, prediction code
tests/               Unit tests
idea.tex             LaTeX report
```

## Future Work

- Add more verified healthcare-specific phishing datasets when licenses allow redistribution.
- Add threshold tuning with a validation set for stricter false-negative control.
- Add SHAP or LIME explanations for richer model interpretability.
- Package as a small API for integration with clinic helpdesk workflows.
