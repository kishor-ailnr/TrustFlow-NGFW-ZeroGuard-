# 🛡️ TrustFlow NGFW (Next-Generation AI Firewall)

> **Zero-Trust Network Architecture powered by a Multi-Model AI Ensemble (XGBoost + Isolation Forest + JA3 TLS Fingerprinting), SHAP Explainability, and Automated Active Defense (iptables, Cowrie Honeypot, & Telegram Alerts).**

---

## 🔍 Architecture in 1 Glance

```
                              [ Incoming Network Flow ]
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
         [ Zero-Trust Engine ]                         [ AI Ensemble Pipeline ]
       • MFA Status (30 pts)                    • Model A: Supervised XGBoost (Known Attacks)
       • Device Health (30 pts)                 • Model B: Isolation Forest (Zero-Day Anomaly)
       • Known Location (25 pts)                • Model C: JA3 / TLS Fingerprint Intelligence
       • Normal Hours (15 pts)                                    │
                  │                                               ▼
                  │                                   [ Meta-Learner (Logistic Reg) ]
                  │                                   • Fused Risk Score (0 - 100)
                  │                                   • TreeSHAP Feature Attribution
                  ▼                                               ▼
        [ Trust Score (0-100) ]                        [ Fused Risk Score (0-100) ]
                  └───────────────────────┬───────────────────────┘
                                          ▼
                             [ 2D Decision Matrix Engine ]
                                          │
         ┌──────────────────┬─────────────┴────────────┬──────────────────┐
         ▼                  ▼                          ▼                  ▼
    ✅ ALLOW           🟡 RATE-LIMIT             🔒 QUARANTINE        🚫 BLOCK
  (Normal Pass)     (Bandwidth Throttle)     • Redirect to Cowrie    • Real iptables
                                               SSH Honeypot (p:2222)   DROP rule
                                             • Simulated VLAN Tag    • Telegram Alert
```

---

## 📋 Prerequisites
* **Python 3.10+** (check: `python --version` or `python3 --version`)
* **Node.js 18+ & npm** (check: `node --version` and `npm --version`)

---

## 🚀 Complete Step-by-Step Setup & Run Guide

Follow these steps in order from top to bottom.

---

### Step 1 — Setup Python Virtual Environment & Dependencies

Open your terminal in the `TrustFlowNGFW` project root directory and run:

**On Windows (PowerShell / CMD):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn websockets pydantic pandas numpy scikit-learn xgboost joblib httpx shap
```
*(If you see an execution policy error on PowerShell, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

**On Linux / Ubuntu / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn websockets pydantic pandas numpy scikit-learn xgboost joblib httpx shap
```

---

### Step 2 — Verify ML Model Artifacts (OPTIONAL)

Pre-trained model artifacts are stored in `models/`:
* `xgb_model.pkl` — Supervised XGBoost multi-class attack classifier (Model A)
* `iso_forest.pkl` — Isolation Forest zero-day anomaly detector (Model B)
* `meta_model.pkl` — Meta-Learner fusing all scores into `fused_risk_score`
* `feature_cols.pkl` — 52 network traffic flow features
* `label_encoder.pkl` — Attack type encoder

*(Optional: If you ever want to re-train the models from scratch, run: `python backend/train_ensemble.py`)*

---

### Step 3 — Start the Backend Server (Terminal 1)

Open **Terminal 1** in the project root and run:

**On Windows:**
```powershell
.\venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

**On Linux / Ubuntu / macOS:**
```bash
source venv/bin/activate
python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

* **Backend Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **WebSocket Endpoint:** `ws://127.0.0.1:8000/ws`

---

### Step 4 — Start the Frontend Dashboard (Terminal 2)

Open a **new Terminal 2** and run:

```bash
cd frontend
npm install
npm run dev
```

