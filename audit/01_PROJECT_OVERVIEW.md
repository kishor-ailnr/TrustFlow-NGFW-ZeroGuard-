# 01 - Project Overview: TrustFlow NGFW (ZeroGuard)

## 1. Application Summary (10 Lines)

1. TrustFlow NGFW (ZeroGuard) is an AI-driven Next-Generation Firewall and Security Operations Center (SOC) platform.
2. It evaluates network packet flows through a two-dimensional decision paradigm combining continuous Zero-Trust identity scores and AI risk scores.
3. Machine learning threat detection uses a 3-part ensemble: supervised XGBoost (Model A), unsupervised Isolation Forest anomaly detection (Model B), and JA3 TLS client fingerprint threat intelligence (Model C).
4. A Logistic Regression meta-learner fuses sub-model probabilities into a calibrated 0–100 risk score with TreeSHAP local feature attribution.
5. A deterministic 2D decision matrix maps Trust Band (High, Medium, Low) and Risk Band (Low, Medium, High) into four enforcement actions: Allow, Rate-limit, Quarantine, and Block.
6. Borderline flows (Rate-limit, Quarantine) trigger an autonomous SOC agent powered by local Ollama LLM (`llama3.2`) with tool calling and strict policy guardrails.
7. Active defense applies real kernel-level Windows Firewall packet filtering via `netsh advfirewall` CLI commands for Block verdicts.
8. Quarantined flows trigger automated decoy SSH honeypot containment against a Cowrie container on port 2222 with simulated VLAN 99 port tagging.
9. An automated honeypot watcher inspects Cowrie session logs for payload downloads or suspicious commands to issue follow-up verdicts.
10. The frontend is a React 19 / Vite single-page application communicating via WebSocket (`/ws`) and REST polling for live flow monitoring, red-team analysis, and executive PDF reporting.

---

## 2. Complete File Tree & Purpose

