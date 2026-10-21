# backend/soc_agent.py
import json
import csv
import os
from datetime import datetime
import ollama

INCIDENT_LOG = "data/incident_log.csv"
SEVERITY = {"Allow": 0, "Rate-limit": 1, "Quarantine": 2, "Block": 3}
SEVERITY_NAMES = ["Allow", "Rate-limit", "Quarantine", "Block"]

def _log_incident(flow_id, action, severity, message):
    file_exists = os.path.exists(INCIDENT_LOG)
    with open(INCIDENT_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "flow_id", "action", "severity", "message"])
        writer.writerow([datetime.now().isoformat(), flow_id, action, severity, message])

def tool_confirm_action(flow_id: str, action: str, reason: str) -> dict:
    _log_incident(flow_id, action, "info", f"Agent CONFIRMED. Reason: {reason}")
    return {"final_action": action, "overridden": False, "agent_reason": reason}

def tool_escalate_action(flow_id: str, new_action: str, reason: str) -> dict:
    _log_incident(flow_id, new_action, "warning", f"Agent ESCALATED. Reason: {reason}")
    return {"final_action": new_action, "overridden": True, "agent_reason": reason}

def tool_deescalate_action(flow_id: str, new_action: str, reason: str) -> dict:
    _log_incident(flow_id, new_action, "info", f"Agent DE-ESCALATED. Reason: {reason}")
    return {"final_action": new_action, "overridden": True, "agent_reason": reason}

TOOL_IMPL = {
    "confirm_action": tool_confirm_action,
    "escalate_action": tool_escalate_action,
    "deescalate_action": tool_deescalate_action,
}

TOOL_SCHEMA = [
    {"type": "function", "function": {
        "name": "confirm_action",
        "description": "Confirm the decision engine's suggested action is correct - no change needed.",
        "parameters": {"type": "object", "properties": {
            "flow_id": {"type": "string"},
            "action": {"type": "string", "enum": ["Allow", "Rate-limit", "Quarantine", "Block"]},
            "reason": {"type": "string"},
        }, "required": ["flow_id", "action", "reason"]},
    }},
    {"type": "function", "function": {
        "name": "escalate_action",
        "description": "Override with a MORE severe action than suggested, because the evidence justifies it.",
        "parameters": {"type": "object", "properties": {
            "flow_id": {"type": "string"},
            "new_action": {"type": "string", "enum": ["Rate-limit", "Quarantine", "Block"]},
            "reason": {"type": "string"},
        }, "required": ["flow_id", "new_action", "reason"]},
    }},
    {"type": "function", "function": {
        "name": "deescalate_action",
        "description": "Override with a LESS severe action, because the decision engine is being too cautious.",
        "parameters": {"type": "object", "properties": {
            "flow_id": {"type": "string"},
            "new_action": {"type": "string", "enum": ["Allow", "Rate-limit", "Quarantine"]},
            "reason": {"type": "string"},
        }, "required": ["flow_id", "new_action", "reason"]},
    }},
]

SYSTEM_PROMPT = """
You are TrustFlow NGFW's network security decision agent.

You MUST call exactly one tool.

You are reviewing a decision already produced by the decision engine.

Actions have this severity order:

Allow < Rate-limit < Quarantine < Block

Decision rules:

1. If ja3_flagged is true and the JA3 fingerprint is known malicious,
   escalate the action to Block unless the suggested action is already Block.

2. If risk_score >= 85,
   escalate the action to Block unless the suggested action is already Block.

3. If risk_score >= 60 OR trust_score <= 50,
   the appropriate action is at least Quarantine.
   Escalate if the suggested action is less severe than Quarantine.

4. If risk_score < 60 AND trust_score > 50 AND ja3_flagged is false,
   the flow can be allowed.
   De-escalate if the suggested action is more severe than Allow.

5. If the suggested action is already appropriate for the evidence,
   confirm_action.

6. Never de-escalate a flow that has a known-malicious JA3 fingerprint.

7. Never allow a flow when ja3_flagged is true.

Always choose exactly one of:
- confirm_action
- escalate_action
- deescalate_action
"""

