# backend/decision_engine.py
import datetime
from iptables_action import block_ip, list_rules
from honeypot_redirect import trigger_honeypot_connection
# In-memory VLAN quarantine state (simulated — no managed switch available)
vlan_quarantine_state = {}  # flow_id -> {"vlan_status": "QUARANTINED", "timestamp": ...}

def trust_band(score: float) -> str:
    if score >= 80:
        return "High"
    elif score >= 50:
        return "Medium"
    return "Low"

def risk_band(score: float) -> str:
    if score < 30:
        return "Low"
    elif score < 70:
        return "Medium"
    return "High"

# Trust genuinely changes the outcome here — same risk level can land
# on a different action depending on how trusted the session is.
DECISION_MATRIX = {
    ("High", "Low"): "Allow",
    ("High", "Medium"): "Allow",
    ("High", "High"): "Rate-limit",
    ("Medium", "Low"): "Allow",
    ("Medium", "Medium"): "Rate-limit",
    ("Medium", "High"): "Quarantine",
    ("Low", "Low"): "Rate-limit",
    ("Low", "Medium"): "Quarantine",
    ("Low", "High"): "Block",
}

def decide_action(trust_score: float, risk_score: float, source_ip: str = "192.0.2.100") -> dict:
    t_band = trust_band(trust_score)
    r_band = risk_band(risk_score)

    if risk_score >= 90:
        action = "Block"
        override = True
    else:
        action = DECISION_MATRIX[(t_band, r_band)]
        override = False

    reason = (
        f"Very high risk ({risk_score:.0f}) triggers an immediate block regardless of trust"
        if override else
        f"Trust={t_band} ({trust_score:.0f}) + Risk={r_band} ({risk_score:.0f}) -> {action}"
    )

    if action == "Block":
        before = list_rules()
        block_ip(source_ip)
        after = list_rules()

        print("BEFORE:\n", before)
        print("AFTER:\n", after)

    return {
        "action": action,
        "trust_band": t_band,
        "risk_band": r_band,
        "override_applied": override,
        "reason": reason,
    }

if __name__ == "__main__":
    result = decide_action(
        trust_score=20,
        risk_score=95
    )

    print(result)

    

def simulate_vlan_quarantine(flow_id: str, source_ip: str):
    """
    Simulated VLAN quarantine action. No managed switch is available in this
    environment, so this sets a state flag and timestamp instead of issuing
    a real switch-port VLAN reassignment command. This is flagged honestly
    in the dashboard and demo narrative as a simulated enforcement action.
    """
    vlan_quarantine_state[flow_id] = {
        "source_ip": source_ip,
        "vlan_status": "QUARANTINED",
        "simulated": True,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    print(f"[VLAN-SIM] Flow {flow_id} ({source_ip}) flagged as quarantined (simulated)")
    return vlan_quarantine_state[flow_id]


def get_vlan_state(flow_id: str):
    """Returns current simulated VLAN state for a flow, or None if not quarantined."""
    return vlan_quarantine_state.get(flow_id)


def get_all_vlan_states():
    """Returns the full simulated VLAN quarantine table — used by the dashboard endpoint."""
    return vlan_quarantine_state