| File Path | Purpose / Description |
|---|---|
| `.env` | Environment configuration containing Telegram bot token and chat ID `[REDACTED]`. |
| `.gitignore` | Git exclusion rules for virtual environments, node modules, build artifacts, and large CSVs. |
| `check_cowrie.ps1` | PowerShell diagnostic testing TCP reachability of Cowrie SSH honeypot on port 2222. |
| `check_data.py` | CLI diagnostic utility verifying integrity and shape of `data/replay_holdout.csv`. |
| `cowrie.json` | Sample/cached Cowrie honeypot event telemetry log for offline testing. |
| `demo_live_stream.py` | Interactive client streaming simulated network scenarios to backend via WebSocket (`/ws`). |
| `generate_pdf_report.py` | Python script utilizing ReportLab to compile a master SIH evaluation PDF document. |
| `honeypot_redirect.py` | Decoy socket connection, simulated session synthesis, and log watcher for Cowrie honeypot. |
| `iptables_action.py` | Kernel firewall rule manager executing Windows Firewall `netsh advfirewall` CLI commands. |
| `launch_admin.bat` | Windows batch launcher opening an elevated Administrator PowerShell prompt in workspace root. |
| `quarantine_test_payload.json` | JSON test fixture for injecting quarantine-scenario network flow payloads. |
| `README.md` | Master project documentation, architecture schematics, and step-by-step setup guide. |
| `stop_extra_containers.ps1` | PowerShell script stopping non-Cowrie Docker containers to free CPU/RAM for local LLM inference. |
| `telegram_alert.py` | Dispatches real-time security alerts to Telegram channels for Block and Quarantine actions. |
| `test_high_risk_flow.py` | End-to-end integration test asserting DoS attack flows trigger Block or Quarantine actions. |
| `test_integration.py` | Multi-scenario test verifying Allow, Rate-limit, Quarantine, and Block decision pipeline paths. |
| `test_quarantine_confirmed.py` | Unit test validating honeypot watcher and VLAN state behavior on quarantined flows. |
| `test_quarantine_flow.py` | Detailed test case verifying honeypot redirection, session creation, and watcher feedback. |
| `test_websocket.py` | Diagnostic script validating bidirectional WebSocket connectivity against backend `/ws`. |
| `TrustFlow_NGFW_Complete_SIH_Project_Analysis.pdf` | Pre-generated executive presentation report document for evaluation. |
| `ws_test.py` | Minimal socket probe testing raw WebSocket JSON message exchange. |
| `ws_test.py.save` | Backup scratch copy of the WebSocket test script. |
| `backend/__init__.py` | Python package initializer for the backend module. |
| `backend/decision_engine.py` | 2D matrix mapping (Trust Band × Risk Band), risk threshold overrides, and simulated VLAN state. |
| `backend/explain.py` | TreeSHAP explainer script pre-generating feature attribution and human-readable text for replay data. |
| `backend/fix_explanations.py` | Post-processing utility sanitizing benign flow explanations in `data/replay_final.csv`. |
| `backend/main.py` | FastAPI application defining REST endpoints, CORS middleware, and WebSocket broadcasting server. |
| `backend/pipeline.py` | Core flow processing orchestrator coordinating models, trust engine, SOC agent, and active defense. |
| `backend/soc_agent.py` | Autonomous SOC agent wrapping Ollama `llama3.2`, tool definitions, guardrails, and audit logger. |
| `backend/test_agent_tools.py` | Test harness checking Ollama LLM tool-calling functionality with schema validation. |
| `backend/test_pipeline.py` | End-to-end test validating the complete asynchronous pipeline execution on sample CSV rows. |
| `backend/train_ensemble.py` | Model training script for Isolation Forest (Model B), JA3 simulation, and Logistic meta-learner. |
| `backend/train_model.py` | Supervised XGBoost (Model A) training script parsing CIC-IDS2017 and exporting replay holdout. |
| `backend/trust_engine.py` | Calculates 0–100 Zero-Trust continuous identity score based on 4 weighted posture signals. |
| `backend/federated/__init__.py` | Python package initializer for federated learning module. |
| `backend/federated/client.py` | Flower federated learning client training local XGBoost/Logistic classifiers across client nodes. |
| `backend/federated/data_split.py` | Partitions CIC-IDS2017 dataset into non-IID subsets for Client 0 and Client 1. |
| `backend/federated/run_federated_demo.py` | Orchestration script launching Flower server and two client subprocesses for 3 rounds. |
| `backend/federated/server.py` | Flower federated learning aggregation server running `FedAvg` with round-by-round accuracy logging. |
| `backend/federated/data/client_0.csv` | Non-IID training split allocated to Federated Client 0. |
| `backend/federated/data/client_1.csv` | Non-IID training split allocated to Federated Client 1. |
| `backend/federated/results/accuracy_log.json` | Logged accuracy results per round exported by Flower federated server. |
| `backend/redteam/__init__.py` | Python package initializer for red-teaming evasion module. |
| `backend/redteam/perturb.py` | Adversarial perturbation functions modifying packet lengths, timing, and headers. |
| `backend/redteam/run_redteam_test.py` | Executes baseline vs perturbed evaluation across malicious flows and logs evasion stats. |
| `backend/redteam/select_flows.py` | Selects 8 candidate attack flows (4 robust, 4 evadable) from CIC-IDS2017 into sample CSV. |
| `backend/redteam/data/malicious_sample.csv` | 8 selected raw attack flows used for red-team adversarial evasion benchmarks. |
| `backend/redteam/results/evasion_results.json` | Benchmarked detection vs evasion metrics produced by `run_redteam_test.py`. |
| `data/cicids2017_cleaned.csv` | Cleaned primary dataset derived from Canadian Institute for Cybersecurity IDS 2017 dataset. |
| `data/incident_log.csv` | Append-only audit ledger recording autonomous SOC agent decisions, overrides, and timestamps. |
| `data/replay_enriched.csv` | Replay holdout dataset enriched with sub-model predictions, JA3 hashes, and fused risk scores. |
| `data/replay_final.csv` | Enriched replay dataset with TreeSHAP primary model attribution and natural language explanations. |
| `data/replay_holdout.csv` | 15% held-out test split of CIC-IDS2017 reserved for live demo streaming and validation. |
| `frontend/.gitignore` | Git exclusion rules for node_modules and frontend production build outputs. |
| `frontend/.oxlintrc.json` | Configuration file for the Oxlint high-performance JavaScript/JSX linter. |
| `frontend/index.html` | HTML entry template loading web fonts, root container, and React entry point. |
| `frontend/package.json` | Node.js project manifest defining React 19 dependencies, build scripts, and dev tools. |
| `frontend/package-lock.json` | Pinned dependency tree lockfile for reproducible npm installations. |
| `frontend/README.md` | Standard Vite React template readme document. |
| `frontend/vite.config.js` | Vite bundler configuration including React plugin integration. |
| `frontend/public/favicon.svg` | SVG favicon emblem displaying the TrustFlow shield logo. |
| `frontend/public/icons.svg` | Reusable SVG symbol definitions for dashboard icons. |
| `frontend/public/logo.png` | Raster logo image asset. |
| `frontend/src/App.css` | Unused legacy Vite default styling file (not imported by application). |
| `frontend/src/App.jsx` | Top-level React component managing theme, navigation tabs, active flow selection, and layouts. |
| `frontend/src/index.css` | Main application stylesheet containing design system, layout rules, and component styles. |
| `frontend/src/main.jsx` | Application bootstrap file mounting `<App />` within React `<StrictMode>` into DOM `#root`. |
| `frontend/src/tokens.css` | Design token definitions for light and dark themes (CSS custom properties). |
| `frontend/src/utils.js` | Helper utilities for risk classification bands, trust colors, and percentage formatting. |
| `frontend/src/assets/hero.png` | Graphical hero image asset. |
| `frontend/src/assets/react.svg` | Default React framework SVG icon asset. |
| `frontend/src/assets/vite.svg` | Default Vite build tool SVG icon asset. |
| `frontend/src/components/CircuitBackground.jsx` | Flattened background wrapper component returning `null` (legacy circuit canvas removed). |
| `frontend/src/components/EnsemblePanel.jsx` | Displays Circular Risk Gauge, sub-model bar charts (A, B, C), and SHAP primary driver pill. |
| `frontend/src/components/FederatedPanel.jsx` | Recharts line chart displaying federated learning accuracy across training rounds (unused in App.jsx). |
| `frontend/src/components/FlowDetailPage.jsx` | In-depth inspection view showing human-friendly AI diagnostics, full SHAP breakdown, and packet features. |
| `frontend/src/components/FlowFeed.jsx` | Real-time scrolling feed list of evaluated flows with live score roll-up animations. |
| `frontend/src/components/MitigationPanel.jsx` | Displays firewall enforcement status, Cowrie honeypot decoy terminal, and Telegram dispatch info. |
| `frontend/src/components/RedTeamPanel.jsx` | Summary card and table benchmarking model detection rate against perturbed adversarial attacks. |
| `frontend/src/components/RiskGauge.jsx` | SVG chronograph dial displaying fused risk score (0–100) with animated tick marks. |
| `frontend/src/components/Sidebar.jsx` | Enterprise navigation bar supporting tab switching, status indicators, and dark/light mode toggle. |
| `frontend/src/components/TrustPanel.jsx` | Zero-Trust posture score breakdown with interactive toggle switches and real-time re-send capability. |
| `frontend/src/hooks/usePolling.js` | Custom React hook for polling REST API endpoints on a specified recurring millisecond interval. |
| `frontend/src/hooks/useWebSocket.js` | Custom React hook managing persistent connection, message decoding, and state for `/ws`. |
| `frontend/src/pages/AdversarialPage.jsx` | Full page view for red-team stress testing benchmarks and flow perturbation analysis. |
| `frontend/src/pages/IncidentsPage.jsx` | Full page view displaying immutable audit trail of autonomous SOC agent decisions and VLAN states. |
| `frontend/src/pages/ReportsPage.jsx` | Executive reporting console generating and downloading certified compliance PDF documents. |
| `models/feature_cols.pkl` | Pickled Python list of the 52 numerical feature column names extracted from CIC-IDS2017. |
| `models/iso_forest.pkl` | Serialized scikit-learn Isolation Forest model trained on benign network flows (Model B). |
| `models/label_encoder.pkl` | Serialized scikit-learn LabelEncoder mapping attack strings to integer classes. |
| `models/meta_model.pkl` | Serialized scikit-learn LogisticRegression model fusing sub-model risk predictions into 0–100 score. |
| `models/xgb_model.pkl` | Serialized XGBoost multiclass classifier trained to detect known attack signatures (Model A). |

