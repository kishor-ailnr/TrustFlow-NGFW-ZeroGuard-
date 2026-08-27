# backend/pipeline.py

import os
import sys
import asyncio
import joblib
import pandas as pd
import numpy as np
import shap

# Ensure root directory is in sys.path for top-level module imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.trust_engine import compute_trust_score
from backend.decision_engine import decide_action, simulate_vlan_quarantine
from telegram_alert import send_telegram_alert_async
from honeypot_redirect import trigger_honeypot_connection

# Load models and preprocessing artifacts
MODELS_DIR = os.path.join(ROOT_DIR, "models")
xgb_model = joblib.load(os.path.join(MODELS_DIR, "xgb_model.pkl"))
label_encoder = joblib.load(os.path.join(MODELS_DIR, "label_encoder.pkl"))
feature_cols = joblib.load(os.path.join(MODELS_DIR, "feature_cols.pkl"))
iso_forest = joblib.load(os.path.join(MODELS_DIR, "iso_forest.pkl"))
meta_model = joblib.load(os.path.join(MODELS_DIR, "meta_model.pkl"))

# Initialize SHAP explainer for XGBoost
explainer = shap.TreeExplainer(xgb_model)
feature_names = np.array(feature_cols)

# Calibrate Isolation Forest min/max limits
# Derived from replay dataset baseline distribution
try:
    replay_path = os.path.join(ROOT_DIR, "data", "replay_holdout.csv")
    if os.path.exists(replay_path):
        replay_df = pd.read_csv(replay_path)
        X_replay = replay_df[feature_cols]
        iso_scores_replay = -iso_forest.score_samples(X_replay)
        iso_min = float(iso_scores_replay.min())
        iso_max = float(iso_scores_replay.max())
    else:
        iso_min = 0.31877
        iso_max = 0.75165
except Exception:
    iso_min = 0.31877
    iso_max = 0.75165

# Normal traffic class index in label encoder
normal_class_idx = list(label_encoder.classes_).index("Normal Traffic") if "Normal Traffic" in label_encoder.classes_ else 0

# Meta-learner coefficients and model names for attribution
meta_coefs = meta_model.coef_[0]  # [xgb_risk, iso_risk, ja3_risk]
submodel_names = ["AI classifier", "Anomaly detector", "TLS/JA3 intel"]

async def trigger_honeypot_connection_async(
    flow_id: str,
    source_ip: str = "203.0.113.42",
    target_host: str = "localhost",
    target_port: int = 2222
):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        trigger_honeypot_connection,
        flow_id,
        source_ip,
        target_host,
        target_port
    )

