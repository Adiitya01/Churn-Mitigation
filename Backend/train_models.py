import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# 1. TRAIN CHURN MODEL
print("Training Churn Model...")
df_churn = pd.read_csv('../Datasets/Final_bank.csv')
churn_features = ['Age', 'CreditScore', 'Tenure', 'TransactionFrequency', 
                  'AvgTransactionAmount', 'ComplaintsFiled', 'CustomerSatisfaction', 
                  'HasLoan', 'Balance']
X_churn = df_churn[churn_features]
y_churn = df_churn['Churn']

# Random Forest Classifier
rf_churn = RandomForestClassifier(n_estimators=100, random_state=42)
rf_churn.fit(X_churn, y_churn)
with open('../Models/churn_model.pkl', 'wb') as f:
    pickle.dump(rf_churn, f)
print("✅ churn_model.pkl saved.")

# 2. TRAIN ALLOWANCE MODEL
print("Training Allowance Model...")
# The allowance model uses the standard 'Exited' (Churn in our new df) but as an 'Allowance' label
# According to Credit_card.ipynb: features are CreditScore, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary
df_allow = pd.read_csv('../Datasets/Final_bank.csv')
# Gender mapping
df_allow['Gender'] = df_allow['Gender'].map({'Female': 0, 'Male': 1, 'Other': 0})
allow_features = ['CreditScore', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
X_allow = df_allow[allow_features]
y_allow = df_allow['Churn'] # In the notebook, 'Exited' was renamed to 'Allowance'

rf_allow = RandomForestClassifier(n_estimators=100, random_state=42)
rf_allow.fit(X_allow, y_allow)
with open('../Models/allowance_model.pkl', 'wb') as f:
    pickle.dump(rf_allow, f)
print("✅ allowance_model.pkl saved.")