---

## 3. Technology Stack & Exact Versions

### Python Environment (`requirements` / `pip list` in `venv`)
* **Python Runtime**: `3.10+` (Windows x64)
* **Web Framework**: `fastapi` `0.138.2`, `starlette` `1.3.1`, `uvicorn` `0.49.0`
* **Machine Learning & Math**:
  * `xgboost` `3.2.0`
  * `scikit-learn` `1.9.0`
  * `shap` `0.51.0`
  * `numpy` `2.4.6`
  * `pandas` `3.0.5`
  * `scipy` `1.17.1`
  * `joblib` `1.5.3`
* **Federated Learning**: `flwr` (Flower) `1.33.0`
* **AI & Agentic Review**: `ollama` `0.6.2` (invoking `llama3.2` locally)
* **Networking & HTTP**:
  * `websockets` `17.0.1`
  * `httpx` `0.28.1`
  * `requests` `2.34.2`
  * `paramiko` `5.0.0`
* **Reporting & Data**:
  * `reportlab` `5.0.1`
  * `python-dotenv` `1.2.2`
  * `pydantic` `2.13.4`

### Frontend Environment (`frontend/package.json`)
* **Framework**: React `^19.2.8`
* **DOM Renderer**: `react-dom` `^19.2.8`
* **Build System / Dev Server**: `vite` `^8.2.0` (running `v8.2.1`)
* **Data Visualization**: `recharts` `^3.10.1`
* **PDF Export Engine**: `jspdf` `^4.2.1`
* **PDF Table Plugin**: `jspdf-autotable` `^5.0.8`
* **Code Quality & Linting**: `oxlint` `^1.75.0`
* **Type Declarations**: `@types/react` `^19.2.17`, `@types/react-dom` `^19.2.3`
* **Vite Plugin**: `@vitejs/plugin-react` `^6.0.4`

