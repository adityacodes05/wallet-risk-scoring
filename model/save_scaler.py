import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
import os

# Load preprocessed features
df = pd.read_csv("output/wallet_features.csv")
features = df.drop(columns=["wallet"], errors="ignore")

# Fit scaler
scaler = StandardScaler()
scaler.fit(features)

# Save scaler
os.makedirs("model", exist_ok=True)
with open("model/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("✅ scaler.pkl saved in model/")
