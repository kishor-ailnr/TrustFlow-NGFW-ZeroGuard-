# backend/trust_engine.py

def compute_trust_score(mfa_on: bool, device_healthy: bool, known_location: bool, normal_hours: bool) -> dict:
    weights = {
        "mfa_on": 30,
        "device_healthy": 30,
        "known_location": 25,
        "normal_hours": 15,
    }
    signals = {
        "mfa_on": mfa_on,
        "device_healthy": device_healthy,
        "known_location": known_location,
        "normal_hours": normal_hours,
    }

    score = sum(weights[k] for k, v in signals.items() if v)

    if score >= 80:
        level = "High"
    elif score >= 50:
        level = "Medium"
    else:
        level = "Low"

    reasons = [f"{k.replace('_', ' ')} failed (-{weights[k]})" for k, v in signals.items() if not v]

    return {
        "trust_score": score,
        "trust_level": level,
        "signals": signals,
        "reasons": reasons if reasons else ["All identity and posture checks passed"],
    }