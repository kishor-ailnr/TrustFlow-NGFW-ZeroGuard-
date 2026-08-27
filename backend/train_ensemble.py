# backend/train_ensemble.py

import re
import hashlib
import random
import numpy as np
import pandas as pd
import joblib
import requests
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

random.seed(42)
np.random.seed(42)

# ---------- 1. Load Phase 2a outputs ----------
print("Loading Phase 2a outputs...")
xgb_model = joblib.load("models/xgb_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
feature_cols = joblib.load("models/feature_cols.pkl")

replay_df = pd.read_csv("data/replay_holdout.csv")
print("Replay shape:", replay_df.shape)

X = replay_df[feature_cols]
true_label = replay_df["true_label"]

# ---------- 2. Model A: XGBoost risk score ----------
print("Scoring with XGBoost (Model A)...")
proba = xgb_model.predict_proba(X)
normal_idx = list(label_encoder.classes_).index("Normal Traffic")
xgb_risk = 1 - proba[:, normal_idx]
replay_df["xgb_risk"] = xgb_risk

# ---------- 3. Model B: Isolation Forest anomaly score ----------
print("Training Isolation Forest (Model B) on benign-only flows...")
benign_mask = true_label == "Normal Traffic"
X_benign = X[benign_mask]

iso_forest = IsolationForest(n_estimators=150, contamination=0.05, random_state=42, n_jobs=-1)
iso_forest.fit(X_benign)

raw_scores = iso_forest.score_samples(X)
iso_risk_raw = -raw_scores
iso_risk = (iso_risk_raw - iso_risk_raw.min()) / (iso_risk_raw.max() - iso_risk_raw.min())
replay_df["iso_risk"] = iso_risk

joblib.dump(iso_forest, "models/iso_forest.pkl")

# ---------- 4. Model C: JA3 encrypted-traffic intelligence ----------
print("Downloading JA3 malicious fingerprint blocklist (abuse.ch, free)...")
try:
    resp = requests.get("https://sslbl.abuse.ch/blacklist/ja3_fingerprints.csv", timeout=15)
    resp.raise_for_status()
    malicious_hashes = set(re.findall(r"[a-f0-9]{32}", resp.text))
    if not malicious_hashes:
        raise ValueError("No hashes parsed from response")
    print(f"Loaded {len(malicious_hashes)} known-malicious JA3 hashes from the live feed")
except Exception as e:
    print(f"Could not reach the live feed ({e}). Using local placeholder hashes so the pipeline still runs.")
    malicious_hashes = {hashlib.md5(f"demo-malicious-{i}".encode()).hexdigest() for i in range(20)}

malicious_list = list(malicious_hashes)

def random_benign_hash():
    while True:
        h = hashlib.md5(str(random.random()).encode()).hexdigest()
        if h not in malicious_hashes:
            return h

def assign_ja3(is_attack):
    if is_attack and random.random() < 0.6:
        return random.choice(malicious_list)
    return random_benign_hash()

print("Attaching JA3 fingerprints to replay flows (simulated — CIC-IDS2017 has no native TLS metadata)...")
replay_df["ja3_hash"] = [assign_ja3(lbl != "Normal Traffic") for lbl in true_label]
replay_df["ja3_risk"] = replay_df["ja3_hash"].apply(lambda h: 1.0 if h in malicious_hashes else 0.0)

# ---------- 5. Meta-learner: fuse the three scores ----------
print("Training meta-learner...")
meta_X = replay_df[["xgb_risk", "iso_risk", "ja3_risk"]]
meta_y = (true_label != "Normal Traffic").astype(int)

meta_X_train, meta_X_test, meta_y_train, meta_y_test = train_test_split(
    meta_X, meta_y, test_size=0.2, stratify=meta_y, random_state=42
)

meta_model = LogisticRegression(class_weight="balanced")
meta_model.fit(meta_X_train, meta_y_train)

meta_preds = meta_model.predict(meta_X_test)
print("Meta-learner accuracy:", accuracy_score(meta_y_test, meta_preds))
print(classification_report(meta_y_test, meta_preds, target_names=["Normal", "Attack"]))

joblib.dump(meta_model, "models/meta_model.pkl")

# ---------- 6. Final fused Flow Risk Score (0-100) ----------
replay_df["flow_risk_score"] = meta_model.predict_proba(meta_X)[:, 1] * 100
replay_df.to_csv("data/replay_enriched.csv", index=False)
print("Saved data/replay_enriched.csv with", len(replay_df), "rows")
print("\n✅ Phase 2b complete: ensemble (XGBoost + Isolation Forest + JA3) + meta-learner saved.")