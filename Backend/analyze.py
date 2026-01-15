import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel("churn_data.xlsx")

print("\n===== BASIC INFO =====")
print(df.info())

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== CHURN DISTRIBUTION =====")
print(df['Churn'].value_counts(normalize=True))

print("\n===== STATISTICS =====")
print(df.describe())

print("\n===== CORRELATION WITH CHURN =====")
print(df.corr()['Churn'].sort_values(ascending=False))

# Heatmap (optional)
sns.heatmap(df.corr(), cmap="coolwarm")
plt.show()