async def process_flow(flow_data: dict) -> dict:
    """
    Orchestration function for processing a single incoming network flow:
    a. Runs ensemble scoring (XGBoost, Isolation Forest, JA3 check, Meta-learner)
    b. Computes SHAP feature and sub-model attribution
    c. Computes trust score from posture signals
    d. Decides action via decision engine matrix
    e. Dispatches async quarantine / alerting tasks if required
    f. Returns combined structured result
    """
    flow_id = str(flow_data.get("flow_id", "UNKNOWN"))
    source_ip = str(flow_data.get("source_ip", "192.0.2.100"))

    # 1. Prepare feature vector for ML models
    row_dict = {col: float(flow_data.get(col, 0.0)) for col in feature_cols}
    df_row = pd.DataFrame([row_dict])[feature_cols]

    # --- a. Ensemble Scoring Pipeline ---
    # Model A: XGBoost supervised risk score (0.0 - 1.0)
    proba = xgb_model.predict_proba(df_row)
    xgb_risk = float(1.0 - proba[0, normal_class_idx])
    model_a_score = xgb_risk

    # Model B: Isolation Forest unsupervised anomaly risk score (0.0 - 1.0)
    raw_iso_score = float(-iso_forest.score_samples(df_row)[0])
    iso_risk = (raw_iso_score - iso_min) / (iso_max - iso_min) if (iso_max - iso_min) > 0 else 0.0
    iso_risk = float(np.clip(iso_risk, 0.0, 1.0))
    model_b_score = iso_risk

    # Model C: JA3 TLS intelligence risk score (0.0 - 1.0)
    # Check ja3_risk field or ja3_hash
    if "ja3_risk" in flow_data:
        ja3_risk = float(flow_data["ja3_risk"])
    else:
        ja3_risk = 0.0
    model_c_score = ja3_risk

    # Meta-learner fusion: Final fused risk score (0.0 - 100.0)
    meta_X = pd.DataFrame([[xgb_risk, iso_risk, ja3_risk]], columns=["xgb_risk", "iso_risk", "ja3_risk"])
    fused_risk_score = float(meta_model.predict_proba(meta_X)[0, 1] * 100.0)

    # --- b. SHAP & Sub-Model Explainability ---
    # SHAP values for XGBoost
    shap_raw = np.array(explainer.shap_values(df_row))
    if len(shap_raw.shape) == 3:  # (samples, features, classes)
        row_shap = shap_raw[0, :, proba[0].argmax()]
    elif len(shap_raw.shape) == 2:  # (samples, features)
        row_shap = shap_raw[0, :]
    else:
        row_shap = shap_raw.flatten()

    top2_idx = np.argsort(-np.abs(row_shap))[:2]
    top_shap_features = ", ".join(feature_names[top2_idx])

    # Sub-model attribution based on meta-learner weighted contributions
    contributions = np.array([xgb_risk, iso_risk, ja3_risk]) * meta_coefs
    primary_idx = int(np.argmax(contributions))
    primary_model = submodel_names[primary_idx]

    shap_attribution = {
        "primary_model": primary_model,
        "top_features": top_shap_features,
        "contributions": {
            "model_a_xgboost": float(contributions[0]),
            "model_b_isolation_forest": float(contributions[1]),
            "model_c_ja3": float(contributions[2])
        }
    }

    # Human-readable explanation text
    if fused_risk_score < 40:
        explanation = f"Allowed: consistent with normal traffic patterns (risk score {fused_risk_score:.0f}/100)"
    elif primary_model == "TLS/JA3 intel" and ja3_risk == 1.0:
        explanation = f"Flagged: TLS client fingerprint matches known malicious JA3 signature"
    elif primary_model == "Anomaly detector":
        explanation = f"Flagged: flow deviates from normal traffic baseline (unsupervised anomaly signal)"
    else:
        explanation = f"Flagged: classifier identified anomalous pattern in {top_shap_features}"

    # --- c. Trust Score Computation ---
    mfa_on = bool(flow_data.get("mfa_on", True))
    device_healthy = bool(flow_data.get("device_healthy", True))
    known_location = bool(flow_data.get("known_location", True))
    normal_hours = bool(flow_data.get("normal_hours", True))

    trust_result = compute_trust_score(
        mfa_on=mfa_on,
        device_healthy=device_healthy,
        known_location=known_location,
        normal_hours=normal_hours
    )
    trust_score = float(trust_result["trust_score"])
    trust_band = trust_result.get("trust_level", "High")

    # --- d. Decision Engine Action ---
    decision = decide_action(trust_score=trust_score, risk_score=fused_risk_score, source_ip=source_ip)
    action = decision["action"]
    reason = decision["reason"]

    # --- e. Quarantine Handling ---
    if action == "Quarantine":
        asyncio.create_task(
            trigger_honeypot_connection_async(flow_id, source_ip=source_ip)
        )
        simulate_vlan_quarantine(flow_id, source_ip)

    # --- f. Block Handling ---
    # Note: decide_action() already handles block_ip(source_ip) internally.

    # --- g. Telegram Alerting ---
    if action in ("Block", "Quarantine"):
        asyncio.create_task(
            send_telegram_alert_async(
                flow_id=flow_id,
                action=action.upper(),
                risk_score=fused_risk_score,
                trust_score=trust_score,
                reason=reason
            )
        )

    # --- h. Combined Response ---
    return {
        "flow_id": flow_id,
        "source_ip": source_ip,
        "model_a_score": round(model_a_score, 4),
        "model_b_score": round(model_b_score, 4),
        "model_c_score": round(model_c_score, 4),
        "fused_risk_score": round(fused_risk_score, 2),
        "shap_attribution": shap_attribution,
        "explanation": explanation,
        "trust_score": trust_score,
        "trust_band": trust_band,
        "action": action,
        "reason": reason
    }
