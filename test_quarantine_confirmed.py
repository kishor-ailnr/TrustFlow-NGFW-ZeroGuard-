"""
test_quarantine_confirmed.py
============================
Loads quarantine_test_payload.json, sends it to /ws once, prints the
full response, and asserts action == "Quarantine".

Usage:
    uvicorn backend.main:app --host 127.0.0.1 --port 8000
    python test_quarantine_confirmed.py
"""

import json
import asyncio
import os
import websockets

PAYLOAD_FILE = "quarantine_test_payload.json"
WS_URL       = os.getenv("WS_URL", "ws://127.0.0.1:8000/ws")


async def main():
    if not os.path.exists(PAYLOAD_FILE):
        raise FileNotFoundError(
            f"{PAYLOAD_FILE} not found. "
            "Run test_quarantine_flow.py first to generate it."
        )

    with open(PAYLOAD_FILE) as f:
        payload = json.load(f)

    print(f"[*] Loaded payload from {PAYLOAD_FILE}")
    print(f"    flow_id   : {payload['flow_id']}")
    print(f"    source_ip : {payload['source_ip']}")
    print(f"    mfa_on={payload['mfa_on']}  device_healthy={payload['device_healthy']}  "
          f"known_location={payload['known_location']}  normal_hours={payload['normal_hours']}")
    print(f"    ja3_risk  : {payload['ja3_risk']}")

    print(f"\n[*] Connecting to {WS_URL} ...")
    async with websockets.connect(WS_URL) as ws:
        await ws.send(json.dumps(payload))
        response = json.loads(await ws.recv())

    sep = "=" * 60
    print(f"\n{sep}\nFULL RESPONSE FROM /ws\n{sep}")
    print(json.dumps(response, indent=2))

    print(f"\n{sep}\nSUMMARY\n{sep}")
    print(f"  model_a_score   : {response['model_a_score']}")
    print(f"  model_b_score   : {response['model_b_score']}")
    print(f"  model_c_score   : {response['model_c_score']}")
    print(f"  fused_risk_score: {response['fused_risk_score']} / 100")
    print(f"  trust_score     : {response['trust_score']} / 100  ({response['trust_band']})")
    print(f"  primary_model   : {response['shap_attribution']['primary_model']}")
    print(f"  top_features    : {response['shap_attribution']['top_features']}")
    print(f"  explanation     : {response['explanation']}")
    print(f"  action          : {response['action']}")
    print(f"  reason          : {response['reason']}")
    print(sep)

    assert response["action"] == "Quarantine", (
        f"\n[FAIL] Expected action='Quarantine', got '{response['action']}'\n"
        f"       fused_risk={response['fused_risk_score']:.2f}, "
        f"trust={response['trust_score']:.0f} ({response['trust_band']})"
    )
    print(f"\n[PASS]  action == 'Quarantine' confirmed.")


if __name__ == "__main__":
    asyncio.run(main())
