# backend/train_model.py

import pandas as pd
import numpy as np
import glob
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

# 1. Load all CSVs (recursive, in case the zip extracted into a subfolder)
files = glob.glob("data/**/*.csv", recursive=True)
print(f"Loading {len(files)} file(s): {files}")
df = pd.concat([pd.read_csv(f, low_memory=False) for f in files], ignore_index=True)
print("Raw shape:", df.shape)

# 2. Clean column names (CIC-IDS CSVs have leading/trailing spaces)
df.columns = df.columns.str.strip()

# 3. Find the label column (this dataset calls it "Attack Type")
label_col = "Attack Type"
print("Label column:", label_col)
print(df[label_col].value_counts())

# 4. Replace inf/-inf with NaN, drop bad rows
df = df.replace([np.inf, -np.inf], np.nan).dropna()
print("After cleaning:", df.shape)

# 5. Keep numeric feature columns
feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
X = df[feature_cols]
y_raw = df[label_col]

# 6. Encode labels (BENIGN, DDoS, PortScan... -> 0,1,2...)
le = LabelEncoder()
y = le.fit_transform(y_raw)
print("Classes:", list(le.classes_))

# 7. Downsample if huge, so training stays fast on a laptop CPU
MAX_ROWS = 300_000
if len(X) > MAX_ROWS:
    X, _, y, _ = train_test_split(X, y, train_size=MAX_ROWS, stratify=y, random_state=42)
    print("Downsampled to:", X.shape)

# 8. Train/test split — the test slice becomes today's "live replay" feed
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, stratify=y, random_state=42
)

# 9. Train XGBoost
model = XGBClassifier(n_estimators=150, max_depth=6, learning_rate=0.2, n_jobs=-1)
print("Training...")
model.fit(X_train, y_train)

# 10. Evaluate
preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))
print(classification_report(y_test, preds, target_names=le.classes_))

# 11. Save model + encoder + feature list for later phases
joblib.dump(model, "models/xgb_model.pkl")
joblib.dump(le, "models/label_encoder.pkl")
joblib.dump(feature_cols, "models/feature_cols.pkl")

# 12. Save the held-out test rows as today's replay feed
replay_df = X_test.copy()
replay_df["true_label"] = le.inverse_transform(y_test)
replay_df.to_csv("data/replay_holdout.csv", index=False)
print("Saved replay_holdout.csv with", len(replay_df), "rows")

print("\n✅ Phase 2a complete: model + replay data saved.")