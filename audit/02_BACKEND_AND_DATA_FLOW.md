# 02 - Backend Architecture and Data Flow

---

## 1. REST API Route Directory

All routes are served by the FastAPI application defined in [`backend/main.py`](file:///c:/Music/TrustFlowNGFW/backend/main.py).

| Method | Path | Request Body | Response Shape | Handler Function | Purpose |
|---|---|---|---|---|---|
| `GET` | `/` | None | `{"status": "TrustFlow NGFW backend running"}` | `root()` ([main.py:183](file:///c:/Music/TrustFlowNGFW/backend/main.py#L183)) | Health check / backend liveness check |
| `POST` | `/trust-score` | `{"mfa_on": bool, "device_healthy": bool, "known_location": bool, "normal_hours": bool}` | `{"trust_score": int, "trust_level": str, "signals": dict, "reasons": list}` | `trust_score(req: TrustRequest)` ([main.py:194](file:///c:/Music/TrustFlowNGFW/backend/main.py#L194)) | Standalone endpoint to compute 0-100 zero-trust score |
| `POST` | `/decide` | `{"trust_score": float, "risk_score": float}` | `{"action": str, "trust_band": str, "risk_band": str, "override_applied": bool, "reason": str}` | `decide(req: DecisionRequest)` ([main.py:208](file:///c:/Music/TrustFlowNGFW/backend/main.py#L208)) | Evaluates 2D decision matrix without running full ML pipeline |
| `POST` | `/agent-review` | `{"flow_id": str, "trust_score": float, "risk_score": float, "suggested_action": str, "explanation": str, "ja3_flagged": bool}` | `{"flow_id": str, "action": str, "overridden": bool, "agent_used": bool, "tool_called": str, "agent_reason": str}` | `agent_review(req: AgentReviewRequest)` ([main.py:220](file:///c:/Music/TrustFlowNGFW/backend/main.py#L220)) | Explicit trigger of Ollama SOC Agent review |
| `GET` | `/api/pipeline-info` | None | `{"model_a": str, "model_b": str, "model_c": str, "meta_learner": str}` | `pipeline_info()` ([main.py:257](file:///c:/Music/TrustFlowNGFW/backend/main.py#L257)) | Static architectural description of the 3 sub-models |
| `GET` | `/api/honeypot-session/{flow_id}` | None (path parameter `flow_id`) | Session dictionary: `session_id`, `flow_id`, `source_ip`, `decoy_host`, `auth`, `commands`, `keystrokes_captured`, etc. | `honeypot_session(flow_id: str)` ([main.py:70](file:///c:/Music/TrustFlowNGFW/backend/main.py#L70)) | Returns live/synthesized Cowrie decoy shell telemetry |
| `GET` | `/api/honeypot-sessions` | None | Array of all active decoy honeypot session dictionaries | `all_honeypot_sessions()` ([main.py:76](file:///c:/Music/TrustFlowNGFW/backend/main.py#L76)) | Lists all recorded decoy sessions across quarantined flows |
| `GET` | `/api/vlan-status` | None | Dictionary mapping `flow_id` to `{"source_ip": str, "vlan_status": str, "simulated": bool, "timestamp": str}` | `vlan_status()` ([main.py:86](file:///c:/Music/TrustFlowNGFW/backend/main.py#L86)) | Returns in-memory simulated VLAN quarantine states |
| `GET` | `/api/federated-status` | None | Array of accuracy logs from `backend/federated/results/accuracy_log.json` | `federated_status()` ([main.py:96](file:///c:/Music/TrustFlowNGFW/backend/main.py#L96)) | Returns federated learning accuracy logs per training round |
| `GET` | `/api/redteam-status` | None | Object from `backend/redteam/results/evasion_results.json`: `total_tested`, `still_detected`, `evaded`, `per_flow` | `redteam_status()` ([main.py:116](file:///c:/Music/TrustFlowNGFW/backend/main.py#L116)) | Returns adversarial evasion benchmark results |
| `GET` | `/api/incident-logs` | None | Reverse-chronological array of CSV dictionaries from `data/incident_log.csv` | `incident_logs()` ([main.py:136](file:///c:/Music/TrustFlowNGFW/backend/main.py#L136)) | Returns immutable ledger of SOC agent decisions and overrides |

---

## 2. WebSocket Endpoints & Message Specifications

### Endpoint: `ws://127.0.0.1:8000/ws` ([backend/main.py:280](file:///c:/Music/TrustFlowNGFW/backend/main.py#L280))

The WebSocket connection handles bidirectional real-time packet flow ingestion and decision broadcasting.

#### 1. Incoming Client Message Payload (Flow Ingestion)
Sent by `demo_live_stream.py` or re-sent by frontend `TrustPanel.jsx`.
Contains identity flags, JA3 risk, and the 52 numerical CIC-IDS features:

```json
{
  "flow_id": "DEMO-DOS-001",
  "source_ip": "203.0.113.88",
  "mfa_on": true,
  "device_healthy": false,
  "known_location": true,
  "normal_hours": true,
  "ja3_risk": 0.8,
  "Destination Port": 80.0,
  "Flow Duration": 12450.0,
  "Total Fwd Packets": 45.0,
  "Total Length of Fwd Packets": 2840.0,
  "Fwd Packet Length Max": 850.0,
  "Fwd Packet Length Min": 0.0,
  "Fwd Packet Length Mean": 63.1,
  "Fwd Packet Length Std": 128.4,
  "Bwd Packet Length Max": 0.0,
  "Bwd Packet Length Min": 0.0,
  "Bwd Packet Length Mean": 0.0,
  "Bwd Packet Length Std": 0.0,
  "Flow Bytes/s": 228112.4,
  "Flow Packets/s": 3614.4,
  "Flow IAT Mean": 282.9,
  "Flow IAT Std": 412.0,
  "Flow IAT Max": 2100.0,
  "Flow IAT Min": 4.0,
  "Fwd IAT Total": 12450.0,
  "Fwd IAT Mean": 282.9,
  "Fwd IAT Std": 412.0,
  "Fwd IAT Max": 2100.0,
  "Fwd IAT Min": 4.0,
  "Bwd IAT Total": 0.0,
  "Bwd IAT Mean": 0.0,
  "Bwd IAT Std": 0.0,
  "Bwd IAT Max": 0.0,
  "Bwd IAT Min": 0.0,
  "Fwd Header Length": 920.0,
  "Bwd Header Length": 0.0,
  "Fwd Packets/s": 3614.4,
  "Bwd Packets/s": 0.0,
  "Min Packet Length": 0.0,
  "Max Packet Length": 850.0,
  "Packet Length Mean": 61.7,
  "Packet Length Std": 125.9,
  "Packet Length Variance": 15850.8,
  "FIN Flag Count": 0.0,
  "PSH Flag Count": 1.0,
  "ACK Flag Count": 0.0,
  "Average Packet Size": 63.1,
  "Subflow Fwd Bytes": 2840.0,
  "Init_Win_bytes_forward": 29200.0,
  "Init_Win_bytes_backward": -1.0,
  "act_data_pkt_fwd": 12.0,
  "min_seg_size_forward": 20.0,
  "Active Mean": 0.0,
  "Active Max": 0.0,
  "Active Min": 0.0,
  "Idle Mean": 0.0,
  "Idle Max": 0.0,
  "Idle Min": 0.0
}
```

#### 2. Outgoing Broadcast Message Payload (Evaluated Verdict)
Broadcast to all connected clients (`conn.send_json(result)`) upon completion of `process_flow(data)`:

```json
{
  "flow_id": "DEMO-DOS-001",
  "source_ip": "203.0.113.88",
  "model_a_score": 0.9842,
  "model_b_score": 0.8125,
  "model_c_score": 0.8000,
  "fused_risk_score": 94.67,
  "shap_attribution": {
    "primary_model": "AI classifier",
    "top_features": "Flow Packets/s, Total Fwd Packets",
    "contributions": {
      "model_a_xgboost": 2.451,
      "model_b_isolation_forest": 1.284,
      "model_c_ja3": 1.102
    }
  },
  "explanation": "Blocked: classifier identified a high-confidence attack pattern in Flow Packets/s, Total Fwd Packets",
  "trust_score": 70.0,
  "trust_band": "Medium",
  "action": "Block",
  "reason": "Very high risk (95) triggers an immediate block regardless of trust",
  "agent_review": null,
  "honeypot_verdict": null
}
```

---

## 3. Complete End-to-End Decision Pipeline

When a flow packet arrives on `ws://127.0.0.1:8000/ws`:

```
1. [Client / demo_live_stream.py]
   └─ Sends JSON over WebSocket -> backend/main.py:websocket_endpoint()

2. [backend/main.py: websocket_endpoint]
   └─ Calls process_flow(flow_data) in backend/pipeline.py

3. [backend/pipeline.py: process_flow]
   ├─ Step 3A: Sub-Model Inference
   │  ├─ Model A: xgb_model.predict_proba(df_row) -> xgb_risk = 1 - proba(Normal Traffic)
   │  ├─ Model B: iso_forest.score_samples(df_row) -> iso_risk = min-max calibrated
   │  └─ Model C: ja3_risk extracted from flow_data
   │
   ├─ Step 3B: Meta-Learner Probability Fusion
   │  └─ meta_model.predict_proba([[xgb_risk, iso_risk, ja3_risk]])[:, 1] * 100 -> fused_risk_score
   │
   ├─ Step 3C: TreeSHAP Feature Attribution
   │  └─ explainer.shap_values(df_row) -> top 2 features & submodel contribution weights
   │
   ├─ Step 3D: Zero-Trust Continuous Posture Calculation
   │  └─ backend/trust_engine.py: compute_trust_score(mfa, healthy, location, hours) -> trust_score (0-100)
   │
   ├─ Step 3E: 2D Matrix Decision Engine
   │  └─ backend/decision_engine.py: decide_action(trust_score, fused_risk_score) -> action, reason
   │
   ├─ Step 3F: Borderline Agentic SOC Review (Ollama LLM)
   │  └─ If action in ("Rate-limit", "Quarantine"):
   │     Calls backend/soc_agent.py: run_soc_agent(...)
   │     -> May confirm, escalate, or de-escalate subject to policy guardrails
   │
   ├─ Step 3G: Active Defense Dispatch
   │  ├─ If action == "Quarantine":
   │  │  ├─ asyncio.create_task(trigger_honeypot_connection_async(flow_id, source_ip))
   │  │  ├─ simulate_vlan_quarantine(flow_id, source_ip)
   │  │  └─ honeypot_verdict = watch_honeypot_and_judge(flow_id, source_ip, timeout_seconds=4)
   │  │     (Note: Overrides action if verdict is Block or Allow!)
   │  ├─ If action == "Block":
   │  │  └─ iptables_action.py: block_ip(source_ip) -> netsh advfirewall rule added
   │  └─ If action in ("Block", "Quarantine"):
   │     └─ asyncio.create_task(send_telegram_alert_async(...))
   │
   └─ Step 3H: Return Evaluated Object to websocket_endpoint()

4. [backend/main.py: websocket_endpoint]
   └─ Broadcasts evaluated JSON result to ALL connected browser dashboards
```

---

## 4. Function & Class Catalog by Backend File

### `backend/main.py`
* **`trigger_honeypot_connection_async(flow_id, source_ip, target_host, target_port)`**: Runs synchronous socket connection in threadpool executor via `loop.run_in_executor`. Returns bool.
* **`honeypot_session(flow_id)`**: Route handler returning recorded/synthesized decoy session telemetry.
* **`all_honeypot_sessions()`**: Route handler returning all recorded honeypot sessions.
* **`vlan_status()`**: Route handler returning `vlan_quarantine_state` dictionary.
* **`federated_status()`**: Route handler reading `accuracy_log.json`. Returns list of round accuracies.
* **`redteam_status()`**: Route handler reading `evasion_results.json`. Returns red-team metrics.
* **`incident_logs()`**: Route handler reading `data/incident_log.csv` and returning reversed list of dicts.
* **`root()`**: Route handler returning static health status.
* **`trust_score(req)`**: Route handler invoking `compute_trust_score`.
* **`decide(req)`**: Route handler invoking `decide_action`.
* **`agent_review(req)`**: Route handler invoking `run_soc_agent`.
* **`pipeline_info()`**: Route handler returning model descriptions.
* **`websocket_endpoint(websocket)`**: Manages WebSocket lifecycle, receives flow data, coordinates `process_flow`, and broadcasts results.

### `backend/pipeline.py`
* **`trigger_honeypot_connection_async(flow_id, source_ip, target_host, target_port)`**: Non-blocking wrapper dispatching `trigger_honeypot_connection` to event loop executor.
* **`process_flow(flow_data: dict) -> dict`**: Master pipeline function. Converts 52 features to DataFrame, runs XGBoost, Isolation Forest, Meta-learner, SHAP attribution, trust engine, decision matrix, SOC agent, honeypot redirect/watcher, netsh block, and Telegram alerting.

### `backend/decision_engine.py`
* **`trust_band(score: float) -> str`**: Maps score to `"High"` (>=80), `"Medium"` (>=50), or `"Low"` (<50).
* **`risk_band(score: float) -> str`**: Maps score to `"Low"` (<30), `"Medium"` (<70), or `"High"` (>=70).
* **`decide_action(trust_score, risk_score, source_ip) -> dict`**: If `risk_score >= 90`, overrides to `"Block"`. Otherwise looks up `(trust_band, risk_band)` in `DECISION_MATRIX`.
* **`simulate_vlan_quarantine(flow_id, source_ip)`**: Records quarantined host into in-memory `vlan_quarantine_state` dict with `"simulated": True`.
* **`get_vlan_state(flow_id)`**: Returns single flow VLAN entry.
* **`get_all_vlan_states()`**: Returns complete `vlan_quarantine_state` dictionary.

### `backend/trust_engine.py`
* **`compute_trust_score(mfa_on, device_healthy, known_location, normal_hours) -> dict`**: Computes weighted sum: MFA (+30), Device Health (+30), Known Location (+25), Normal Hours (+15). Returns score (0–100), trust level, and diagnostic reasons.

### `backend/soc_agent.py`
* **`_log_incident(flow_id, action, severity, message)`**: Appends a timestamped audit row to `data/incident_log.csv`.
* **`tool_confirm_action(flow_id, action, reason)`**: Tool implementation confirming suggested action. Logs incident.
* **`tool_escalate_action(flow_id, new_action, reason)`**: Tool implementation escalating action severity. Logs incident.
* **`tool_deescalate_action(flow_id, new_action, reason)`**: Tool implementation reducing action severity. Logs incident.
* **`run_soc_agent(flow_id, trust_score, risk_score, suggested_action, explanation, ja3_flagged, model="llama3.2") -> dict`**: Formulates structured prompt, calls `ollama.chat` with tools schema, enforces direction guardrails, single-step de-escalation cap, and zero-trust floor (`risk >= 60` or `trust <= 50`).

### `backend/explain.py`
* Standalone script: Computes raw TreeSHAP values for XGBoost on `replay_enriched.csv`, calculates meta-model feature contributions, constructs human-readable explanations, and outputs `data/replay_final.csv`.

### `backend/fix_explanations.py`
* Standalone script: Sanitizes explanation strings in `data/replay_final.csv` so allowed flows do not display alarming "risk driver" text.

### `backend/train_ensemble.py`
* Standalone script: Trains Isolation Forest on benign rows of `replay_holdout.csv`, fetches/simulates JA3 hashes, fits LogisticRegression meta-learner, and dumps model pickles.

### `backend/train_model.py`
* Standalone script: Ingests CIC-IDS2017 CSVs, cleans headers and infinite values, downsamples, trains multiclass XGBClassifier, and outputs `models/xgb_model.pkl` and `data/replay_holdout.csv`.

### `backend/federated/server.py`
* **`weighted_average(metrics)`**: Aggregates client evaluation accuracies weighted by example count.
* **`LoggingStrategy(fl.server.strategy.FedAvg)`**: Custom Flower strategy writing round accuracy logs to `backend/federated/results/accuracy_log.json`.
* **`main()`**: Starts Flower server on port 8080 for 3 rounds.

### `backend/federated/client.py`
* **`FlowerClient(fl.client.NumPyClient)`**: Flower client class handling local model weight updates (`fit`) and validation metrics (`evaluate`).

### `backend/federated/data_split.py`
* Standalone script: Splits CIC-IDS2017 into non-IID partitions `client_0.csv` and `client_1.csv`.

### `backend/redteam/perturb.py`
* **`apply_evasion_perturbation(row) -> pd.Series`**: Applies synthetic feature perturbation (simulating FGSM / packet padding) by shifting Flow Duration, Packet Lengths, and IAT statistics.

### `backend/redteam/select_flows.py`
* Standalone script: Extracts 4 robust and 4 evadable flow indices from CIC-IDS2017 to `backend/redteam/data/malicious_sample.csv`.

### `backend/redteam/run_redteam_test.py`
* Standalone script: Iterates over selected flows, calculates baseline vs perturbed risk scores, evaluates decision engine verdicts, and outputs `evasion_results.json`.

---

## 5. Machine Learning Ensemble & Decision Engine Logic

### Sub-Model Scoring
1. **Model A (XGBoost Multiclass)**:
   * Features: 52 numeric network packet features.
   * Target: Multiclass attack categories (`Normal Traffic`, `DoS`, `Port Scanning`, `Brute Force`, `Bots`, etc.).
   * Score: $xgb\_risk = 1.0 - P(\text{Normal Traffic})$. Output range $[0.0, 1.0]$.
2. **Model B (Isolation Forest)**:
   * Trained exclusively on benign network flows ($n=150$ estimators, contamination=0.05).
   * Raw anomaly score: $s = -\text{score\_samples}(X)$.
   * Calibration: Min-max scaled against replay baseline limits ($min=0.31877, max=0.75165$):
     $$iso\_risk = \text{clip}\left(\frac{s - iso\_min}{iso\_max - iso\_min}, 0.0, 1.0\right)$$
3. **Model C (JA3 TLS Client Fingerprint Intelligence)**:
   * Binary threat indicator: matches known-malicious MD5 hashes (from abuse.ch blocklist).
   * Score: $ja3\_risk \in \{0.0, 1.0\}$. $ja3\_flagged = (ja3\_risk \ge 1.0)$.

### Meta-Learner Probability Fusion
* Algorithm: Logistic Regression with balanced class weights (`models/meta_model.pkl`).
* Input vector: $[xgb\_risk, iso\_risk, ja3\_risk]$.
* Output: Calibrated probability of attack scaled to 0–100:
  $$fused\_risk\_score = P(Y = 1 \mid xgb, iso, ja3) \times 100$$
* Attribution: Meta-learner coefficients ($\beta_1 \cdot xgb, \beta_2 \cdot iso, \beta_3 \cdot ja3$) identify the primary model driver.

### Zero-Trust Posture Scoring
* Identity & Endpoint attributes evaluated by `backend/trust_engine.py`:
  * **MFA Enabled**: +30 points
  * **Device Healthy / Compliant**: +30 points
  * **Known Corporate Location**: +25 points
  * **Normal Business Hours**: +15 points
* Output: Integer score from 0 to 100.
* Band Mapping:
  * $\ge 80$: **High Trust**
  * $50 - 79$: **Medium Trust**
  * $< 50$: **Low Trust**

### 2D Decision Matrix Engine

The decision engine combines Trust Band and Risk Band ($Low < 30$, $Medium \in [30, 69]$, $High \ge 70$):

| Trust Band \ Risk Band | Low Risk (<30) | Medium Risk (30–69) | High Risk (70–89) | Critical Risk ($\ge 90$) |
|---|---|---|---|---|
| **High Trust ($\ge 80$)** | Allow | Allow | Rate-limit | **Block (Hard Override)** |
| **Medium Trust (50–79)** | Allow | Rate-limit | Quarantine | **Block (Hard Override)** |
| **Low Trust (<50)** | Rate-limit | Quarantine | Block | **Block (Hard Override)** |

* **Hard Override Rule**: If $fused\_risk\_score \ge 90$, the verdict is immediately **Block**, ignoring trust posture.

---

## 6. Autonomous SOC Agent (Ollama LLM)

### Trigger Conditions
The agent is invoked dynamically within `backend/pipeline.py` ([line 130](file:///c:/Music/TrustFlowNGFW/backend/pipeline.py#L130)) **only** when the initial decision matrix action is a borderline verdict:
$$\text{action} \in \{\text{"Rate-limit"}, \text{"Quarantine"}\}$$
Clean Allow flows and unambiguous Block flows ($\ge 90$ risk or Low Trust + High Risk) bypass the LLM to preserve low latency.

### Available Tools
The agent is presented with three JSON schema function tools:
1. `confirm_action(flow_id, action, reason)`: Confirms the deterministic action.
2. `escalate_action(flow_id, new_action, reason)`: Upgrades to a more severe action (`Rate-limit` -> `Quarantine` -> `Block`).
3. `deescalate_action(flow_id, new_action, reason)`: Downgrades to a less severe action (`Quarantine` -> `Rate-limit` -> `Allow`).

### Guardrails & Policy Enforcement Floors
The backend implements three strict procedural guardrails in Python around the agent's output:
1. **Semantic Direction Integrity** ([soc_agent.py:152-162](file:///c:/Music/TrustFlowNGFW/backend/soc_agent.py#L152)): Discards any tool call where the target severity rank contradicts the tool name (e.g., calling `escalate_action` with target `"Allow"`).
2. **Single-Step De-escalation Cap** ([soc_agent.py:169-178](file:///c:/Music/TrustFlowNGFW/backend/soc_agent.py#L169)): The agent is prohibited from dropping more than one severity rank in a single call (e.g. `Quarantine` cannot be dropped straight to `Allow`; it is capped at `Rate-limit`).
3. **Zero-Trust Hard Floor** ([soc_agent.py:183-196](file:///c:/Music/TrustFlowNGFW/backend/soc_agent.py#L183)): If $trust\_score \le 50$ OR $risk\_score \ge 60$, the action is forbidden from landing below `Quarantine`. If the LLM proposes `Allow` or `Rate-limit`, Python overrides the agent and enforces `Quarantine`.

---

## 7. Active Defense Execution: Real vs. Simulated

| Defense Vector | Implementation File | Execution Mechanism | Real vs. Simulated | Operational Notes |
|---|---|---|---|---|
| **Windows Firewall** | [`iptables_action.py`](file:///c:/Music/TrustFlowNGFW/iptables_action.py) | Executes `netsh advfirewall firewall add rule name=TrustFlowNGFW_Block_<ip> dir=in action=block remoteip=<ip>` via `subprocess.run` | **REAL** | True kernel packet drop on Windows. Fails silently if process lacks Administrator rights. (File name `iptables_action.py` is a Linux misnomer). |
| **Cowrie Honeypot Socket** | [`honeypot_redirect.py`](file:///c:/Music/TrustFlowNGFW/honeypot_redirect.py) | Attempts real TCP connection to `localhost:2222` with dummy SSH string | **REAL** (Conditional) | Connects to Docker container on port 2222 if container is running. |
| **Decoy Shell Telemetry** | [`honeypot_redirect.py`](file:///c:/Music/TrustFlowNGFW/honeypot_redirect.py) | Synthesizes command stream (`whoami`, `cat /etc/passwd`, `wget`) from hardcoded scenario templates | **SIMULATED** | Pre-scripted attacker commands displayed in frontend terminal. |
| **VLAN Port Quarantine** | [`backend/decision_engine.py`](file:///c:/Music/TrustFlowNGFW/backend/decision_engine.py) | Sets in-memory dictionary entry `vlan_quarantine_state[flow_id] = {"simulated": True}` | **SIMULATED** | No physical or virtual switch (802.1Q) port reconfiguration occurs. |
| **Honeypot Watcher** | [`honeypot_redirect.py`](file:///c:/Music/TrustFlowNGFW/honeypot_redirect.py) | Copies and parses `cowrie.json` via `docker cp` for 4 seconds | **REAL / HYBRID** | If container inactive, treats 0 events as "clean" and de-escalates to `Allow`. |
| **Telegram Notifications** | [`telegram_alert.py`](file:///c:/Music/TrustFlowNGFW/telegram_alert.py) | HTTP POST to `https://api.telegram.org/bot<TOKEN>/sendMessage` via `httpx.AsyncClient` | **REAL** | Dispatches genuine push notification messages for Block and Quarantine actions. |

---

## 8. Incident Audit Ledger (`data/incident_log.csv`)

### Schema & Headers
The CSV file records all autonomous governance events. The current code writes 5 columns:
1. `timestamp`: ISO-8601 UTC timestamp (`datetime.now().isoformat()`).
2. `flow_id`: Target network flow identifier string.
3. `action`: Enforced security action (`Allow`, `Rate-limit`, `Quarantine`, `Block`).
4. `severity`: Logging level (`info`, `warning`).
5. `message`: Detailed diagnostic explaining whether the agent confirmed, escalated, de-escalated, or was overridden by guardrail policy.

*(Note: Legacy historical rows in the file prior to the UI redesign contained 4 columns: `timestamp,flow_id,action,reasoning`.)*

### Write Triggers
`data/incident_log.csv` is written synchronously by `_log_incident()` in [`backend/soc_agent.py`](file:///c:/Music/TrustFlowNGFW/backend/soc_agent.py):
1. When `tool_confirm_action` executes.
2. When `tool_escalate_action` executes.
3. When `tool_deescalate_action` executes.
4. When an inconsistent escalate or de-escalate tool call is discarded.
5. When a multi-step de-escalation is capped.
6. When the Zero-Trust policy floor overrides the agent's decision.
7. In [`honeypot_redirect.py:188`](file:///c:/Music/TrustFlowNGFW/honeypot_redirect.py#L188) when `watch_honeypot_and_judge` logs a follow-up honeypot verdict.
