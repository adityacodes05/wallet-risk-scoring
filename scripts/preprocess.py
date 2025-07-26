import os
import json
import pandas as pd
from datetime import datetime

INPUT_JSON = "output/transactions_raw.json"
OUTPUT_CSV = "output/wallet_features.csv"

def load_data():
    if not os.path.exists(INPUT_JSON):
        print(f"❌ Input file not found: {INPUT_JSON}")
        return []
    with open(INPUT_JSON, "r") as f:
        return json.load(f)

def preprocess_wallet(wallet_data):
    items = wallet_data.get("items", [])
    if not items:
        return None

    total_tx = len(items)
    successful_tx = sum(1 for tx in items if tx.get("successful"))
    success_rate = successful_tx / total_tx if total_tx > 0 else 0

    timestamps = [datetime.strptime(tx["block_signed_at"], "%Y-%m-%dT%H:%M:%S%z") for tx in items]
    timestamps.sort()

    duration = (timestamps[-1] - timestamps[0]).total_seconds() if len(timestamps) >= 2 else 0
    avg_time_between_tx = duration / (total_tx - 1) if total_tx > 1 else 0

    total_gas = sum(tx.get("gas_spent", 0) for tx in items)
    total_value = sum(int(tx.get("value", 0)) for tx in items)

    return {
        "wallet": wallet_data["wallet"],
        "total_tx": total_tx,
        "successful_tx": successful_tx,
        "success_rate": round(success_rate, 4),
        "total_gas": total_gas,
        "total_value": total_value / 1e18,  # Convert from wei to ETH
        "avg_time_between_tx_sec": round(avg_time_between_tx, 2)
    }

def main():
    raw_data = load_data()
    features = []

    for wallet_data in raw_data:
        f = preprocess_wallet(wallet_data)
        if f:
            features.append(f)

    df = pd.DataFrame(features)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Preprocessed data saved to '{OUTPUT_CSV}'")

if __name__ == "__main__":
    main()
