# test_integration.py

import os
import sys
import json
import asyncio
import pandas as pd
import requests
import websockets

async def test_ws():
    print("\n--- 1. Testing WebSocket /ws with Raw Flow Features from CSV ---")
    # Read one raw flow from data/replay_holdout.csv
    csv_path = "data/replay_holdout.csv"
    if not os.path.exists(csv_path):
        csv_path = "data/replay_enriched.csv"

    df = pd.read_csv(csv_path, nrows=5)
    # Select an attack flow or first flow
    row = df.iloc[0].to_dict()
    row["flow_id"] = "FLOW-LIVE-TEST-001"
    row["source_ip"] = "192.168.10.50"
    row["mfa_on"] = True
    row["device_healthy"] = False
    row["known_location"] = True
    row["normal_hours"] = True

    # Ensure NaN/inf values are serialized properly if any
    clean_payload = {}
    for k, v in row.items():
        if pd.isna(v):
            clean_payload[k] = 0.0
        else:
            clean_payload[k] = v

    uri = "ws://127.0.0.1:8000/ws"
    print(f"Connecting to {uri}...")
    async with websockets.connect(uri) as ws:
        print(f"Sending raw flow payload for flow_id='{clean_payload['flow_id']}' with {len(clean_payload)} fields...")
        await ws.send(json.dumps(clean_payload))

        raw_resp = await ws.recv()
        resp = json.loads(raw_resp)
        print("\nWebSocket Full Response:")
        print(json.dumps(resp, indent=2))

        # Assertions for non-null, real values
        required_fields = [
            "flow_id", "source_ip", "model_a_score", "model_b_score", "model_c_score",
            "fused_risk_score", "shap_attribution", "trust_score", "action", "reason"
        ]
        for field in required_fields:
            assert field in resp, f"Missing field {field} in response"
            assert resp[field] is not None, f"Field {field} is None"

        assert isinstance(resp["model_a_score"], (int, float)), "model_a_score is not a number"
        assert isinstance(resp["model_b_score"], (int, float)), "model_b_score is not a number"
        assert isinstance(resp["model_c_score"], (int, float)), "model_c_score is not a number"
        assert isinstance(resp["fused_risk_score"], (int, float)), "fused_risk_score is not a number"
        assert isinstance(resp["trust_score"], (int, float)), "trust_score is not a number"
        assert resp["action"] in ("Allow", "Rate-limit", "Quarantine", "Block"), f"Unexpected action {resp['action']}"
        print("\n[PASS] All WebSocket response fields validated successfully!")

def test_rest_endpoints():
    print("\n--- 2. Testing REST Endpoints ---")
    base_url = "http://127.0.0.1:8000"

    # GET /api/pipeline-info
    r_pipe = requests.get(f"{base_url}/api/pipeline-info")
    print(f"GET /api/pipeline-info: status={r_pipe.status_code}")
    print(json.dumps(r_pipe.json(), indent=2))
    assert r_pipe.status_code == 200
    assert "model_a" in r_pipe.json()
    assert "meta_learner" in r_pipe.json()

    # GET /api/federated-status
    r_fed = requests.get(f"{base_url}/api/federated-status")
    print(f"GET /api/federated-status: status={r_fed.status_code}, length={len(r_fed.json())}")
    assert r_fed.status_code == 200

    # GET /api/redteam-status
    r_red = requests.get(f"{base_url}/api/redteam-status")
    print(f"GET /api/redteam-status: status={r_red.status_code}, summary={r_red.json().get('summary')}")
    assert r_red.status_code == 200

    # GET /api/vlan-status
    r_vlan = requests.get(f"{base_url}/api/vlan-status")
    print(f"GET /api/vlan-status: status={r_vlan.status_code}, states={r_vlan.json()}")
    assert r_vlan.status_code == 200

    # GET /api/honeypot-session/TEST-FLOW
    r_honey = requests.get(f"{base_url}/api/honeypot-session/TEST-FLOW-QUARANTINE")
    print(f"GET /api/honeypot-session: status={r_honey.status_code}, session={r_honey.json().get('session_id')}")
    assert r_honey.status_code == 200
    assert "commands" in r_honey.json()
    assert len(r_honey.json()["commands"]) > 0

    # POST /trust-score
    r_trust = requests.post(f"{base_url}/trust-score", json={"mfa_on": True, "device_healthy": True, "known_location": True, "normal_hours": True})
    print(f"POST /trust-score: status={r_trust.status_code}, score={r_trust.json().get('trust_score')}")
    assert r_trust.status_code == 200
    assert r_trust.json()["trust_score"] == 100

    # POST /decide
    r_decide = requests.post(f"{base_url}/decide", json={"trust_score": 20, "risk_score": 95})
    print(f"POST /decide: status={r_decide.status_code}, action={r_decide.json().get('action')}")
    assert r_decide.status_code == 200
    assert r_decide.json()["action"] == "Block"

    print("\n[PASS] All REST endpoints tested and validated successfully!")

if __name__ == "__main__":
    test_rest_endpoints()
    asyncio.run(test_ws())
