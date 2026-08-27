# backend/explain.py

import numpy as np
import pandas as pd
import joblib
import shap

# ---------- 1. Load everything from Phase 2a/2b ----------
print("Loading models and enriched replay data...")
xgb_model = joblib.load("models/xgb_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
feature_cols = joblib.load("models/feature_cols.pkl")
meta_model = joblib.load("models/meta_model.pkl")

replay_df = pd.read_csv("data/replay_enriched.csv")
X = replay_df[feature_cols]
n_samples, n_features = X.shape
n_classes = len(label_encoder.classes_)

# ---------- 2. SHAP values for the XGBoost model ----------
print("Computing SHAP values (this can take a couple of minutes)...")
explainer = shap.TreeExplainer(xgb_model)
shap_raw = np.array(explainer.shap_values(X))
print("Raw SHAP array shape:", shap_raw.shape)

# Different shap/xgboost versions return different shapes — normalize to (samples, features, classes)
if shap_raw.shape == (n_classes, n_samples, n_features):
    shap_values = np.transpose(shap_raw, (1, 2, 0))
elif shap_raw.shape == (n_samples, n_features, n_classes):
    shap_values = shap_raw
elif shap_raw.shape == (n_samples, n_features):
    shap_values = shap_raw[:, :, None]
else:
    raise ValueError(f"Unexpected SHAP shape: {shap_raw.shape}")

print("Normalized SHAP shape:", shap_values.shape)

predicted_class_idx = xgb_model.predict(X)
feature_names = np.array(feature_cols)

top_features = []
for i in range(n_samples):
    cls = predicted_class_idx[i] if shap_values.shape[2] > 1 else 0
    row_shap = shap_values[i, :, cls]
    top2 = feature_names[np.argsort(-np.abs(row_shap))[:2]]
    top_features.append(", ".join(top2))

replay_df["top_shap_features"] = top_features

# ---------- 3. Which sub-model drove the decision? ----------
print("Computing per-model attribution...")
coefs = meta_model.coef_[0]  # order matches: xgb_risk, iso_risk, ja3_risk
model_names = np.array(["AI classifier", "Anomaly detector", "TLS/JA3 intel"])

contributions = replay_df[["xgb_risk", "iso_risk", "ja3_risk"]].values * coefs
primary_idx = np.argmax(contributions, axis=1)
replay_df["primary_model"] = model_names[primary_idx]

# ---------- 4. Human-readable explanation ----------
def make_explanation(row):
    if row["flow_risk_score"] >= 70:
        label = "Blocked"
    elif row["flow_risk_score"] >= 40:
        label = "Flagged"
    else:
        label = "Allowed"

    if row["primary_model"] == "TLS/JA3 intel" and row["ja3_risk"] == 1.0:
        return f"{label}: TLS client fingerprint matches a known-malicious JA3 hash ({row['ja3_hash'][:8]}...)"
    elif row["primary_model"] == "Anomaly detector":
        return f"{label}: flow deviates from the normal traffic baseline (unsupervised anomaly signal)"
    else:
        return f"{label}: classifier flagged unusual {row['top_shap_features']}"

replay_df["explanation"] = replay_df.apply(make_explanation, axis=1)

# ---------- 5. Save + sanity check ----------
replay_df.to_csv("data/replay_final.csv", index=False)
print("Saved data/replay_final.csv with", len(replay_df), "rows")

print("\nSample explanations (attack flows):")
samples = replay_df[replay_df["true_label"] != "Normal Traffic"].sample(5, random_state=1)
for _, r in samples.iterrows():
    print(f"  [{r['true_label']}] {r['explanation']}")

print("\nSample explanations (normal flows):")
samples = replay_df[replay_df["true_label"] == "Normal Traffic"].sample(2, random_state=1)
for _, r in samples.iterrows():
    print(f"  [{r['true_label']}] {r['explanation']}")

print("\n✅ Phase 3 complete: explainability + per-model attribution saved.")