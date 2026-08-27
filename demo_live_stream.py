"""
demo_live_stream.py
===================
Interactive Live Demo Streamer for TrustFlow NGFW Hackathon Presentation.

Streams diverse network flows (Benign, Rate-limit, Quarantine, Block) into the
dashboard via ws://127.0.0.1:8000/ws so the judges can watch real-time
zero-trust decisions, SHAP attributions, and mitigation actions live.

Usage:
    venv\\Scripts\\python.exe demo_live_stream.py
"""

import os
import json
import time
import asyncio
import random
import pandas as pd
import joblib
import websockets

WS_URL = os.getenv("WS_URL", "ws://127.0.0.1:8000/ws")
CSV_PATH = "data/replay_holdout.csv"

# Pre-defined curated scenarios to ensure every action is demonstrated clearly
SCENARIOS = [
    {
        "name": "Trusted User - Normal Browsing (Allow)",
        "label": "Normal Traffic",
        "mfa": True, "healthy": True, "location": True, "hours": True, "ja3": 0.0,
        "desc": "High Trust + Low Risk -> Allow"
    },
    {
        "name": "Off-hours User - Unusual Volume (Rate-limit)",
        "label": "Normal Traffic",
        "mfa": True, "healthy": False, "location": False, "hours": False, "ja3": 0.2,
        "desc": "Medium Trust + Low/Med Risk -> Rate-limit"
    },
    {
        "name": "Suspicious Port Scan on Managed Device (Quarantine)",
        "label": "Port Scanning",
        "row_index": 21187,
        "mfa": True, "healthy": True, "location": False, "hours": False, "ja3": 0.0,
        "desc": "Medium Trust + Borderline Attack -> Redirect to Cowrie Honeypot"
    },
    {
        "name": "External High-Volume DoS Flood (Block)",
        "label": "DoS",
        "mfa": False, "healthy": False, "location": False, "hours": False, "ja3": 0.8,
        "desc": "Zero Trust + Critical Risk -> Real iptables DROP Rule"
    },
    {
        "name": "Brute Force Password Attempt (Block)",
        "label": "Brute Force",
        "mfa": False, "healthy": False, "location": False, "hours": False, "ja3": 0.6,
        "desc": "Untrusted Source + High Risk -> Block + Telegram Alert"
    },
    {
        "name": "Corporate Endpoint - Routine Activity (Allow)",
        "label": "Normal Traffic",
        "mfa": True, "healthy": True, "location": True, "hours": True, "ja3": 0.0,
        "desc": "Full Posture Compliance -> Instant Allow"
    },
]

def load_dataset_and_features():
    feature_cols = joblib.load("models/feature_cols.pkl")
    df = pd.read_csv(CSV_PATH)
    return df, feature_cols

def build_flow_payload(row, feature_cols, scenario, counter):
    features = {c: (0.0 if pd.isna(row[c]) else float(row[c])) for c in feature_cols}
    ip_last = random.randint(10, 240)
    source_ip = f"192.168.1.{ip_last}" if scenario.get("healthy") else f"203.0.113.{ip_last}"
    
    return {
        "flow_id": f"DEMO-{scenario['label'].upper().replace(' ', '_')}-{counter:03d}",
        "source_ip": source_ip,
        **features,
        "mfa_on": scenario["mfa"],
        "device_healthy": scenario["healthy"],
        "known_location": scenario["location"],
        "normal_hours": scenario["hours"],
        "ja3_risk": scenario["ja3"]
    }

async def stream_demo(continuous=True, delay=2.0):
    print("=" * 70)
    print(" [TrustFlow NGFW] Live Demo Traffic Streamer")
    print(f" Connecting to: {WS_URL}")
    print(f" Dashboard UI : http://localhost:5173/")
    print("=" * 70)

    df, feature_cols = load_dataset_and_features()

    async with websockets.connect(WS_URL) as ws:
        print(" [OK] WebSocket connection established!")
        print(" [*] Streaming live security flows to dashboard...\n")
        
        counter = 1
        while True:
            for s in SCENARIOS:
                if "row_index" in s and s["row_index"] in df.index:
                    row = df.loc[s["row_index"]]
                else:
                    matching = df[df["true_label"] == s["label"]]
                    row = matching.sample(1).iloc[0] if not matching.empty else df.iloc[0]

                payload = build_flow_payload(row, feature_cols, s, counter)
                
                await ws.send(json.dumps(payload))
                raw_resp = await ws.recv()
                resp = json.loads(raw_resp)

                action = resp.get("action", "Unknown")
                risk = resp.get("fused_risk_score", 0.0)
                trust = resp.get("trust_score", 0.0)
                
                icons = {"Allow": "[ALLOW]", "Rate-limit": "[RATE-LIMIT]", "Quarantine": "[QUARANTINE]", "Block": "[BLOCK]"}
                badge = icons.get(action, f"[{action}]")

                print(f" [{counter:03d}] {badge:<13} | Risk: {risk:>5.1f} | Trust: {trust:>4.0f} | Scenario: {s['name']}")

                counter += 1
                await asyncio.sleep(delay)

            if not continuous:
                break
            print("\n" + "-" * 70)
            print(" [*] Completed demo cycle. Looping next batch of live flows...")
            print("-" * 70 + "\n")

if __name__ == "__main__":
    import sys
    delay = 2.0
    if len(sys.argv) > 1:
        try:
            delay = float(sys.argv[1])
        except ValueError:
            pass
    try:
        asyncio.run(stream_demo(continuous=True, delay=delay))
    except KeyboardInterrupt:
        print("\n\n [!] Live demo stream stopped by user.")
