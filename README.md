# Healthcare Scam / Phishing Detector

![Healthcare Scam Detector](assets/healthcare-hero.svg)

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Deploy-000000?logo=vercel&logoColor=white)](https://vercel.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end machine learning project by **Anmol Rathod** that classifies healthcare-related SMS, emails, and short messages as `legit` or `scam`.

## Overview

Healthcare teams and patients increasingly rely on text-based communication for appointments, lab reports, billing updates, prescription notices, and portal access. That convenience also creates a very practical attack surface. A scam message does not need to be sophisticated. It only needs to look believable for a few seconds.

This project screens those messages before a user reacts to them. It uses classical NLP, a lightweight model stack, and a browser-based interface so the system stays fast, explainable, and easy to deploy.

## Why this project exists

Healthcare scams often use urgency, fake insurance or Medicare claims, credential theft, and payment pressure. Missing a scam is more costly than flagging a suspicious message, so the project prioritizes scam recall while keeping the model lightweight and understandable.

## What the project does

The system follows a straightforward workflow:

1. load and clean a documented SMS dataset,
2. merge it with a curated healthcare seed set,
3. compare several classical NLP models,
4. choose the best model for deployment,
5. serve predictions through a browser UI and Python API.

The selected model is optimized for short-message phishing detection, where the signal usually lives in a few words, a link, or an urgent request.

## Key features

- Clean browser interface with a premium-looking layout
- Scam-aware result display with confidence and explanation
- Lightweight NLP pipeline based on TF-IDF
- Classical model comparison before selection
- Fast local training and inference
- Vercel-ready frontend and Python API
- Unit tests for core utilities

## Tech stack

Python, pandas, scikit-learn, TF-IDF, Logistic Regression, Multinomial Naive Bayes, Linear SVM, Random Forest, joblib, Streamlit, Flask, pytest.

## Dataset

The primary public source is the **UCI SMS Spam Collection**, a public set of **5,574 English SMS messages** labeled ham/spam. The training pipeline downloads it when internet access is available. A healthcare-focused seed dataset is included at `data/processed/healthcare_seed_messages.csv` so the project remains runnable offline.

### Label mapping

- `ham`, `legitimate`, `legit`, `safe` → `legit`
- `spam`, `smishing`, `phishing`, `scam`, `fraud` → `scam`

More dataset details are documented in `docs/dataset.md`.

## Model approach

The project compares the following classical NLP models:

- Multinomial Naive Bayes
- Logistic Regression
- Linear Support Vector Machine
- Random Forest

Why classical models? For short phishing-style messages, sparse lexical features often matter more than deep semantic reasoning. TF-IDF keeps the pipeline compact and works well with linear classifiers. Random Forest stays in the comparison set for benchmarking, but the final choice is driven by scam recall, F1-score, and deployability.

## Installation

```bash
python -m pip install -r requirements.txt
```

## Usage

### Train and save the model

```bash
python -m src.train --rebuild-data
```

### Run command-line prediction

```bash
python -m src.predict "Urgent Medicare refund, click to verify your SSN"
```

### Launch the UI

```bash
streamlit run app/streamlit_app.py
```

## Web demo

The repository includes a Vercel-ready browser frontend and Python inference API.

- Static frontend source: `public/`
- Build output: `dist/`
- Python API: `api/index.py`
- Prediction endpoint: `/api/predict`

Import the GitHub repository into Vercel and click Deploy. Vercel reads `vercel.json`, runs `npm run build`, serves `dist/`, and routes predictions to the Python Function.

## API

The inference layer exposes a small JSON API. The browser app and serverless function follow the same principle: send a message, receive a risk-aware prediction, explanation, and confidence.

## Results

Training writes `models/metrics.json` with model comparison, class balance, and selected model metrics. The selector ranks models by scam recall first, then scam F1-score and accuracy.

## Project structure

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
assets/              README visuals and banner art
idea.tex             LaTeX report
```

## Screenshots

The included web UI is intentionally minimal and fast. It is designed to show the prediction clearly, not to overwhelm the user with controls.

## Future work

- Add more verified healthcare-specific phishing datasets when licenses allow redistribution.
- Add threshold tuning with a validation set for stricter false-negative control.
- Add SHAP or LIME explanations for richer model interpretability.
- Package as a small API for integration with clinic helpdesk workflows.
- Extend the browser experience with a darker, more visual security-style theme.

## Author

**Anmol Rathod**

If you use this project in a presentation or internship submission, keep the architecture notes and dataset sources intact so the evaluation remains reproducible.
