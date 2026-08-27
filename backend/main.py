# backend/main.py

import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from backend.trust_engine import compute_trust_score
from backend.decision_engine import (decide_action,simulate_vlan_quarantine,get_all_vlan_states)
import asyncio
from telegram_alert import send_telegram_alert_async
from honeypot_redirect import trigger_honeypot_connection, get_honeypot_session, get_all_honeypot_sessions

async def trigger_honeypot_connection_async(
    flow_id,
    source_ip="203.0.113.42",
    target_host="localhost",
    target_port=2222
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

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TrustFlow NGFW API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/honeypot-session/{flow_id}")
async def honeypot_session(flow_id: str):
    """Returns real-time shell activity and decoy command logs for a quarantined flow."""
    return get_honeypot_session(flow_id)

@app.get("/api/honeypot-sessions")
async def all_honeypot_sessions():
    """Returns all active decoy honeypot sessions."""
    return get_all_honeypot_sessions()

@app.get("/api/vlan-status")
async def vlan_status():
    """Returns all currently simulated VLAN quarantine flags for the dashboard badge."""
    return get_all_vlan_states()

@app.get("/api/federated-status")
async def federated_status():
    """Returns the contents of the federated learning accuracy log."""
    log_path = "backend/federated/results/accuracy_log.json"
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, "r") as f:
            return json.load(f)
    except Exception:
        return []

@app.get("/api/redteam-status")
async def redteam_status():
    """Returns the contents of the red-team evasion results log."""
    log_path = "backend/redteam/results/evasion_results.json"
    if not os.path.exists(log_path):
        return {}
    try:
        with open(log_path, "r") as f:
            return json.load(f)
    except Exception:
        return {}

class TrustRequest(BaseModel):
    mfa_on: bool = True
    device_healthy: bool = True
    known_location: bool = True
    normal_hours: bool = True

class DecisionRequest(BaseModel):
    trust_score: float
    risk_score: float

@app.get("/")
def root():
    return {"status": "TrustFlow NGFW backend running"}


@app.post("/trust-score")
def trust_score(req: TrustRequest):
    return compute_trust_score(req.mfa_on, req.device_healthy, req.known_location, req.normal_hours)

@app.post("/decide")
def decide(req: DecisionRequest):
    return decide_action(req.trust_score, req.risk_score)

from backend.pipeline import process_flow

@app.get("/api/pipeline-info")
async def pipeline_info():
    """Returns static description of each sub-model in the ensemble pipeline."""
    return {
        "model_a": "XGBoost supervised classifier (known attack patterns)",
        "model_b": "Isolation Forest (zero-day/anomaly detection, trained on benign-only flows)",
        "model_c": "JA3 TLS fingerprint check against abuse.ch blocklist + logistic regression",
        "meta_learner": "Logistic regression fusing all three sub-scores into final risk score"
    }

# Active WebSocket connections tracker for live broadcasting
active_connections = []

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

            for dead in dead_connections:
                if dead in active_connections:
                    active_connections.remove(dead)

    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)
    except Exception:
        if websocket in active_connections:
            active_connections.remove(websocket)