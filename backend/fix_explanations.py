# backend/fix_explanations.py
import pandas as pd

df = pd.read_csv("data/replay_final.csv")

def make_explanation(row):
    score = row["flow_risk_score"]
    if score >= 70:
        label = "Blocked"
    elif score >= 40:
        label = "Flagged"
    else:
        label = "Allowed"

    # Allowed flows get a clean, non-alarming explanation — no "risk driver" language
    if label == "Allowed":
        return f"{label}: consistent with normal traffic patterns (risk score {score:.0f}/100)"

    if row["primary_model"] == "TLS/JA3 intel" and row["ja3_risk"] == 1.0:
        return f"{label}: TLS client fingerprint matches a known-malicious JA3 hash ({row['ja3_hash'][:8]}...)"
    elif row["primary_model"] == "Anomaly detector":
        return f"{label}: flow deviates from the normal traffic baseline (unsupervised anomaly signal)"
    else:
        return f"{label}: classifier flagged unusual {row['top_shap_features']}"

df["explanation"] = df.apply(make_explanation, axis=1)
df.to_csv("data/replay_final.csv", index=False)
print("Fixed explanations saved.\n")

print("Sample explanations (attack flows):")
for _, r in df[df["true_label"] != "Normal Traffic"].sample(5, random_state=2).iterrows():
    print(f"  [{r['true_label']}] {r['explanation']}")

print("\nSample explanations (normal flows):")
for _, r in df[df["true_label"] == "Normal Traffic"].sample(3, random_state=2).iterrows():
    print(f"  [{r['true_label']}] {r['explanation']}")