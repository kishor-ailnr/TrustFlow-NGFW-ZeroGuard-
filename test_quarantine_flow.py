"""
test_quarantine_flow.py  (v2)
==============================
Strategy
--------
1. Load ALL rows from data/replay_holdout.csv.
2. Run XGBoost predict_proba locally to find "borderline" rows where the
   attack-class probability is in [0.40, 0.75] -- genuine uncertainty zone.
3. Also compute the full fused_risk offline to narrow to rows that land
   in the 30-90 window (below the hard-Block override at 90).
4. Send those borderline rows through /ws with a few trust combos.
5. Stop and print the full winning payload on the first Quarantine.
6. If still none, print a full fused_risk distribution across all rows so
   you can see whether the model's confidence is truly bimodal.

Usage:
    uvicorn backend.main:app --host 127.0.0.1 --port 8000
    python test_quarantine_flow.py
"""

import os, json, asyncio
import pandas as pd
import numpy as np
import joblib
import websockets

# ── Config ──────────────────────────────────────────────────────────────────
WS_URL   = os.getenv("WS_URL",   "ws://127.0.0.1:8000/ws")
CSV_PATH = os.getenv("CSV_PATH", "data/replay_holdout.csv")

# Rows with attack_prob in this range are borderline (XGBoost is uncertain)
BORDER_LO, BORDER_HI = 0.40, 0.75

# Only send rows whose OFFLINE fused_risk sits below the hard-Block override (90)
# and above the Low-risk floor (30) so we can actually reach a non-Block action.
FUSED_QUARANTINE_WINDOW = (30.0, 90.0)

# How many borderline rows to try (sorted by fused_risk descending so the
# highest-risk-but-below-override rows go first)
MAX_ROWS = 15

# Trust combos targeting the two Quarantine matrix cells:
#   Medium trust (50-79) + High risk (70-89)  -> Quarantine
#   Low    trust (< 50)  + Medium risk (30-70) -> Quarantine
TRUST_COMBOS = [
    # (label, mfa, device_healthy, known_location, normal_hours)
    ("Medium-trust (score=60)", True,  True,  False, False),   # 60 -> Medium
    ("Low-trust   (score=0)",   False, False, False, False),   # 0  -> Low
]

JA3_VALUES = [0.0, 0.3, 0.5]


# ── Local scoring helpers ────────────────────────────────────────────────────
def load_models():
    models_dir = "models"
    xgb     = joblib.load(os.path.join(models_dir, "xgb_model.pkl"))
    iso     = joblib.load(os.path.join(models_dir, "iso_forest.pkl"))
    meta    = joblib.load(os.path.join(models_dir, "meta_model.pkl"))
    le      = joblib.load(os.path.join(models_dir, "label_encoder.pkl"))
    fcols   = joblib.load(os.path.join(models_dir, "feature_cols.pkl"))
    return xgb, iso, meta, le, fcols


def compute_fused_offline(df, xgb, iso, meta, le, fcols):
    """Compute fused_risk for every row without going through the WebSocket."""
    normal_idx = list(le.classes_).index("Normal Traffic")

    X = df[fcols].fillna(0.0)

    # Model A
    proba    = xgb.predict_proba(X)
    xgb_risk = 1.0 - proba[:, normal_idx]

    # Model B -- calibrate iso min/max on this same dataset
    iso_raw = -iso.score_samples(X)
    iso_min, iso_max = iso_raw.min(), iso_raw.max()
    iso_risk = np.clip((iso_raw - iso_min) / (iso_max - iso_min + 1e-9), 0.0, 1.0)

    # Model C -- no ja3 data offline, use 0.0
    ja3_risk = np.zeros(len(df))

    meta_X = pd.DataFrame({"xgb_risk": xgb_risk, "iso_risk": iso_risk, "ja3_risk": ja3_risk})
    fused  = meta.predict_proba(meta_X)[:, 1] * 100.0

    return xgb_risk, iso_risk, fused


# ── Payload builder ──────────────────────────────────────────────────────────
def build_payload(row, fcols, mfa, healthy, location, hours, ja3, row_idx, label):
    feature_values = {
        col: (0.0 if pd.isna(row[col]) else float(row[col]))
        for col in fcols
    }
    return {
        "flow_id":        f"QTEST-{str(label).upper().replace(' ','_')}-row{row_idx}",
        "source_ip":      "203.0.113.42",
        **feature_values,
        "mfa_on":         mfa,
        "device_healthy": healthy,
        "known_location": location,
        "normal_hours":   hours,
        "ja3_risk":       ja3,
    }


