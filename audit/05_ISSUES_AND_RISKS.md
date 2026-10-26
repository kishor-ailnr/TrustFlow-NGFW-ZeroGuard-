# 05 - Issues, Risks, and Technical Debt Analysis

This document identifies all architectural bugs, logic inconsistencies, edge-case risks, and simulated values discovered across the TrustFlow NGFW codebase. As instructed, no fixes have been applied to existing files.

---

## 1. Deep-Dive Investigations (User-Specific Queries)

---

### Issue 1.1: Why PORT_SCANNING Flows with High Risk (~88) End Up as ALLOW

* **Target Files**:
  * [`demo_live_stream.py:41-46`](file:///c:/Music/TrustFlowNGFW/demo_live_stream.py#L41-L46)
  * [`backend/pipeline.py:154-164`](file:///c:/Music/TrustFlowNGFW/backend/pipeline.py#L154-L164)
  * [`honeypot_redirect.py:179-182`](file:///c:/Music/TrustFlowNGFW/honeypot_redirect.py#L179-L182)
  * [`data/incident_log.csv:615-626`](file:///c:/Music/TrustFlowNGFW/data/incident_log.csv#L615-L626)
* **Severity**: **HIGH**
* **Root Cause & Code Trace**:
  1. In `demo_live_stream.py` (lines 41–46), the curated scenario *"Suspicious Port Scan on Managed Device"* sends a `Port Scanning` attack row (index 21187) with posture flags: `mfa=True`, `healthy=True`, `location=False`, `hours=False`.
  2. `compute_trust_score` calculates: $30 (\text{mfa}) + 30 (\text{healthy}) = 60 \rightarrow \text{Medium Trust}$ ([trust_engine.py:3-22](file:///c:/Music/TrustFlowNGFW/backend/trust_engine.py#L3-L22)).
  3. The meta-learner calculates a fused risk score of $\approx 88.0$ (High Risk).
  4. In `backend/decision_engine.py:43`, the 2D decision matrix evaluates `("Medium", "High")`, producing **`Quarantine`**.
  5. In `backend/soc_agent.py:183-196`, even if the SOC agent review executes, the Zero-Trust policy floor forbids de-escalation below `Quarantine` because $risk\_score \ge 60$. Thus, `action` enters Step 3G as `Quarantine`.
  6. **The Critical Flaw**: In `backend/pipeline.py:154-164`:
     ```python
     if action == "Quarantine":
         asyncio.create_task(trigger_honeypot_connection_async(flow_id, source_ip=source_ip))
         simulate_vlan_quarantine(flow_id, source_ip)
         try:
             honeypot_verdict = watch_honeypot_and_judge(flow_id, source_ip=source_ip, timeout_seconds=4)
             if honeypot_verdict and honeypot_verdict.get("final_verdict") in ("Block", "Allow"):
                 action = honeypot_verdict["final_verdict"]
                 reason = f"{reason} | {honeypot_verdict['reason']}"
     ```
  7. `pipeline.py` calls `watch_honeypot_and_judge(flow_id, source_ip, timeout_seconds=4)`.
  8. In `honeypot_redirect.py:179-182`:
     ```python
     elif len(events_found) == 0:
         verdict = "Allow"
         reason = f"Honeypot feedback: Allow - no malicious activity observed in {timeout_seconds}s honeypot containment window"
     ```
  9. Because the Cowrie container is either not running or no attacker executed a real exploit script against port 2222 within the 4-second polling window, `len(events_found) == 0`.
  10. The watcher returns `verdict = "Allow"`.
  11. `pipeline.py:160` overwrites `action = "Allow"`, completely overruling both the ML ensemble and the Zero-Trust policy floor!
  12. **Empirical Proof**: The actual `data/incident_log.csv` confirms this exact bug occurred across 12 consecutive live runs (lines 615–626):
      `DEMO-PORT_SCANNING-915,Allow,info,Honeypot feedback: Allow - no malicious activity observed in 4s honeypot containment window`.
* **Suggested Fix**:
  Do NOT automatically de-escalate quarantined flows to `Allow` on empty honeypot logs. If no active exploit occurs within the window, the flow must remain in `Quarantine` (or maintain its decision-matrix action). In `honeypot_redirect.py:179-185`, change the default when `len(events_found) == 0` from `"Allow"` to `"Quarantine"`. In `pipeline.py:159`, only update `action` if `final_verdict == "Block"`.

---

### Issue 1.2: Red-Team Report Discrepancy (8 Flows vs. 3 Suites of 3 Flows) and Hardcoded Robustness

* **Target Files**:
  * [`backend/redteam/select_flows.py:27-31`](file:///c:/Music/TrustFlowNGFW/backend/redteam/select_flows.py#L27-L31)
  * [`backend/redteam/results/evasion_results.json:1-6`](file:///c:/Music/TrustFlowNGFW/backend/redteam/results/evasion_results.json#L1-L6)
  * [`frontend/src/pages/ReportsPage.jsx:332-345`](file:///c:/Music/TrustFlowNGFW/frontend/src/pages/ReportsPage.jsx#L332-L345)
* **Severity**: **HIGH**
* **Root Cause & Code Trace**:
  1. In `select_flows.py`, exactly 8 rows are selected from the dataset:
     * `robust_indices = [1496, 35292, 37697, 37698]` (4 flows)
     * `evadable_indices = [157230, 182154, 182224, 182677]` (4 flows)
     * Resulting in `total_tested: 8`, `still_detected: 5`, `evaded: 3` in `evasion_results.json`.
  2. In `ReportsPage.jsx` (lines 332–345), the PDF export table calculates:
     ```javascript
     const tested = redTeamData.total_tested || 24    // 8
     const detected = redTeamData.still_detected || 21 // 5
     const evaded = redTeamData.evaded || 3            // 3
     const robustnessRate = ((detected / tested) * 100).toFixed(1) // 62.5%

     body: [
       ['FGSM Feature Shift', '...', `${Math.round(tested * 0.4)} flows`, '91.7% Maintained Detection'],
       ['Packet Jitter Noise', '...', `${Math.round(tested * 0.35)} flows`, '88.9% Maintained Detection'],
       ['Stealth Evaded Flows', '...', `${evaded} flows`, 'Redirected to Honeypot via JA3/Anomaly'],
       ['Ensemble Defense Score', '...', `${tested} total flows`, `${robustnessRate}% Robustness Verified`],
     ]
     ```
  3. **Why the math doesn't add up**:
     * Suite 1 evaluates: `Math.round(8 * 0.4)` = **3 flows**.
     * Suite 2 evaluates: `Math.round(8 * 0.35)` = **3 flows**.
     * Suite 3 evaluates: `evaded` = **3 flows**.
     * Sum of suites: $3 + 3 + 3 =$ **9 flows**. But row 4 declares `${tested} total flows` = **8 flows**!
  4. **Hardcoded vs. Computed**:
     * The sub-suite percentages **`91.7% Maintained Detection`** and **`88.9% Maintained Detection`** are **100% HARDCODED string literals**. They are never calculated from the test data.
     * Only the bottom aggregate `${robustnessRate}%` ($5/8 = 62.5\%$) is computed dynamically.
* **Suggested Fix**:
  Structure `evasion_results.json` to store per-suite breakdown counts and detection percentages dynamically. In `ReportsPage.jsx`, read actual flow counts and detection rates from `redTeamData.suites` rather than hardcoding static percentage strings and fractional multipliers.

---

### Issue 1.3: Mean Zero-Trust Score, Flow Counts, and Dashboard Percentages Discrepancy

* **Target Files**:
  * [`frontend/src/pages/ReportsPage.jsx:16-89`](file:///c:/Music/TrustFlowNGFW/frontend/src/pages/ReportsPage.jsx#L16-L89)
  * [`frontend/src/App.jsx:55-58`](file:///c:/Music/TrustFlowNGFW/frontend/src/App.jsx#L55-L58)
  * [`frontend/src/hooks/useWebSocket.js:8-32`](file:///c:/Music/TrustFlowNGFW/frontend/src/hooks/useWebSocket.js#L8-L32)
* **Severity**: **MEDIUM**
* **Root Cause & Code Trace**:
  1. The backend does **not** provide any aggregation endpoint or stateful metrics API for historical average trust scores, cumulative flow counts, or action percentages.
  2. In `App.jsx`, all statistics are derived solely from the frontend's local React state: `flows`.
  3. In `useWebSocket.js`, `flows` is explicitly capped at `MAX_FLOWS = 100` via `.slice(0, 100)`.
  4. In `ReportsPage.jsx` (lines 16–45):
     ```javascript
     const hasFlows = Array.isArray(flows) && flows.length > 0
     const totalFlows = hasFlows ? flows.length : 128
     ...
     } else {
       // Baseline proportions when live traffic queue is initializing
       blocks = Math.round(totalFlows * 0.22)
       quarantines = Math.round(totalFlows * 0.18)
       ratelimits = Math.round(totalFlows * 0.15)
       allows = Math.max(0, totalFlows - blocks - quarantines - ratelimits)
     }
     ```
  5. When the user opens the Reports page before starting `demo_live_stream.py`, the dashboard renders **128 fabricated flows**, **74 average trust**, and hardcoded distribution percentages (22% block, 18% quarantine, 15% rate-limit).
  6. Even when live flows are streaming, the numbers only reflect the rolling window of the last 100 WebSocket packets held in browser RAM, not the true total processed by the firewall engine since boot.
* **Suggested Fix**:
  Implement a lightweight aggregation endpoint on the FastAPI backend (`/api/stats`) that maintains in-memory or SQLite rolling counters (`total_inspected`, `total_blocks`, `total_quarantines`, `total_ratelimits`, `total_allows`, `sum_trust_score`). Expose this via `usePolling` so reports reflect authoritative server-side ground truth.

---

## 2. Inventory of Hardcoded, Simulated, or Demo Data

| Component / File | Code Location | Hardcoded / Simulated Value | Impact on Credibility |
|---|---|---|---|
| `backend/train_ensemble.py` | Lines 73–80 | `assign_ja3()` randomly assigns known malicious hashes (`random.random() < 0.6`) because CIC-IDS2017 lacks TLS metadata | Replay dataset JA3 intelligence is synthetically generated |
| `honeypot_redirect.py` | Lines 12–37 | `SAMPLE_COMMAND_SEQUENCES` hardcodes fake hacker commands (`whoami`, `cat /etc/passwd`, `wget recon.sh`) | Decoy terminal shows pre-scripted canned attacks |
| `honeypot_redirect.py` | Lines 100–115 | Keystrokes logged and payloads intercepted are calculated from hardcoded strings (`len(cmd) + 24`) | Sensor counts are synthesized |
| `backend/decision_engine.py` | Lines 68–83 | `simulate_vlan_quarantine()` writes to in-memory dict with `"simulated": True` | No real network switch VLAN tagging occurs |
| `frontend/src/components/Sidebar.jsx` | Lines 135–148 | Ollama Agent and Active Defense pills display green `"online"` LED unconditionally | Indicators remain green even if Ollama or Docker are stopped |
| `frontend/src/pages/ReportsPage.jsx` | Lines 227–230 | Model contribution shares (`48.2%`, `29.4%`, `22.4%`, `100.0%`) in the PDF preview table | Static percentages presented as live telemetry |
| `frontend/src/pages/ReportsPage.jsx` | Lines 341–342 | Red-team robustness benchmarks (`91.7%`, `88.9%`) in PDF export | Static percentages presented as empirical test results |
| `frontend/src/pages/AdversarialPage.jsx` | Lines 9–16 | 6 fallback flow rows (`adv-fgsm-001`, `adv-jitter-002`, etc.) when backend data is absent | Pre-scripted dummy rows presented as live test vectors |
| `frontend/src/components/FlowDetailPage.jsx` | Lines 54–89 | `getHumanFriendlyDiagnosis()` matches substring keywords in `flow_id` (`PORT_SCAN`, `DDOS`, `BRUTE`) | AI diagnosis is a template rule, not LLM-generated inference |
| `frontend/src/components/CircuitBackground.jsx` | Line 5 | Returns `null` | Dead component retaining legacy name |

---

## 3. Concurrency, Race Conditions, and Reliability Issues

---

### Issue 3.1: Synchronous `time.sleep` Inside Async WebSocket Handler Freezes FastAPI

* **Target File**: [`backend/pipeline.py:158`](file:///c:/Music/TrustFlowNGFW/backend/pipeline.py#L158) invoking [`honeypot_redirect.py:139`](file:///c:/Music/TrustFlowNGFW/honeypot_redirect.py#L139)
* **Severity**: **HIGH**
* **Explanation**:
  `process_flow()` is an `async def` function running on the main FastAPI asyncio event loop. When a flow is quarantined, it calls `honeypot_verdict = watch_honeypot_and_judge(...)`.
  Inside `watch_honeypot_and_judge`, line 139 executes:
  `time.sleep(poll_interval)`
  inside a `while` loop lasting up to 4–6 seconds!
  Because `time.sleep` is synchronous and blocking, it **freezes the entire asyncio event loop thread**. During these 4 seconds:
  * No WebSocket pings or packets can be received or sent.
  * No REST API requests can be answered.
  * Other connected browser dashboards freeze.
* **Suggested Fix**:
  Refactor `watch_honeypot_and_judge` to be `async def` using `await asyncio.sleep(poll_interval)`, or offload its execution via `await loop.run_in_executor(None, watch_honeypot_and_judge, ...)`.

---

### Issue 3.2: Unmounted Component WebSocket Reconnection Loop & Memory Leak

* **Target File**: [`frontend/src/hooks/useWebSocket.js:21-39`](file:///c:/Music/TrustFlowNGFW/frontend/src/hooks/useWebSocket.js#L21-L39)
* **Severity**: **MEDIUM**
* **Explanation**:
  In `useWebSocket.js`:
  ```javascript
  ws.onclose = () => {
    setConnected(false)
    setTimeout(connect, 3000) // auto-reconnect after 3s
  }
  useEffect(() => {
    connect()
    return () => wsRef.current?.close()
  }, [connect])
  ```
  When the component unmounts (or during React 19 StrictMode double-mounting), `wsRef.current?.close()` executes in the cleanup function. Closing the WebSocket triggers its `ws.onclose` event handler. The handler immediately schedules a timer: `setTimeout(connect, 3000)`. Because there is no cancellation check or unmount flag, `connect()` runs 3 seconds later on an unmounted component, opening a dangling WebSocket connection and throwing React state update warnings.
* **Suggested Fix**:
  Maintain a `mountedRef = useRef(true)` or `reconnectTimeoutRef = useRef(null)`. In the `useEffect` cleanup function, set `mountedRef.current = false` and call `clearTimeout(reconnectTimeoutRef.current)`.

---

### Issue 3.3: Missing Error Boundary on TreeSHAP Calculation

* **Target File**: [`backend/pipeline.py:93-101`](file:///c:/Music/TrustFlowNGFW/backend/pipeline.py#L93-L101)
* **Severity**: **MEDIUM**
* **Explanation**:
  `explainer.shap_values(df_row)` is called synchronously without a `try...except` block. If a packet contains NaN, non-numeric strings, or an unexpected schema dimension, SHAP raises an internal exception. This causes `process_flow()` to crash unhandled, abruptly terminating the client's WebSocket connection without returning an informative JSON error message.
* **Suggested Fix**:
  Wrap SHAP calculation in a `try...except Exception as e:` block. If SHAP fails, log the warning and fall back to top features extracted from XGBoost's static `feature_importances_`.

---

### Issue 3.4: Silent Privilege Failure on Windows Netsh Commands

* **Target File**: [`iptables_action.py:8-17`](file:///c:/Music/TrustFlowNGFW/iptables_action.py#L8-L17)
* **Severity**: **LOW**
* **Explanation**:
  `netsh advfirewall firewall add rule ...` requires administrative privileges on Windows. When the backend is run in a standard non-elevated terminal, `subprocess.run` raises `CalledProcessError` (access denied). The exception is caught and printed to console (`[Firewall] Could not add rule for ... - likely needs admin rights`), but returns `False`. In `backend/pipeline.py:167`, the return value is ignored. The pipeline logs that the flow was "Blocked" and informs the UI that a kernel rule was applied, even though no packet filtering actually took place.
* **Suggested Fix**:
  Return firewall enforcement success/failure status in the evaluated flow dictionary (`"kernel_rule_applied": bool`) and display an administrative elevation warning badge on the dashboard if kernel enforcement fails.

---

## 4. Summary Matrix of All Identified Issues

| Ref # | Category | Description | Severity | File & Line Range |
|---|---|---|---|---|
| 1.1 | Logic Error | Port scan flows (~88 risk) flip to `Allow` due to empty honeypot log | **HIGH** | [`pipeline.py:154-164`](file:///c:/Music/TrustFlowNGFW/backend/pipeline.py#L154-L164), [`honeypot_redirect.py:179-182`](file:///c:/Music/TrustFlowNGFW/honeypot_redirect.py#L179-L182) |
| 1.2 | Inconsistency | Red-team PDF shows 9 flows across 3 suites vs 8 total; hardcoded 91.7%/88.9% | **HIGH** | [`ReportsPage.jsx:332-345`](file:///c:/Music/TrustFlowNGFW/frontend/src/pages/ReportsPage.jsx#L332-L345) |
| 1.3 | Data Integrity | Mean Zero-Trust score and flow counts are rolling client RAM or hardcoded fallback (128 flows) | **MEDIUM** | [`ReportsPage.jsx:16-89`](file:///c:/Music/TrustFlowNGFW/frontend/src/pages/ReportsPage.jsx#L16-L89) |
| 3.1 | Concurrency | Synchronous `time.sleep` in honeypot watcher freezes FastAPI event loop | **HIGH** | [`pipeline.py:158`](file:///c:/Music/TrustFlowNGFW/backend/pipeline.py#L158), [`honeypot_redirect.py:139`](file:///c:/Music/TrustFlowNGFW/honeypot_redirect.py#L139) |
| 3.2 | Race Condition | Reconnection timer in `useWebSocket` fires after unmount | **MEDIUM** | [`useWebSocket.js:21-39`](file:///c:/Music/TrustFlowNGFW/frontend/src/hooks/useWebSocket.js#L21-L39) |
| 3.3 | Error Handling | Unhandled SHAP exception drops WebSocket connection on dirty data | **MEDIUM** | [`pipeline.py:93-101`](file:///c:/Music/TrustFlowNGFW/backend/pipeline.py#L93-L101) |
| 3.4 | Security / Admin | Silent failure of `netsh advfirewall` without administrator privileges | **LOW** | [`iptables_action.py:8-17`](file:///c:/Music/TrustFlowNGFW/iptables_action.py#L8-L17) |
| 4.1 | Dead Code | `FederatedPanel.jsx` and `App.css` exist in repository but are completely unreferenced | **LOW** | [`FederatedPanel.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/FederatedPanel.jsx), [`App.css`](file:///c:/Music/TrustFlowNGFW/frontend/src/App.css) |
| 4.2 | Styling Defect | 43 hardcoded colors remain outside CSS custom properties | **LOW** | [`index.css`](file:///c:/Music/TrustFlowNGFW/frontend/src/index.css) |
