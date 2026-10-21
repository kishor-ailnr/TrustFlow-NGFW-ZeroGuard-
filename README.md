# 🛡️ TrustFlow NGFW (Next-Generation AI Firewall)

> **Zero-Trust Network Architecture powered by a Multi-Model AI Ensemble (XGBoost + Isolation Forest + JA3 TLS Fingerprinting), Agentic SOC Review (Ollama LLM), SHAP Explainability, and Automated Active Defense (Windows Firewall netsh rules, Cowrie Honeypot, & Telegram Alerts).**

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
                                          ▼
                             [ Agentic SOC Review (Ollama) ]
                               (Borderline / Zero-Trust Rules)
                                          │
         ┌──────────────────┬─────────────┴────────────┬──────────────────┐
         ▼                  ▼                          ▼                  ▼
    ✅ ALLOW           🟡 RATE-LIMIT             🔒 QUARANTINE        🚫 BLOCK
  (Normal Pass)     (Bandwidth Throttle)     • Redirect to Cowrie    • Windows Firewall
                                               SSH Honeypot (p:2222)   (netsh advfirewall)
                                             • Simulated VLAN Tag    • Telegram Alert
```

---

## 📋 Prerequisites (Windows)
* **Windows 10 / 11** with PowerShell
* **Python 3.10+** (verify with `python --version`)
* **Node.js 18+ & npm** (verify with `node --version` and `npm --version`)
* **Docker Desktop** (for Cowrie honeypot container on port 2222)
* **Ollama** running locally with `llama3.2` model (`ollama run llama3.2`)

---

## 🚀 Step-by-Step Setup & Run Guide (Windows)

Follow these steps in order to start and run the entire platform.

---

### Step 1 — Open Elevated Terminal (Admin Rights)

For real Windows Firewall rule enforcement, the backend should run with Administrator privileges:

1. Double-click `launch_admin.bat` in the project root to open an elevated PowerShell window inside the project directory.
2. (Or open PowerShell as Administrator and run: `cd C:\Music\TrustFlowNGFW`).

---

### Step 2 — Environment Setup & Health Checks

In your elevated PowerShell terminal:

```powershell
# 1. Enable script execution (if needed)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. (Optional) Stop extra heavy containers to free CPU/RAM for Ollama & inference
.\stop_extra_containers.ps1

# 4. Verify Cowrie honeypot status (should report OK on port 2222)
.\check_cowrie.ps1
```

---

### Step 3 — Start the FastAPI Backend (Terminal 1)

In your elevated PowerShell terminal (Terminal 1), run:

```powershell
.\venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

* **Backend Swagger API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **WebSocket Stream Endpoint:** `ws://127.0.0.1:8000/ws`

---

### Step 4 — Start the Frontend Dashboard (Terminal 2)

Open a **new PowerShell Terminal 2** and run:

```powershell
cd C:\Music\TrustFlowNGFW\frontend
npm install
npm run dev
```

