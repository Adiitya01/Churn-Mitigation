import pandas as pd
import numpy as np

# Load the base dataset
df = pd.read_csv('../Datasets/Churn.csv')
num_rows = len(df)

# Seed for reproducibility
np.random.seed(42)

# Generate behavioral columns with correlation to 'Exited' (Churn)
# 1. Transaction Frequency (Avg 10-40)
df['TransactionFrequency'] = np.random.poisson(20, num_rows)

# 2. Avg Transaction Amount (Random but realistic)
df['AvgTransactionAmount'] = np.random.normal(5000, 2000, num_rows).clip(100, 50000)

# 3. Complaints Filed (Correlate with Exited)
# If Exited == 1, more likely to have 1-5 complaints. If Exited == 0, mostly 0-1.
df['ComplaintsFiled'] = df['Exited'].apply(lambda x: np.random.poisson(2.5 if x == 1 else 0.5))

# 4. Customer Satisfaction (1-5, Correlate with Exited)
# If Exited == 1, lower satisfaction (1-3). If Exited == 0, higher (3-5).
def get_satisfaction(exited):
    if exited == 1:
        return np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
    else:
        return np.random.choice([3, 4, 5], p=[0.2, 0.4, 0.4])

df['CustomerSatisfaction'] = df['Exited'].apply(get_satisfaction)

# 5. HasLoan (Binary)
df['HasLoan'] = np.random.binomial(1, 0.3, num_rows)

# Clean up: the Fbank.ipynb expects certain columns. Let's see the required columns from app.py prediction
# For Churn: Age, CreditScore, Tenure, TransactionFrequency, AvgTransactionAmount, ComplaintsFiled, CustomerSatisfaction, HasLoan, Balance
# Our df has: CustomerId, RowNumber, Surname, CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited (Churn), plus new ones.

# Rename 'Exited' to 'Churn' as requested in some notebooks
df.rename(columns={'Exited': 'Churn'}, inplace=True)

# Save to Final_bank.csv
df.to_csv('../Datasets/Final_bank.csv', index=False)

print("✅ Dataset augmented and saved as 'Final_bank.csv'")
print(f"Total columns: {len(df.columns)}")
print(df[['Churn', 'ComplaintsFiled', 'CustomerSatisfaction']].groupby('Churn').mean())
