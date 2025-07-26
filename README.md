# 🧠 Wallet Risk Scoring From Scratch

This project analyzes on-chain behavior of wallets using transaction data from the Compound V2/V3 protocol and assigns a **risk score between 0 and 1000** to each wallet based on features like borrow/repay behavior, frequency of interaction, and transaction history.

---

## 📦 Project Structure

```
wallet-risk-scoring/
│
├── data/                            # Input wallet data
│   └── wallets.csv                  # CSV file with 100 wallet addresses
│
├── model/                           # Trained ML models and scaler
│   ├── kmeans.pkl                   # Trained KMeans clustering model
│   ├── model.pkl                    # (Optional) Pickled model file
│   ├── scaler.pkl                   # Saved Scikit-learn StandardScaler
│   └── save_scaler.py               # Script to save scaler (one-time)
│
├── output/                          # Output results
│   ├── transactions_raw.json        # Raw transaction data (large, ignored in Git)
│   ├── wallet_features.csv          # Engineered features per wallet
│   ├── wallet_scores.csv            # Risk scores (0–1000) for each wallet
│   └── scored_output.csv            # Output with uploaded addresses + scores
│
├── scripts/                         # Core pipeline scripts
│   ├── fetch_data.py                # Fetch on-chain transaction data
│   ├── preprocess.py                # Feature engineering & data cleaning
│   ├── train_model.py               # Train ML model & scaler
│   └── score.py                     # Generate risk scores
│
├── templates/                       # Flask HTML templates
│   └── index.html                   # UI for wallet score lookup
│
├── uploads/                         # CSV upload directory via frontend
│   └── Wallet_id_-_Sheet1.csv       # Example uploaded CSV
│
├── .env                             # Environment config (API keys etc.)
├── analysis.md                      # Assignment explanation and analysis
├── app.py                           # Flask app for UI and wallet scoring
├── project setup                    # Text file documenting setup steps
└── README.md                        # Project overview and usage guide


```

---

## ✅ Features Used for Risk Scoring

Each wallet is scored using the following on-chain behavior indicators:

| Feature Name            | Description                                            |
|-------------------------|--------------------------------------------------------|
| `total_transactions`    | Total number of on-chain transactions                  |
| `total_borrows`         | Number of borrow transactions with Compound            |
| `total_repays`          | Number of repay transactions                           |
| `avg_tx_interval`       | Average time interval (in blocks) between transactions |
| `borrow_repay_ratio`    | Ratio of borrow to repay transactions                  |
| `compound_interactions` | Number of times wallet interacted with Compound contracts |

---

## ⚙️ How It Works

1. **Fetch transaction history** for 100 wallets using Covalent API.
2. **Preprocess transactions** to engineer meaningful features.
3. **Train KMeans clustering model** on the features to categorize risk levels.
4. **Assign scores** based on cluster assignment (scaled between 0–1000).
5. **Serve via Flask app** to let users check scores via wallet address.

---

## 🚀 Running the Project

### 1. Clone the repo

```bash
git clone https://github.com/adityacodes05/wallet-risk-scoring.git
cd wallet-risk-scoring
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API key to `.env`

```
COVALENT_API_KEY=your_covalent_api_key_here
```

### 4. Run the full pipeline

```bash
# Step 1: Fetch raw data
python scripts/fetch_data.py

# Step 2: Preprocess features
python scripts/preprocess.py

# Step 3: Train model and scaler
python scripts/train_model.py

# Step 4: Score wallets
python scripts/score.py
```

### 5. Start the UI

```bash
cd frontend
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) to search wallet scores.

---

## 📈 Sample Output

| Wallet Address                             | Score |
|-------------------------------------------|-------|
| 0xfaa0768bde629806739c3a4620656c5d26f44ef2 | 732   |
| 0x8e9b8a68dd77f7dc64b9a09c441eb4b6468b416b | 430   |

---

## 📝 Author Notes

- Built from scratch using only raw on-chain data and open-source tools.
- Project can be extended to support other protocols like Aave or Maker.
- Risk scoring logic is kept transparent and explainable.

---

## 📜 License

This project is open-sourced under the MIT License.
