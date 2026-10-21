# backend/main.py

import os
import json
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.trust_engine import compute_trust_score
from backend.decision_engine import (
    decide_action,
    simulate_vlan_quarantine,
    get_all_vlan_states,
)
from backend.soc_agent import run_soc_agent
from backend.pipeline import process_flow

from telegram_alert import send_telegram_alert_async
from honeypot_redirect import (
    trigger_honeypot_connection,
    get_honeypot_session,
    get_all_honeypot_sessions,
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(title="TrustFlow NGFW API")


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HONEYPOT
# ============================================================

async def trigger_honeypot_connection_async(
    flow_id,
    source_ip="203.0.113.42",
    target_host="localhost",
    target_port=2222,
):
    loop = asyncio.get_running_loop()

    return await loop.run_in_executor(
        None,
        trigger_honeypot_connection,
        flow_id,
        source_ip,
        target_host,
        target_port,
    )


@app.get("/api/honeypot-session/{flow_id}")
async def honeypot_session(flow_id: str):
    """Returns real-time shell activity and decoy command logs for a quarantined flow."""
    return get_honeypot_session(flow_id)


@app.get("/api/honeypot-sessions")
async def all_honeypot_sessions():
    """Returns all active decoy honeypot sessions."""
    return get_all_honeypot_sessions()


# ============================================================
# VLAN STATUS
# ============================================================

@app.get("/api/vlan-status")
async def vlan_status():
    """Returns all currently simulated VLAN quarantine flags."""
    return get_all_vlan_states()


# ============================================================
# FEDERATED LEARNING STATUS
# ============================================================

@app.get("/api/federated-status")
async def federated_status():
    """Returns the federated learning accuracy log."""

    log_path = "backend/federated/results/accuracy_log.json"

    if not os.path.exists(log_path):
        return []

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


# ============================================================
# RED TEAM STATUS
# ============================================================

@app.get("/api/redteam-status")
async def redteam_status():
    """Returns the red-team evasion results log."""

    log_path = "backend/redteam/results/evasion_results.json"

    if not os.path.exists(log_path):
        return {}

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# ============================================================
# INCIDENT LOGS
# ============================================================

@app.get("/api/incident-logs")
async def incident_logs():
    """Returns all logged autonomous SOC agent decisions and override events."""
    log_path = "data/incident_log.csv"
    if not os.path.exists(log_path):
        return []
    import csv
    records = []
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
        return list(reversed(records))
    except Exception:
        return []


# ============================================================
# REQUEST MODELS
# ============================================================

class TrustRequest(BaseModel):
    mfa_on: bool = True
    device_healthy: bool = True
    known_location: bool = True
    normal_hours: bool = True


class DecisionRequest(BaseModel):
    trust_score: float
    risk_score: float


class AgentReviewRequest(BaseModel):
    flow_id: str
    trust_score: float
    risk_score: float
    suggested_action: str
    explanation: str
    ja3_flagged: bool


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "status": "TrustFlow NGFW backend running"
    }


# ============================================================
# TRUST SCORE
# ============================================================

@app.post("/trust-score")
def trust_score(req: TrustRequest):
    return compute_trust_score(
        req.mfa_on,
        req.device_healthy,
        req.known_location,
        req.normal_hours,
    )


# ============================================================
# DECISION ENGINE
# ============================================================

@app.post("/decide")
def decide(req: DecisionRequest):
    return decide_action(
        req.trust_score,
        req.risk_score,
    )


# ============================================================
# SOC AI AGENT REVIEW
# ============================================================

@app.post("/agent-review")
def agent_review(req: AgentReviewRequest):
    """
    Send a decision-engine result to the SOC AI agent.

    The SOC agent can:
        - confirm_action
        - escalate_action
        - deescalate_action

    The actual agent implementation and incident logging
    are handled by backend.soc_agent.run_soc_agent().
    """

    result = run_soc_agent(
        flow_id=req.flow_id,
        trust_score=req.trust_score,
        risk_score=req.risk_score,
        suggested_action=req.suggested_action,
        explanation=req.explanation,
        ja3_flagged=req.ja3_flagged,
    )

    return {
        "flow_id": req.flow_id,
        "action": result.get("final_action"),
        "overridden": result.get("overridden", False),
        "agent_used": result.get("agent_used", False),
        "tool_called": result.get("tool_called"),
        "agent_reason": result.get("agent_reason"),
    }


# ============================================================
# PIPELINE INFORMATION
# ============================================================

@app.get("/api/pipeline-info")
async def pipeline_info():
    """Returns static description of each sub-model in the ensemble pipeline."""

    return {
        "model_a": "XGBoost supervised classifier (known attack patterns)",
        "model_b": "Isolation Forest (zero-day/anomaly detection, trained on benign-only flows)",
        "model_c": "JA3 TLS fingerprint check against abuse.ch blocklist + logistic regression",
        "meta_learner": "Logistic regression fusing all three sub-scores into final risk score",
    }


# ============================================================
# ACTIVE WEBSOCKET CONNECTIONS
# ============================================================

active_connections = []


# ============================================================
# WEBSOCKET
# ============================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    if websocket not in active_connections:
        active_connections.append(websocket)

    try:

        while True:

            data = await websocket.receive_json()

            result = await process_flow(data)

            # Broadcast result to ALL connected dashboards & clients
            dead_connections = []

            for conn in list(active_connections):

                try:
                    await conn.send_json(result)

                except Exception:
                    dead_connections.append(conn)

            # Remove dead connections
            for dead in dead_connections:

                if dead in active_connections:
                    active_connections.remove(dead)

    except WebSocketDisconnect:

        if websocket in active_connections:
            active_connections.remove(websocket)

    except Exception:

        if websocket in active_connections:
            active_connections.remove(websocket)