* **Open the Dashboard in your browser:** **[http://localhost:5173/](http://localhost:5173/)**
* The top bar status will show **`● WS Connected`** in green.

---

### Step 5 — Start Live Traffic Streamer (Terminal 3)

Open a **new Terminal 3** in the project root and run:

**On Windows:**
```powershell
.\venv\Scripts\python.exe demo_live_stream.py
```

**On Linux / Ubuntu / macOS:**
```bash
python3 demo_live_stream.py
```

As soon as this script runs, network flows will start **streaming live into your browser dashboard in real time**!

---

## 🏆 What to Show the Judges During the Demo

Follow this 5-point presentation flow on your dashboard:

1. **⚡ Live Flow Feed (Left Panel):**
   * Show traffic classified in real time into **Allow**, **Rate-limit**, **Quarantine**, and **Block**.
2. **🧠 Signature Circular Risk Gauge & Ensemble Breakdown:**
   * Click any row to show how the **XGBoost (Supervised)**, **Isolation Forest (Anomaly)**, and **JA3 (TLS Intel)** sub-models score the flow simultaneously.
3. **🔍 SHAP Explainability:**
   * Point to the **Top SHAP features** box showing the exact packet metrics (e.g., packet length, flow packets/s) that triggered the AI decision.
4. **🛡️ Zero-Trust Interactive Toggles (Live What-If Simulation):**
   * Flip the **MFA** or **Device Health** switches in the Trust Panel, then click **`↺ Re-send with new trust signals`**.
   * Show the judges how changing trust signals alters the firewall's decision in real-time.
5. **⚔️ Automated Mitigations:**
   * Point out the **iptables DROP rule applied** status on Block flows, the **Cowrie SSH Honeypot (port 2222)** redirection with VLAN badges on Quarantine flows, and the **Telegram SOC notification** note.

---

## 🧪 Quick Test Commands (Run in Terminal 3 on Demand)

| Goal | Command | Expected Result |
|---|---|---|
| **Test Quarantine Flow** | `python test_quarantine_confirmed.py` | Risk: 88.8, Trust: 60 → **Quarantine** (Redirected to Cowrie) |
| **Test High-Risk Attack** | `python test_high_risk_flow.py` | Risk: 100.0 → **Block** (iptables DROP rule applied) |
| **Run Federated Demo** | `python backend/federated/run_federated_demo.py` | Simulates multi-bank federated model aggregation |
| **Run Red-Team Evasion**| `python backend/redteam/run_redteam_test.py` | Tests adversarial traffic perturbations |

---

## 📁 Project Directory Structure

```
TrustFlowNGFW/
├── backend/                        # FastAPI Backend & AI Pipeline
│   ├── main.py                     # WebSocket /ws endpoint + REST APIs + CORS
│   ├── pipeline.py                 # Core AI inference pipeline orchestration
│   ├── decision_engine.py          # 2D Trust-Risk Decision Matrix
│   ├── trust_engine.py             # Zero-Trust Posture Score Calculator
│   ├── explain.py                  # TreeSHAP explainability engine
│   ├── train_ensemble.py           # Model training script
│   ├── federated/                  # Federated Learning client/server scripts
│   └── redteam/                    # Adversarial perturbation & evasion scripts
├── frontend/                       # Vite + React SOC Dashboard
│   ├── src/
│   │   ├── App.jsx                 # Main layout & state wiring
│   │   ├── index.css               # Frosted white glassmorphism design system
│   │   ├── hooks/                  # useWebSocket & usePolling hooks
│   │   └── components/
│   │       ├── FlowFeed.jsx        # Live scrolling flow list
│   │       ├── EnsemblePanel.jsx   # Model A/B/C breakdown
│   │       ├── RiskGauge.jsx       # Signature SVG circular ring gauge
│   │       ├── TrustPanel.jsx      # Neumorphic posture toggles + re-send
│   │       ├── MitigationPanel.jsx # iptables, Cowrie honeypot & Telegram status
│   │       ├── FederatedPanel.jsx  # Recharts federated accuracy curve
│   │       └── RedTeamPanel.jsx    # Adversarial robustness table
├── data/                           # Evaluation & holdout datasets
│   └── replay_holdout.csv          # 45,000 holdout flows (CICIDS2017)
├── models/                         # Pre-trained ML weights (.pkl artifacts)
├── demo_live_stream.py             # Continuous live traffic streaming demo script
├── test_quarantine_confirmed.py    # Deterministic Quarantine verification test
├── test_high_risk_flow.py          # High-Risk Block verification test
└── README.md                       # Complete project documentation
```

---

## 🛠️ Troubleshooting & FAQs

### 1. `WS Disconnected` in Dashboard Top Bar
* **Cause:** The backend server is not running.
* **Fix:** In Terminal 1, run `python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`.

### 2. PowerShell Script Execution Policy Error (Windows)
* **Error:** `cannot be loaded because running scripts is disabled on this system.`
* **Fix:** Run this once in PowerShell:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```

### 3. Port 8000 or 5173 Already in Use
* **Fix (Windows):**
  ```powershell
  Get-Process python, node -ErrorAction SilentlyContinue | Stop-Process
  ```
* **Fix (Linux/macOS):**
  ```bash
  kill -9 $(lsof -t -i:8000 -i:5173)
  ```

---

*TrustFlow NGFW — Next-Generation AI Defense Architecture.*
