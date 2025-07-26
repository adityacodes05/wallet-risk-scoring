from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Paths
SCORES_PATH = "output/wallet_scores.csv"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load existing scores
df_scores = pd.read_csv(SCORES_PATH)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    wallet = request.form.get("wallet_id", "").strip().lower()

    if not wallet:
        return render_template("index.html", error="Please enter a wallet address")

    record = df_scores[df_scores["wallet_id"].str.lower() == wallet]

    if not record.empty:
        score = int(record["score"].values[0])
        return render_template("index.html", score=score, wallet_id=wallet)
    else:
        return render_template("index.html", error="Wallet address not found")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return render_template("index.html", error="No file uploaded")

    file = request.files["file"]
    if file.filename == "":
        return render_template("index.html", error="Empty file name")

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Read uploaded CSV
        df_upload = pd.read_csv(filepath)
        if "wallet_id" not in df_upload.columns:
            return render_template("index.html", error="CSV must contain 'wallet_id' column")

        df_upload["wallet_id"] = df_upload["wallet_id"].str.lower()
        df_scored = pd.merge(df_upload, df_scores, on="wallet_id", how="left")
        output_file = os.path.join("output", "scored_output.csv")
        df_scored.to_csv(output_file, index=False)

        return render_template("index.html", download_link="/download")

    except Exception as e:
        return render_template("index.html", error=f"Error: {str(e)}")

@app.route("/download")
def download():
    return send_file("output/scored_output.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
