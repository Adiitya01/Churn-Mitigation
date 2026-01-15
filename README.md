# 🏦 Elite Financial Intelligence Portal
### *Advanced Customer Churn Prediction & Credit Risk Analytics*

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

A high-performance, full-stack predictive analytics system designed for modern banking. This project identifies at-risk customers with high precision and automates credit allowance decisions using state-of-the-art Machine Learning.

---

## 🚀 Key Features

- **💎 Premium Glassmorphic Dashboard**: A stunning, interactive UI with animated risk gauges and real-time feedback.
- **⚡ Dual-Engine Backend**: Powered by **FastAPI** for high-concurrency RESTful performance and **Flask** for lightweight alternatives.
- **🤖 High-Precision ML Models**: 
    - **Churn Engine**: Predicts customer exit probability based on 19+ behavioral factors including satisfaction and complaint history.
    - **Allowance Engine**: Automated credit scoring based on financial health and product interactions.
- **📊 Behavioral Data Augmentation**: Original banking data was synthetically enhanced with higher-correlation features (Satisfaction Scores, Transaction Frequencies) to allow the model to learn complex human behaviors.

---

## 📁 Repository Structure

```text
├── Backend/
│   ├── main.py            # FastAPI Production Server
│   ├── app.py             # Flask Alternative Server
│   ├── train_models.py    # Model Training Pipeline
│   └── augment_dataset.py # Data Engineering Script
├── Frontend/
│   ├── index.html         # Lead-Dashboard structure
│   ├── Styles.css         # Custom Glassmorphism UI kit
│   └── script.js          # Interactive Dashboard Logic
├── Datasets/
│   ├── Final_bank.csv     # 10,000 Row Augmented Dataset
│   └── Churn.csv          # Raw Base Data
└── Models/
    ├── churn_model.pkl    # Trained Random Forest (Churn)
    └── allowance_model.pkl # Trained Random Forest (Credit)
```

---

## 🛠️ Installation & Setup

### 1. Requirements
Ensure you have Python 3.9+ installed.
```bash
pip install fastapi uvicorn flask flask-cors pandas scikit-learn
```

### 2. Run the API (Backend)
```bash
cd Backend
python main.py
```
*API Documentation will be available at: `http://127.0.0.1:8000/docs`*

### 3. Launch the Portal (Frontend)
Simply open `Frontend/index.html` in your web browser.

---

## 🧠 Model Logic & Engineering

The models are built using a **Random Forest Ensemble** to handle the non-linear relationships in banking behavior:
- **Churn Correlation**: Specially tuned to recognize the "Dissatisfaction Loop"—where low satisfaction and high complaints exponentially increase the churn probability.
- **Allowance Logic**: Focuses on stability indices (Tenure, Balance, and Estimated Salary) to determine eligibility.

---

