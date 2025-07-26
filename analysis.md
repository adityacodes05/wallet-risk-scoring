
## 📊 analysis.md

###  Project Title:
**Wallet Risk Scoring from Scratch using Compound Protocol Data**

---

###  Problem Overview:
The goal of this project is to assign a **risk score (0–1000)** to 100 Ethereum wallet addresses based on their historical transaction behavior with the **Compound V2/V3 protocol**. This score should reflect how risky a wallet is in terms of on-chain lending and borrowing activity.

---

###  1. Data Collection Method:

We fetched transaction history using the **Covalent API**, which provides decoded on-chain data per wallet.

- **API Used**: [Covalent Transactions v2 API](https://www.covalenthq.com/docs/api/)
- **Chain ID**: Ethereum Mainnet (`chain_id = 1`)
- **Data pulled**:
  - Borrow and repay events
  - Transaction counts
  - Block timestamps
  - Token interactions

The data was collected and saved as raw JSON files for processing.

---

###  2. Data Preprocessing & Feature Engineering:

From each wallet’s transaction history, we engineered several features representing wallet behavior:

| Feature Name            | Description                                            |
|-------------------------|--------------------------------------------------------|
| `total_transactions`    | Total number of on-chain transactions                  |
| `total_borrows`         | Number of borrow transactions with Compound            |
| `total_repays`          | Number of repay transactions                           |
| `avg_tx_interval`       | Average time interval (in blocks) between transactions |
| `borrow_repay_ratio`    | Ratio of borrow to repay transactions                  |
| `compound_interactions` | Number of times wallet interacted with Compound contracts |

**Note**: We removed non-informative or redundant features during experimentation (e.g., constant columns).

---

###  3. Feature Normalization:

We used **Min-Max Scaling** to normalize features into the range `[0, 1]`. This is essential for clustering algorithms like KMeans, which are sensitive to feature scales.

```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
```

---

###  4. Risk Scoring Model:

We trained a **KMeans Clustering model** to group wallets into risk levels based on their behavioral features.

- **Model**: `sklearn.cluster.KMeans`
- **Number of Clusters**: 4 (representing 4 risk tiers)

We mapped clusters to risk scores:

| Cluster | Score  |
|---------|--------|
| 0       | 250    |
| 1       | 500    |
| 2       | 750    |
| 3       | 1000   |

> This mapping was determined based on interpretability, where wallets with more stable behaviors (e.g., regular repayments) were grouped into higher scoring clusters.

---

###  5. Risk Indicators Justification:

- **High `total_borrows`** with low `total_repays` → Higher risk.
- **Low interaction with Compound** → Potentially inactive or safer.
- **Very high `avg_tx_interval`** → Inactive or dormant wallets.
- **Balanced borrow-repay ratio** → More reliable behavior.
- **Frequent interactions with Compound contracts** → Engaged and responsible users.

---

###  6. Output Format:

Final CSV Output:

```csv
wallet_id,score
0xfaa0768bde629806739c3a4620656c5d26f44ef2,750
0xabc123abc123abc123abc123abc123abc123abc1,500
...
```

---

###  Conclusion:

This solution demonstrates a scalable method to generate wallet risk scores using unsupervised learning from on-chain behavior. It can be extended to other protocols or used in real-time risk assessment dashboards.