* **Open the Dashboard in your Browser:** 👉 **[http://localhost:5173/](http://localhost:5173/)**
* Check the status indicator in the top-right header: it should show **`● WS Connected`** in green.

---

### Step 5 — Start Live Traffic Streamer (Terminal 3)

Open a **new PowerShell Terminal 3** in the project root and run:

```powershell
cd C:\Music\TrustFlowNGFW
.\venv\Scripts\python.exe demo_live_stream.py
```

As soon as this script runs, network flows will immediately start streaming live into your browser dashboard in real time!

---

## 🏆 Judge Presentation & Live Demonstration Walkthrough

When presenting to judges, open **[http://localhost:5173/](http://localhost:5173/)** in your browser and use the **Sidebar Console** to navigate across the 4 key views:

### 1. ⚡ Live SOC Dashboard (`/`)
* **Live Network Flow Feed:** Real-time stream of incoming network flows dynamically categorized into **Allow**, **Rate-limit**, **Quarantine**, and **Block**.
* **Circular Risk Gauge & Ensemble Breakdown:** Sub-model scoring across **XGBoost** (Known Attacks), **Isolation Forest** (Zero-Day Anomaly), and **JA3 TLS Threat Intel**, fused by the Meta-Learner.
* **TreeSHAP Explainability:** Transparent packet feature attribution.
* **Continuous Zero-Trust "What-If" Simulation:** Toggle MFA, Device Health, or Known Location and click **`↺ Re-send with new trust signals`** to watch the firewall decision adapt in real time.
* **Active Defense Status:** Real Windows Firewall kernel blocks, Cowrie SSH Honeypot (port 2222) redirection, and Telegram alerts.

### 2. 🎯 Adversarial Tests (Red-Team Arena)
* Navigate to the **Adversarial Tests** tab in the sidebar.
* Showcase model resilience against adversarial perturbation vectors (FGSM gradient shifts, timing jitter noise, and payload padding).
* Point out the live adversarial flow table and the **90%+ Robustness Defense Score**.

### 3. 📜 Incident Audit Trail (`Incidents`)
* Open the **Incident Audit Trail** tab in the sidebar.
* Show the immutable log of autonomous **Llama-3.2 SOC Agent** decisions, tool calls (`confirm_action`, `escalate_action`, `deescalate_action`), and zero-trust floor guardrail overrides.
* Inspect quarantined host switch-port isolation states (simulated VLANs).

### 4. 📄 Reports & PDF Compliance Export (`Reports`)
* Open the **Reports & Export** tab in the sidebar.
* Demonstrate the **Daily & Monthly Report Generator**: select any target audit date or month.
* View the live executive summary, risk distribution charts, and MITRE threat breakdowns.
* Click **`Download Certified PDF Report`** to generate a formal, print-ready PDF audit document for regulatory compliance.

---

## 🧪 Quick Test & Validation Scripts

Run any of these in PowerShell to demonstrate specific subsystem capabilities on demand:

| Goal | Command | What It Proves |
|---|---|---|
| **Full Pipeline Test** | `.\venv\Scripts\python.exe -m backend.test_pipeline` | Exercises Allow, Low-Trust Agent override, Quarantine honeypot routing, and Block firewall enforcement. |
| **Check Honeypot** | `.\check_cowrie.ps1` | Validates Cowrie SSH honeypot listener on port 2222. |
| **Stop Extra Docker Load** | `.\stop_extra_containers.ps1` | Stops non-essential containers to free RAM/CPU for Ollama inference. |
| **Red-Team Evasion Test** | `.\venv\Scripts\python.exe backend/redteam/run_redteam_test.py` | Tests model robustness against adversarial network flow perturbations. |

---

## 📁 Project Directory Structure

```
TrustFlowNGFW/
├── backend/                        # FastAPI Backend & AI Pipeline
│   ├── main.py                     # WebSocket /ws endpoint + REST APIs + CORS
│   ├── pipeline.py                 # Core AI inference & mitigation pipeline
│   ├── decision_engine.py          # 2D Trust-Risk Decision Matrix
│   ├── trust_engine.py             # Zero-Trust Posture Score Calculator
│   ├── soc_agent.py                # Ollama autonomous SOC decision agent & guardrails
│   ├── explain.py                  # TreeSHAP explainability engine
│   ├── test_pipeline.py            # End-to-end multi-case pipeline test suite
│   ├── federated/                  # Federated Learning client/server scripts
│   └── redteam/                    # Adversarial perturbation & evasion scripts
├── frontend/                       # Vite + React SOC Dashboard
│   ├── src/
│   │   ├── App.jsx                 # Main dashboard layout & state management
│   │   ├── index.css               # Frosted glassmorphism design system
│   │   ├── hooks/                  # useWebSocket & polling hooks
│   │   └── components/
│   │       ├── FlowFeed.jsx        # Live scrolling flow telemetry feed
│   │       ├── EnsemblePanel.jsx   # Model A/B/C breakdown & explainability
│   │       ├── RiskGauge.jsx       # Circular SVG risk score gauge
│   │       ├── TrustPanel.jsx      # Zero-trust posture toggles + what-if simulation
│   │       ├── MitigationPanel.jsx # Windows Firewall, Cowrie & Telegram status
│   │       ├── FederatedPanel.jsx  # Federated learning convergence chart
│   │       └── RedTeamPanel.jsx    # Adversarial robustness stress-testing
├── data/                           # Replay and evaluation datasets
├── models/                         # Trained ML weights (.pkl artifacts)
├── iptables_action.py              # Windows Firewall netsh advfirewall rule manager
├── honeypot_redirect.py            # Cowrie SSH honeypot dispatcher
├── telegram_alert.py               # Telegram SOC alerting service
├── demo_live_stream.py             # Live traffic streaming demo script
├── launch_admin.bat                # Single-click elevated terminal launcher
├── stop_extra_containers.ps1       # Docker cleanup helper script
├── check_cowrie.ps1                # Standalone Honeypot port 2222 reachability check
└── README.md                       # Project documentation
```

---

## 🛠️ Windows Troubleshooting & FAQs

### 1. `WS Disconnected` in Dashboard Top Bar
* **Cause:** The backend server is not running on port 8000.
* **Fix:** In Terminal 1, run:
  ```powershell
  .\venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
  ```

### 2. PowerShell Script Execution Policy Error
* **Error:** `cannot be loaded because running scripts is disabled on this system.`
* **Fix:** Run this command once in PowerShell:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```

### 3. Port 8000 or 5173 Already in Use
* **Fix:** Kill lingering Python or Node processes:
  ```powershell
  Get-Process python, node -ErrorAction SilentlyContinue | Stop-Process
  ```

---

*TrustFlow NGFW — Next-Generation Zero-Trust AI Defense Architecture.*
