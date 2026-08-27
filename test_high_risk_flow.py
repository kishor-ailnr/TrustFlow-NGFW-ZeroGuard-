"""
test_high_risk_flow.py
======================
End-to-end test that opens a live WebSocket to /ws, sends one real attack
row from data/replay_holdout.csv, and asserts the server replies with
action == "Block" or "Quarantine".

Usage
-----
  Start the backend first (in a separate terminal):
      uvicorn backend.main:app --host 127.0.0.1 --port 8000
  Then run:
      python test_high_risk_flow.py

Optional env vars
-----------------
  WS_URL   - override the WebSocket URL (default: ws://127.0.0.1:8000/ws)
  CSV_PATH - override the CSV to sample from (default: data/replay_holdout.csv)
"""

import os
import json
import asyncio
import pandas as pd
import joblib
import websockets

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
WS_URL       = os.getenv("WS_URL", "ws://127.0.0.1:8000/ws")
CSV_PATH     = os.getenv("CSV_PATH", "data/replay_holdout.csv")
FALLBACK_CSV = "data/replay_final.csv"   # secondary source if holdout absent

# These posture flags are deliberately degraded so that trust_score lands at 15
# (Low band) and the decision matrix always returns Block/Quarantine for any
# High-risk fused score.
POSTURE_SIGNALS = {
    "mfa_on":         False,   # -30 pts
    "device_healthy": False,   # -30 pts  -> trust = 15 (Low band)
    "known_location": False,   # -25 pts
    "normal_hours":   True,    # +15 pts
}

# JA3 risk injected to ensure Model C also contributes to the fused score
JA3_RISK = 1.0


# ---------------------------------------------------------------------------
# Helper: pick one attack row from the CSV
# ---------------------------------------------------------------------------
def load_attack_row(csv_path: str, preferred_label: str = "DoS") -> pd.Series:
    """
    Load the CSV and return the first row whose true_label matches
    preferred_label.  If that class is absent, fall back to any non-Normal row.
    """
    path = csv_path if os.path.exists(csv_path) else FALLBACK_CSV
    print(f"[loader] reading {path} ...")
    df = pd.read_csv(path)

    attack_df = df[df["true_label"] != "Normal Traffic"]
    if attack_df.empty:
        raise ValueError(f"No attack rows found in {path}")

    pref = attack_df[attack_df["true_label"] == preferred_label]
    row  = pref.iloc[0] if not pref.empty else attack_df.iloc[0]
    print(f"[loader] selected attack type: '{row['true_label']}'  "
          f"(total attack rows in file: {len(attack_df):,})")
    return row


# ---------------------------------------------------------------------------
# Helper: build a clean WS payload from a DataFrame row
# ---------------------------------------------------------------------------
def build_payload(row: pd.Series, feature_cols: list) -> dict:
    """
    Construct the JSON payload expected by /ws.

    Required keys
    -------------
    All 52 network-flow feature columns (float) -- fed to the ML ensemble
    flow_id    (str)  -- arbitrary identifier; logged in decision engine
    source_ip  (str)  -- source address; used in VLAN state and block logic

    Optional keys (defaults shown in parentheses)
    ----------
    mfa_on          bool  (True)  -- used by trust_engine
    device_healthy  bool  (True)  -- used by trust_engine
    known_location  bool  (True)  -- used by trust_engine
    normal_hours    bool  (True)  -- used by trust_engine
    ja3_risk        float 0-1 (0.0) -- Model C score; no hash lookup needed
    """
    label = str(row.get("true_label", "UNKNOWN"))

    feature_values = {
        col: (0.0 if pd.isna(row[col]) else float(row[col]))
        for col in feature_cols
    }

    payload = {
        # metadata
        "flow_id":   f"ATTACK-TEST-{label.upper().replace(' ', '_')}-001",
        "source_ip": "203.0.113.195",
        # 52 ML feature columns
        **feature_values,
        # Zero Trust posture signals
        **POSTURE_SIGNALS,
        # TLS / JA3 intelligence
        "ja3_risk": JA3_RISK,
    }
    return payload


# ---------------------------------------------------------------------------
# Main test coroutine
# ---------------------------------------------------------------------------
async def test_high_risk_flow():
    # 1. Load model feature list
    feature_cols = joblib.load("models/feature_cols.pkl")

    # 2. Load one real attack row and build the payload
    row     = load_attack_row(CSV_PATH)
    payload = build_payload(row, feature_cols)

    sep = "=" * 60
    print(f"\n{sep}\nPAYLOAD BEING SENT TO /ws\n{sep}")
    print(json.dumps(payload, indent=2))
    print(sep)

    # 3. Open WebSocket, send payload, receive result
    print(f"\n[ws] connecting to {WS_URL} ...")
    async with websockets.connect(WS_URL) as ws:
        await ws.send(json.dumps(payload))
        raw      = await ws.recv()
        response = json.loads(raw)

    # 4. Print full response
    print(f"\n{sep}\nFULL RESPONSE FROM /ws\n{sep}")
    print(json.dumps(response, indent=2))

    # 5. Human-readable summary
    print(f"\n{sep}\nVERIFICATION SUMMARY\n{sep}")
    print(f"  Dataset label  : {row['true_label']}")
    print(f"  Flow ID        : {response['flow_id']}")
    print(f"  Source IP      : {response['source_ip']}")
    print(f"  Model A XGBoost: {response['model_a_score']:.4f}")
    print(f"  Model B IsoFor : {response['model_b_score']:.4f}")
    print(f"  Model C JA3    : {response['model_c_score']:.4f}")
    print(f"  Fused Risk     : {response['fused_risk_score']:.2f} / 100")
    print(f"  Trust Score    : {response['trust_score']:.0f} / 100  ({response['trust_band']})")
    print(f"  Primary Driver : {response['shap_attribution']['primary_model']}")
    print(f"  Top Features   : {response['shap_attribution']['top_features']}")
    print(f"  Explanation    : {response['explanation']}")
    print(f"  Action         : {response['action']}")
    print(f"  Reason         : {response['reason']}")
    print(sep)

    # 6. Assert the action is Block or Quarantine
    assert response["action"] in ("Block", "Quarantine"), (
        f"\n[FAIL] Expected 'Block' or 'Quarantine' for a real attack flow, "
        f"but got '{response['action']}'.\n"
        f"fused_risk_score={response['fused_risk_score']:.2f}, "
        f"trust_score={response['trust_score']:.0f}"
    )
    print(f"\n[PASS]  Attack row produced action='{response['action']}' OK")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(test_high_risk_flow())
