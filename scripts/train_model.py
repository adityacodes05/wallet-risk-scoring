import pandas as pd
import pickle
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

FEATURES_PATH = "output/wallet_features.csv"
SCALER_PATH = "model/scaler.pkl"
MODEL_PATH = "model/kmeans.pkl"

def main():
    df = pd.read_csv(FEATURES_PATH)
    X = df.drop(columns=["wallet"])

    # Scale the features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Train KMeans
    kmeans = KMeans(n_clusters=4, random_state=42)
    kmeans.fit(X_scaled)

    # Save the scaler and model
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(kmeans, f)

    print(f"✅ Model and scaler saved to '{SCALER_PATH}' and '{MODEL_PATH}'")

if __name__ == "__main__":
    main()