---

## 4. Run Guide & Startup Sequence

To run the complete system on Windows, execute the steps in the exact order below.

### External Service Prerequisites
1. **Docker Desktop**: Must be active if Cowrie honeypot is tested (`docker run -d -p 2222:2222 --name cowrie cowrie/cowrie:latest`). Verify with `check_cowrie.ps1`.
2. **Ollama Service**: Must be running locally on `http://127.0.0.1:11434` with model `llama3.2` pulled (`ollama run llama3.2`).
3. **Elevated Privileges**: Windows Firewall rule modification (`netsh advfirewall`) requires administrative rights. Open terminal via `launch_admin.bat` or Run as Administrator.

### Startup Order & Commands

#### Terminal 1 — FastAPI Backend (Port 8000)
```powershell
cd C:\Music\TrustFlowNGFW
.\venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
* Status verify: `http://127.0.0.1:8000/docs`
* WebSocket listener: `ws://127.0.0.1:8000/ws`

#### Terminal 2 — Vite Frontend (Port 5173)
```powershell
cd C:\Music\TrustFlowNGFW\frontend
npm run dev
```
* Status verify: Open browser at `http://localhost:5173/`
* Header indicator should reflect `● WS Connected`

#### Terminal 3 — Live Traffic Replay Streamer
```powershell
cd C:\Music\TrustFlowNGFW
.\venv\Scripts\python.exe demo_live_stream.py
```
* Network flows begin streaming into the dashboard across 6 curated scenarios.

---

## 5. Current Git State

* **Active Branch**: `ui-redesign`
* **Working Tree**: Clean (no uncommitted modifications in repository)
* **Last Commit**: `f1e86c3bbe26ed7f86ebdae852f093b2a1b65162`
* **Commit Message**: `chore: checkpoint before UI redesign (backend, SOC agent, frontend pages)`
* **Author**: `kishor-ailnr <vrkishorraj@gmail.com>`
* **Date**: `Wed Oct 21 09:06:44 2026 +0530`

---

## 6. Security Findings

> [!CAUTION]
> **Credential Exposure Identified in Workspace**

* **Target File**: [`.env`](file:///c:/Music/TrustFlowNGFW/.env)
* **Exposed Variables**:
  * `TELEGRAM_BOT_TOKEN=[REDACTED]`
  * `TELEGRAM_CHAT_ID=[REDACTED]`
* **Finding Details**: The `.env` file containing live Telegram Bot API authentication credentials and destination chat identifiers was committed directly to the project root directory. Although `.gitignore` exists, `.env` was previously added or not ignored before rule creation.
* **Remediation Recommendation**: Invalidate and regenerate the bot token via Telegram `@BotFather`, remove `.env` from Git index tracking (`git rm --cached .env`), and inject credentials via system environment variables or secure vault stores.