def run_soc_agent(flow_id: str, trust_score: float, risk_score: float, suggested_action: str,
                   explanation: str, ja3_flagged: bool = False, model: str = "llama3.2") -> dict:
    user_prompt = (
        f"Flow ID: {flow_id}\nTrust score: {trust_score}/100\nAI risk score: {risk_score}/100\n"
        f"Decision engine's suggested action: {suggested_action}\n"
        f"Detection explanation: {explanation}\n"
        f"TLS/JA3 threat-intel match: {'YES - known malicious fingerprint' if ja3_flagged else 'No match'}\n\n"
        f"Review this and call the appropriate tool."
    )
    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}],
            tools=TOOL_SCHEMA,
            options={"temperature": 0},
        )
    except Exception as e:
        return {"final_action": suggested_action, "overridden": False, "agent_used": False,
                "agent_reason": f"Agent unavailable ({e}); kept original decision-engine action."}

    tool_calls = response["message"].get("tool_calls")
    if not tool_calls:
        return {"final_action": suggested_action, "overridden": False, "agent_used": True,
                "agent_reason": "Agent returned no tool call; kept original action.",
                "raw_reply": response["message"].get("content")}

    call = tool_calls[0]
    fn_name = call["function"]["name"]
    args = call["function"]["arguments"]
    if isinstance(args, str):
        args = json.loads(args)
    args.setdefault("flow_id", flow_id)

    if fn_name not in TOOL_IMPL:
        return {"final_action": suggested_action, "overridden": False, "agent_used": True,
                "agent_reason": f"Agent called unknown tool '{fn_name}'; kept original action."}

    # Guardrail: the tool's target must actually match its own semantic direction.
    # If escalate/deescalate disagree with their own target severity, don't guess
    # which one was "meant" - discard the override and keep the safe, deterministic action.
    target_action = args.get("new_action") or args.get("action")
    orig_rank = SEVERITY.get(suggested_action, 0)
    target_rank = SEVERITY.get(target_action, orig_rank)

    if fn_name == "escalate_action" and target_rank <= orig_rank:
        _log_incident(flow_id, suggested_action, "warning",
                       f"Discarded inconsistent escalate_action (target '{target_action}' not more severe than '{suggested_action}')")
        return {"final_action": suggested_action, "overridden": False, "agent_used": True, "tool_called": fn_name,
                "agent_reason": f"Discarded inconsistent override (escalate to '{target_action}' wasn't actually more severe); kept original action."}

    if fn_name == "deescalate_action" and target_rank >= orig_rank:
        _log_incident(flow_id, suggested_action, "warning",
                       f"Discarded inconsistent deescalate_action (target '{target_action}' not less severe than '{suggested_action}')")
        return {"final_action": suggested_action, "overridden": False, "agent_used": True, "tool_called": fn_name,
                "agent_reason": f"Discarded inconsistent override (de-escalate to '{target_action}' wasn't actually less severe); kept original action."}

    # Cap single-step deescalation: never let one agent call drop more
    # than one severity rank at a time, regardless of trust_score. This
    # prevents a Quarantine-worthy flow from being waved straight to
    # Allow in one call even when trust is Medium/High and the floor
    # above doesn't apply.
    if fn_name == "deescalate_action" and (orig_rank - target_rank) > 1:
        capped_action = SEVERITY_NAMES[orig_rank - 1]  # one step down only
        _log_incident(flow_id, capped_action, "warning",
                       f"Capped agent's '{target_action}' - deescalation "
                       f"limited to one severity step per call "
                       f"(orig={suggested_action}, requested={target_action})")
        target_action = capped_action
        target_rank = orig_rank - 1
        args["new_action"] = capped_action

    # Hard zero-trust floor: mirrors the policy's own Rule 3. Never let any
    # override land below Quarantine when trust_score <= 50 or risk_score >= 60,
    # regardless of what the model decided - this protects against the model
    # failing to correctly apply its own stated thresholds.
    if (trust_score <= 50 or risk_score >= 60) and target_rank < SEVERITY["Quarantine"]:
        floor_action = "Quarantine" if orig_rank < SEVERITY["Quarantine"] else suggested_action
        reason_bits = []
        if trust_score <= 50:
            reason_bits.append(f"trust_score {trust_score} <= 50")
        if risk_score >= 60:
            reason_bits.append(f"risk_score {risk_score} >= 60")
        reason_str = " and ".join(reason_bits)
        _log_incident(flow_id, floor_action, "warning",
                       f"Overrode agent's '{target_action}' - {reason_str} requires at least Quarantine")
        return {"final_action": floor_action, "overridden": floor_action != suggested_action, "agent_used": True,
                "tool_called": fn_name,
                "agent_reason": f"Agent proposed '{target_action}' but {reason_str} requires at least Quarantine per policy floor."}

    result = TOOL_IMPL[fn_name](**args)
    result["agent_used"] = True
    result["tool_called"] = fn_name
    return result