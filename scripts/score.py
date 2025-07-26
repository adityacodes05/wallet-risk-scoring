import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

FEATURES_PATH = "output/wallet_features.csv"
SCALER_PATH = "model/scaler.pkl"
MODEL_PATH = "model/kmeans.pkl"
OUTPUT_PATH = "output/wallet_scores.csv"

def main():
    df = pd.read_csv(FEATURES_PATH)
    wallet_ids = df["wallet"]
    features = df.drop(columns=["wallet"])

    # Load scaler and model
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)
    with open(MODEL_PATH, "rb") as f:
        kmeans = pickle.load(f)

    X_scaled = scaler.transform(features)

    # Get raw cluster labels
    cluster_labels = kmeans.predict(X_scaled)

    # ✅ Scale cluster labels to 0–1000
    label_scaler = MinMaxScaler(feature_range=(0, 1000))
    scaled_scores = label_scaler.fit_transform(cluster_labels.reshape(-1, 1)).flatten().astype(int)

    result = pd.DataFrame({
        "wallet_id": wallet_ids,
        "score": scaled_scores
    })

    result.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Wallet scores saved to '{OUTPUT_PATH}'")

if __name__ == "__main__":
    main()
