import os
import json
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
COVALENT_API_KEY = os.getenv("COVALENT_API_KEY")
CHAIN_ID = "1"  # Ethereum Mainnet
BASE_URL = "https://api.covalenthq.com/v1"
INPUT_CSV = "data/wallets.csv"
OUTPUT_DIR = "output"
OUTPUT_JSON = os.path.join(OUTPUT_DIR, "transactions_raw.json")

def get_transactions(wallet):
    """Fetch transaction data for a single wallet address using Covalent API."""
    url = f"{BASE_URL}/{CHAIN_ID}/address/{wallet}/transactions_v2/"
    params = {"key": COVALENT_API_KEY}

    try:
        print(f"🔍 Fetching data for {wallet}...")
        response = requests.get(url, params=params, timeout=20)

        if response.status_code == 200:
            data = response.json().get("data", {})
            return {
                "wallet": wallet,
                "data": data,
                "items": data.get("items", [])
            }
        else:
            print(f"❌ Failed for {wallet}: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data for {wallet}: {str(e)}")
        return None

def fetch_all():
    """Read wallets from CSV, fetch data, and save to JSON."""
    if not os.path.exists(INPUT_CSV):
        print(f"❌ Wallet CSV file not found: {INPUT_CSV}")
        return

    df = pd.read_csv(INPUT_CSV)

    if "wallet" not in df.columns:
        print("❌ CSV file must have a 'wallet' column.")
        return

    results = []
    for wallet in df["wallet"].dropna():
        wallet = wallet.strip()
        if wallet:
            data = get_transactions(wallet)
            if data:
                results.append(data)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Fetched data for {len(results)} wallets. Saved to '{OUTPUT_JSON}'")

if __name__ == "__main__":
    fetch_all()
