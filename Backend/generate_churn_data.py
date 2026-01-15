import pandas as pd
import numpy as np

# -----------------------------
# CONFIG
# -----------------------------
np.random.seed(42)
ROWS = 5000
TARGET_CHURN_RATE = 0.25   # ~25% churn (banking realistic)

# -----------------------------
# BASE FEATURES
# -----------------------------
CustomerId = np.random.randint(10000000, 99999999, ROWS)

Age = np.random.normal(40, 10, ROWS).clip(18, 70).astype(int)

CreditScore = np.random.normal(650, 90, ROWS).clip(300, 900).astype(int)

Tenure = np.random.randint(0, 11, ROWS)

TransactionFrequency = np.random.poisson(18, ROWS).clip(1, 60)

AvgTransactionAmount = np.random.normal(15000, 7000, ROWS).clip(200, 200000)

ComplaintsFiled = np.random.poisson(1.2, ROWS).clip(0, 10)

CustomerSatisfaction = np.random.choice(
    [1, 2, 3, 4, 5],
    size=ROWS,
    p=[0.15, 0.20, 0.30, 0.25, 0.10]
)

HasLoan = np.random.binomial(1, 0.45, ROWS)

Balance = np.random.normal(60000, 35000, ROWS).clip(0, 250000)

# -----------------------------
# NORMALIZATION (for risk calc)
# -----------------------------
credit_norm = (700 - CreditScore) / 400
balance_norm = (50000 - Balance) / 50000
tenure_norm = (4 - Tenure) / 10
freq_norm = np.abs(TransactionFrequency - 18) / 40
complaint_norm = ComplaintsFiled / 5
satisfaction_norm = (5 - CustomerSatisfaction) / 4

# -----------------------------
# BEHAVIOR-DRIVEN CHURN RISK
# -----------------------------
churn_risk = (
    1.8 * satisfaction_norm +          # strongest signal
    1.4 * complaint_norm +              # strong signal
    0.9 * tenure_norm +                 # medium
    0.8 * balance_norm +                # medium
    0.6 * credit_norm +                 # weak–medium
    0.5 * HasLoan +                     # mild
    0.4 * freq_norm                     # behavior change
)

# Interaction effects (realistic)
churn_risk += 0.6 * ((CustomerSatisfaction <= 2) & (ComplaintsFiled >= 3))
churn_risk += 0.4 * ((Tenure <= 1) & (Balance < 20000))

# Noise (real world uncertainty)
noise = np.random.normal(0, 0.6, ROWS)
churn_risk += noise

# -----------------------------
# SIGMOID → PROBABILITY
# -----------------------------
churn_prob = 1 / (1 + np.exp(-churn_risk))

# Scale probabilities to desired churn rate
scaling_factor = TARGET_CHURN_RATE / churn_prob.mean()
churn_prob = np.clip(churn_prob * scaling_factor, 0, 1)

# -----------------------------
# FINAL CHURN LABEL
# -----------------------------
Churn = np.random.binomial(1, churn_prob)

# -----------------------------
# CREATE DATAFRAME
# -----------------------------
df = pd.DataFrame({
    "CustomerId": CustomerId,
    "Age": Age,
    "CreditScore": CreditScore,
    "Tenure": Tenure,
    "TransactionFrequency": TransactionFrequency,
    "AvgTransactionAmount": AvgTransactionAmount,
    "ComplaintsFiled": ComplaintsFiled,
    "CustomerSatisfaction": CustomerSatisfaction,
    "HasLoan": HasLoan,
    "Balance": Balance,
    "Churn": Churn
})

# -----------------------------
# SAVE
# -----------------------------
df.to_excel("churn_data.xlsx", index=False)

print("✅ High-quality banking-grade churn dataset generated")
print("Churn rate:", df["Churn"].mean().round(3))
print(df.head())
