# backend/redteam/run_redteam_test.py

import os
import json
import joblib
import pandas as pd
import numpy as np
from backend.decision_engine import decide_action
from backend.redteam.perturb import apply_evasion_perturbation

# Define default trust score for red team evaluation
TRUST_SCORE = 20.0  # Low trust triggers Block/Quarantine on attacks

def main():
    print("=== Phase 7: Adversarial Red-Teaming - Evasion Test ===")

    # 1. Load models and specifications
    print("[RedTeam] Loading model artifacts...")
    xgb_model = joblib.load("models/xgb_model.pkl")
    label_encoder = joblib.load("models/label_encoder.pkl")
    feature_cols = joblib.load("models/feature_cols.pkl")
    iso_forest = joblib.load("models/iso_forest.pkl")
    meta_model = joblib.load("models/meta_model.pkl")

    # 2. Load replay holdout to compute scaling limits for Isolation Forest
    print("[RedTeam] Calibrating Isolation Forest risk score limits...")
    replay_df = pd.read_csv("data/replay_holdout.csv")
    X_replay = replay_df[feature_cols]
    iso_scores_replay = -iso_forest.score_samples(X_replay)
    iso_min = iso_scores_replay.min()
    iso_max = iso_scores_replay.max()

    def get_risk_score(flow_row, ja3_risk=0.0):
        # Convert flow_row to DataFrame with correct columns and order
        df_row = pd.DataFrame([flow_row])[feature_cols]
        
        # XGBoost risk score
        proba = xgb_model.predict_proba(df_row)
        normal_idx = list(label_encoder.classes_).index("Normal Traffic")
        xgb_risk = 1.0 - proba[0, normal_idx]
        
        # Isolation Forest risk score (scaled)
        raw_score = -iso_forest.score_samples(df_row)[0]
        iso_risk = (raw_score - iso_min) / (iso_max - iso_min)
        iso_risk = np.clip(iso_risk, 0.0, 1.0)
        
        # Meta-learner fusion
        meta_X = np.array([[xgb_risk, iso_risk, ja3_risk]])
        flow_risk = meta_model.predict_proba(meta_X)[0, 1] * 100
        
        return flow_risk

    # 3. Load malicious samples
    sample_path = "backend/redteam/data/malicious_sample.csv"
    if not os.path.exists(sample_path):
        raise FileNotFoundError(f"Malicious sample CSV not found at {sample_path}. Run select_flows.py first.")

    print(f"[RedTeam] Loading malicious flows from {sample_path}...")
    df_samples = pd.read_csv(sample_path)
    
    per_flow_results = []
    still_detected_count = 0
    evaded_count = 0

    print("[RedTeam] Running before/after evasion tests...")
    for idx, row in df_samples.iterrows():
        # Baseline run
        baseline_risk = get_risk_score(row)
        baseline_decision = decide_action(TRUST_SCORE, baseline_risk)
        baseline_action = baseline_decision["action"]
        
        # Apply perturbation
        perturbed_row = apply_evasion_perturbation(row)
        
        # Perturbed run
        perturbed_risk = get_risk_score(perturbed_row)
        perturbed_decision = decide_action(TRUST_SCORE, perturbed_risk)
        perturbed_action = perturbed_decision["action"]
        
        # Determine if still caught (Quarantine or Block) or evaded (Allow or Rate-limit)
        still_caught = perturbed_action in ["Quarantine", "Block"]
        if still_caught:
            still_detected_count += 1
        else:
            evaded_count += 1
            
        per_flow_results.append({
            "flow_index": int(idx),
            "baseline_action": baseline_action,
            "baseline_risk": round(float(baseline_risk), 2),
            "perturbed_action": perturbed_action,
            "perturbed_risk": round(float(perturbed_risk), 2),
            "still_caught": still_caught
        })
        
        print(f"  Flow {idx} ({row['Attack Type']}): "
              f"Risk: {baseline_risk:.1f} ({baseline_action}) -> "
              f"Perturbed Risk: {perturbed_risk:.1f} ({perturbed_action}) | "
              f"{'Caught' if still_caught else 'EVADED'}")

    # 4. Save results
    results = {
        "total_tested": len(df_samples),
        "still_detected": still_detected_count,
        "evaded": evaded_count,
        "summary": f"{still_detected_count}/{len(df_samples)} attacks still detected after perturbation",
        "per_flow": per_flow_results
    }
    
    results_dir = "backend/redteam/results"
    os.makedirs(results_dir, exist_ok=True)
    results_path = os.path.join(results_dir, "evasion_results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"\n[RedTeam] Evasion test completed. Results saved to {results_path}")
    print(f"Summary: {results['summary']}\n")

if __name__ == "__main__":
    main()