# ── Main ─────────────────────────────────────────────────────────────────────
async def main():
    sep  = "=" * 90
    sep2 = "-" * 90

    # 1. Load data and models
    print(f"[*] Loading {CSV_PATH} ...")
    df = pd.read_csv(CSV_PATH)
    print(f"    Total rows: {len(df):,}")

    print("[*] Loading models and scoring all rows offline ...")
    xgb, iso, meta, le, fcols = load_models()
    normal_idx = list(le.classes_).index("Normal Traffic")

    xgb_risk, iso_risk, fused_risk = compute_fused_offline(df, xgb, iso, meta, le, fcols)

    # attack_prob = Model A's non-Normal probability
    proba      = xgb.predict_proba(df[fcols].fillna(0.0))
    attack_prob = 1.0 - proba[:, normal_idx]

    df["attack_prob"] = attack_prob
    df["fused_risk"]  = fused_risk

    # 2. Find borderline rows: uncertain XGBoost AND fused in Quarantine window
    lo_f, hi_f = FUSED_QUARANTINE_WINDOW
    borderline = df[
        (df["attack_prob"] >= BORDER_LO) &
        (df["attack_prob"] <= BORDER_HI) &
        (df["fused_risk"]  >= lo_f) &
        (df["fused_risk"]  <  hi_f)
    ].copy()

    borderline = borderline.sort_values("fused_risk", ascending=False).head(MAX_ROWS)

    print(f"\n[*] Borderline rows (attack_prob {BORDER_LO}-{BORDER_HI}, "
          f"fused_risk {lo_f}-{hi_f}): {len(borderline)} found")
    if not borderline.empty:
        cols_show = ["true_label", "attack_prob", "fused_risk"]
        print(borderline[cols_show].to_string())

    # 3. Send borderline rows through /ws
    if borderline.empty:
        print("\n[!] No borderline rows found — skipping WS phase. See distribution below.")
    else:
        print(f"\n[*] Connecting to {WS_URL} ...")
        async with websockets.connect(WS_URL) as ws:
            for _, row in borderline.iterrows():
                label    = row["true_label"]
                row_idx  = row.name
                off_risk = row["fused_risk"]
                ap       = row["attack_prob"]

                print(f"\n{sep2}")
                print(f"  Row {row_idx:>5d} | label={label:<18s} | "
                      f"attack_prob={ap:.4f} | offline_fused={off_risk:.2f}")
                print(sep2)

                for (trust_label, mfa, healthy, loc, hrs) in TRUST_COMBOS:
                    for ja3 in JA3_VALUES:
                        payload = build_payload(row, fcols, mfa, healthy, loc, hrs, ja3, row_idx, label)

                        await ws.send(json.dumps(payload))
                        resp = json.loads(await ws.recv())

                        action      = resp["action"]
                        trust_score = resp["trust_score"]
                        live_risk   = resp["fused_risk_score"]
                        trust_band  = resp["trust_band"]
                        r_band      = ("High"   if live_risk >= 70 else
                                       "Medium" if live_risk >= 30 else "Low")

                        print(f"    {trust_label:<28s}  ja3={ja3}  "
                              f"trust={trust_score:.0f}({trust_band})  "
                              f"risk={live_risk:.2f}({r_band})  -> {action}")

                        if action == "Quarantine":
                            print(f"\n{sep}")
                            print("  *** QUARANTINE FOUND! ***")
                            print(sep)
                            print(f"  Row index    : {row_idx}")
                            print(f"  Dataset label: {label}")
                            print(f"  Trust flags  : mfa={mfa}, device_healthy={healthy}, "
                                  f"known_location={loc}, normal_hours={hrs}")
                            print(f"  ja3_risk     : {ja3}")
                            print(f"  trust_score  : {trust_score:.0f} ({trust_band})")
                            print(f"  fused_risk   : {live_risk:.2f} ({r_band})")
                            print(f"  reason       : {resp['reason']}")
                            print(f"\n--- WINNING PAYLOAD (copy-paste ready) ---")
                            print(json.dumps(payload, indent=2))
                            print(f"\n--- FULL SERVER RESPONSE ---")
                            print(json.dumps(resp, indent=2))
                            print(sep)
                            return   # done

    # 4. No Quarantine found — print full distribution diagnosis
    print(f"\n{sep}")
    print("  NO Quarantine produced. Full fused_risk distribution across ALL rows:")
    print(sep)

    # Histogram-style breakdown
    bands = [
        ("0-10   (very low)",    0,   10),
        ("10-30  (low)",        10,   30),
        ("30-50  (med-low)",    30,   50),
        ("50-70  (medium)",     50,   70),
        ("70-90  (high/Q-zone)",70,   90),
        ("90-100 (override->Block)", 90, 100.001),
    ]
    fr = df["fused_risk"]
    print(f"\n  total rows : {len(fr):,}")
    print(f"  min        : {fr.min():.4f}")
    print(f"  max        : {fr.max():.4f}")
    print(f"  mean       : {fr.mean():.4f}")
    print(f"  median     : {fr.median():.4f}")
    print()
    print(f"  {'Band':<32s}  {'Count':>7}  {'%':>6}  bar")
    print(f"  {'-'*70}")
    for label, lo, hi in bands:
        n   = int(((fr >= lo) & (fr < hi)).sum())
        pct = n / len(fr) * 100
        bar = "#" * int(pct / 2)
        print(f"  {label:<32s}  {n:>7,}  {pct:>5.1f}%  {bar}")

    print(f"\n  Borderline rows (attack_prob {BORDER_LO}-{BORDER_HI}) regardless of fused_risk:")
    all_border = df[(df["attack_prob"] >= BORDER_LO) & (df["attack_prob"] <= BORDER_HI)]
    print(f"    count: {len(all_border)}")
    if not all_border.empty:
        print(all_border[["true_label","attack_prob","fused_risk"]].to_string())

    print(f"\n  Conclusion: the model is {'bimodal' if fr.median() < 5 else 'not bimodal'}.")
    in_window = int(((fr >= 30) & (fr < 90)).sum())
    print(f"  Rows with fused_risk in the Quarantine window (30-90): {in_window:,} / {len(fr):,}")


if __name__ == "__main__":
    asyncio.run(main())
