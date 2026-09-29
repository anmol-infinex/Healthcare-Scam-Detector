# 🛡️ Healthcare Scam / Phishing Detector

![Healthcare Scam Detector](assets/healthcare-hero.svg)

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Deploy-000000?logo=vercel&logoColor=white)](https://vercel.com/)

> An end-to-end machine learning project that analyzes healthcare-related SMS, emails, and short messages and classifies them as **legit** or **scam**.

## 🎯 Why It Matters

Healthcare communication is increasingly delivered through messages about appointments, billing, lab reports, prescriptions, insurance, and portal access. That creates opportunities for phishing and fraud.

This project focuses on identifying suspicious healthcare-themed messages **before a user acts on them**, using a lightweight and explainable NLP pipeline.

## 🔍 What the Project Does

**Message → Cleaning → TF-IDF Features → Model Comparison → Scam/Legit Prediction → Confidence & Explanation**

The training workflow uses a public SMS dataset together with a healthcare-focused seed dataset, then compares several classical NLP models before selecting a deployable model.

## ✨ Key Features

- Scam-focused text classification
- TF-IDF-based NLP pipeline
- Comparison of Naive Bayes, Logistic Regression, Linear SVM, and Random Forest
- Confidence-aware prediction output
- Browser UI + Python API
- Local training and inference
- Vercel-ready deployment
- Unit tests for core utilities

## 🧰 Tech Stack

Python · pandas · scikit-learn · TF-IDF · Logistic Regression · Naive Bayes · Linear SVM · Random Forest · joblib · Streamlit · Flask · pytest

## 📚 Dataset

The primary public source is the **UCI SMS Spam Collection (5,574 messages)**, supplemented by a healthcare seed dataset included in the repository.

## 🚀 Quick Start

```bash
python -m pip install -r requirements.txt
python -m src.train --rebuild-data
python -m src.predict "Urgent Medicare refund, click to verify your SSN"
streamlit run app/streamlit_app.py
```

## 🌐 Deployment

The project includes a browser frontend and Python inference API designed for deployment with Vercel.

## 👨‍💻 Author

**Anmol Rathod**

Built as an applied AI + cybersecurity project for phishing/scam detection research.