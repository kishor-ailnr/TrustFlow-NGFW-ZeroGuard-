# 03 - Frontend Component Inventory and Hierarchy

---

## 1. Component Hierarchy Tree

```mermaid
graph TD
    Main[main.jsx] --> App[App.jsx]
    App --> Circuit[CircuitBackground.jsx (Returns null)]
    App --> Sidebar[Sidebar.jsx]
    
    %% Conditional Rendering in App.jsx based on viewingDetailFlow & currentTab
    App --> ViewDetail{viewingDetailFlow?}
    
    ViewDetail -- Yes --> FlowDetail[FlowDetailPage.jsx]
    FlowDetail --> GaugeDetail[RiskGauge.jsx]
    
    ViewDetail -- No --> TabSwitch{currentTab?}
    
    TabSwitch -- 'reports' --> Reports[ReportsPage.jsx]
    TabSwitch -- 'adversarial' --> AdvPage[AdversarialPage.jsx]
    TabSwitch -- 'incidents' --> IncPage[IncidentsPage.jsx]
    
    TabSwitch -- 'dashboard' (Default) --> DashboardLayout[Dashboard View]
    DashboardLayout --> Header[topbar]
    DashboardLayout --> Feed[FlowFeed.jsx]
    DashboardLayout --> Ensemble[EnsemblePanel.jsx]
    Ensemble --> RiskGauge[RiskGauge.jsx]
    DashboardLayout --> Trust[TrustPanel.jsx]
    DashboardLayout --> Mitigation[MitigationPanel.jsx]
    DashboardLayout --> RedTeam[RedTeamPanel.jsx]
    
    %% Dead / Unused
    App -. Unused / Unreferenced .-> FedPanel[FederatedPanel.jsx]
```

---

## 2. Component Inventory (In Render Order)

---

### 1. `main.jsx`
* **File Path**: [`frontend/src/main.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/main.jsx)
* **On-Screen Display**: Root application mount point. Does not render independent UI.
* **Props & State**: None.
* **Feeds / Data Sources**: None.
* **Child Components**: [`App`](file:///c:/Music/TrustFlowNGFW/frontend/src/App.jsx) (wrapped in `<StrictMode>`).
* **CSS Class Names**: None. Mounts to DOM element `#root`.
* **Events & Interactions**: None.
* **Libraries Used**: `react` (StrictMode), `react-dom/client` (`createRoot`).

---

### 2. `App.jsx`
* **File Path**: [`frontend/src/App.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/App.jsx)
* **On-Screen Display**: Application shell encompassing navigation sidebar, top navigation bar, status indicators, and the primary content viewport.
* **Props**: None (Root component).
* **State**:
  * `currentTab`: `'dashboard' | 'adversarial' | 'incidents' | 'reports'` (default: `'dashboard'`).
  * `selectedFlow`: Flow object currently selected for inspection in dashboard panels.
  * `viewingDetailFlow`: Flow object currently open in full detail mode (or `null`).
  * `theme`: `'light' | 'dark'` (persisted in `localStorage` under `'trustflow-theme'`).
* **Feeds / Data Sources**:
  * `useWebSocket()`: Connects to `ws://127.0.0.1:8000/ws` -> provides `flows` array, `connected` boolean, and `sendFlow` dispatcher.
  * `usePolling('http://127.0.0.1:8000/api/vlan-status', 4000)`: Simulated VLAN quarantine states.
  * `usePolling('http://127.0.0.1:8000/api/redteam-status', 5000)`: Adversarial evasion metrics.
  * `usePolling('http://127.0.0.1:8000/api/incident-logs', 4000)`: SOC agent audit records.
* **Child Components**:
  * [`CircuitBackground`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/CircuitBackground.jsx)
  * [`Sidebar`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/Sidebar.jsx)
  * [`FlowDetailPage`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/FlowDetailPage.jsx)
  * [`ReportsPage`](file:///c:/Music/TrustFlowNGFW/frontend/src/pages/ReportsPage.jsx)
  * [`AdversarialPage`](file:///c:/Music/TrustFlowNGFW/frontend/src/pages/AdversarialPage.jsx)
  * [`IncidentsPage`](file:///c:/Music/TrustFlowNGFW/frontend/src/pages/IncidentsPage.jsx)
  * [`FlowFeed`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/FlowFeed.jsx)
  * [`EnsemblePanel`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/EnsemblePanel.jsx)
  * [`TrustPanel`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/TrustPanel.jsx)
  * [`MitigationPanel`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/MitigationPanel.jsx)
  * [`RedTeamPanel`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/RedTeamPanel.jsx)
* **CSS Class Names**:
  * `app-shell-layout`, `app-main-viewport`, `dashboard`, `topbar`, `topbar-logo`, `topbar-emblem`, `topbar-brand`, `brand-title`, `accent-text`, `sub-badge`, `sub`, `topbar-meta`, `meta-item`, `date-tag`, `ws-status`, `ws-dot`, `connected`, `ws-label`, `flow-counter-wrap`, `odometer-number`, `counter-label`, `theme-toggle-pill`, `main-grid`, `right-grid`, `extended-adversarial-col`.
* **Events & Interactions**:
  * Clicking topbar theme toggle pill toggles `'light'` / `'dark'` theme via `document.documentElement.setAttribute('data-theme', theme)`.
* **Libraries Used**: Native React hooks (`useState`, `useEffect`, `useRef`).

---

### 3. `CircuitBackground.jsx`
* **File Path**: [`frontend/src/components/CircuitBackground.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/CircuitBackground.jsx)
* **On-Screen Display**: None. Returns `null` (legacy canvas circuit animations were removed during flat UI redesign).
* **Props & State**: None.
* **Child Components**: None.
* **CSS Class Names**: None.

---

### 4. `Sidebar.jsx`
* **File Path**: [`frontend/src/components/Sidebar.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/Sidebar.jsx)
* **On-Screen Display**: Fixed left navigation rail displaying branding, 4 tab links with badge counts, live system integrity indicators (FastAPI, Ollama, Active Defense), and theme toggle button.
* **Props**:
  * `currentTab`: string (`'dashboard'`, `'adversarial'`, `'incidents'`, `'reports'`).
  * `onSelectTab`: callback `(tabId) => void`.
  * `flowCount`: integer length of flows array.
  * `wsConnected`: boolean WebSocket connection status.
  * `theme`: string `'light' | 'dark'`.
  * `toggleTheme`: callback `() => void`.
* **State**: None (controlled component).
* **Child Components**: None (inline SVGs).
* **CSS Class Names**:
  * `app-sidebar`, `sidebar-brand`, `sidebar-logo-emblem`, `sidebar-brand-text`, `brand-main`, `accent-text`, `brand-tag`, `sidebar-nav-section`, `sidebar-section-title`, `sidebar-nav`, `sidebar-nav-item`, `active`, `nav-icon`, `nav-info`, `nav-title`, `nav-subtitle`, `nav-badge`, `badge-info`, `badge-block`, `badge-accent`, `badge-allow`, `nav-indicator`, `sidebar-defense-status`, `status-cards-col`, `status-pill`, `status-led`, `online`, `offline`, `status-text`, `status-label`, `status-value`, `sidebar-footer`, `sidebar-footer-row`, `sidebar-version`, `sidebar-status-sub`, `theme-toggle-sidebar-btn`.
* **Events & Interactions**:
  * Clicking any nav item calls `onSelectTab(item.id)`, resetting detail view and switching page.
  * Clicking footer theme toggle icon executes `toggleTheme()`.

---

### 5. `FlowFeed.jsx`
* **File Path**: [`frontend/src/components/FlowFeed.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/FlowFeed.jsx)
* **On-Screen Display**: Vertical scrolling list of inspected network flows (up to 100), displaying Flow ID, Source IP, Trust Score + Band, Timestamp, animated Fused Risk Score, and Action Pill.
* **Props**:
  * `flows`: array of flow objects.
  * `selectedFlowId`: string ID of active flow.
  * `onSelect`: callback `(flow) => void`.
  * `onOpenDetail`: callback `(flow) => void`.
* **State**: Local `FlowScore` sub-component maintains animated `val` count-up state using `requestAnimationFrame`.
* **Child Components**: Internal helper `FlowScore`.
* **CSS Class Names**:
  * `panel`, `span-row`, `panel-stage-1`, `panel-header`, `panel-title`, `panel-badge`, `panel-body`, `empty-state`, `flow-feed-list`, `flow-item`, `selected`, `flow-main`, `flow-id-row`, `flow-id`, `flow-inspect-pill`, `flow-meta`, `flow-ip`, `flow-trust`, `flow-time`, `flow-right`, `flow-risk`, `crit`, `high`, `med`, `low`, `action-pill`, `allow`, `rate-limit`, `quarantine`, `block`.
* **Events & Interactions**:
  * Clicking a flow row invokes `onSelect(flow)`.
  * Clicking "Inspect ↗" button invokes `onOpenDetail(flow)` with `e.stopPropagation()`.

---

### 6. `EnsemblePanel.jsx`
* **File Path**: [`frontend/src/components/EnsemblePanel.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/EnsemblePanel.jsx)
* **On-Screen Display**: Centerpiece Risk Gauge dial, three animated horizontal progress bars for Model A (XGBoost), Model B (Isolation Forest), Model C (JA3 TLS), and TreeSHAP primary driver summary pill.
* **Props**:
  * `flow`: active selected flow object (or null).
  * `onOpenDetail`: callback `(flow) => void`.
* **State**: Internal `ModelBar` sub-component manages `filled` boolean animation state via `setTimeout`.
* **Child Components**:
  * [`RiskGauge`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/RiskGauge.jsx)
  * Internal helper `ModelBar`.
* **CSS Class Names**:
  * `panel`, `panel-stage-2`, `panel-header`, `panel-title`, `panel-badge`, `flow-id-badge`, `panel-body`, `empty-state`, `detail-panel`, `decluttered-ensemble`, `gauge-wrap`, `ensemble-row`, `model-bar-wrap`, `model-bar-label`, `model-name`, `model-val`, `bar-track`, `bar-fill`, `bar-a`, `bar-b`, `bar-c`, `ensemble-summary-box`, `shap-driver-pill`, `shap-driver-label`, `shap-driver-name`, `inspect-detail-btn`, `inspect-arrow`.
* **Events & Interactions**:
  * Clicking "Inspect Deep SHAP Attribution →" button executes `onOpenDetail(flow)`.

---

### 7. `RiskGauge.jsx`
* **File Path**: [`frontend/src/components/RiskGauge.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/RiskGauge.jsx)
* **On-Screen Display**: High-precision SVG chronograph dial rendering 40 tick marks, calibrated 0-100 numerals, inactive circular track arc, active colored sweep arc, and large numeric center score readout.
* **Props**:
  * `score`: float 0–100 fused risk score (default: 0).
  * `size`: integer width/height in pixels (default: 150).
* **State**: Custom hook `useAnimatedScore` animates numeric transition via cubic easing ($1 - (1-t)^3$) and `requestAnimationFrame`.
* **Child Components**: None (pure SVG geometry).
* **CSS Class Names**:
  * `risk-gauge-container`, `chronograph-ticks`.

---

### 8. `TrustPanel.jsx`
* **File Path**: [`frontend/src/components/TrustPanel.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/TrustPanel.jsx)
* **On-Screen Display**: Zero-Trust score hero readout (/100), band tag, 4 interactive toggle switches (MFA, Device Health, Known Location, Normal Hours), and "Re-send with new trust signals" simulation button.
* **Props**:
  * `flow`: active selected flow object.
  * `sendFlow`: WebSocket sender callback `(payload) => void`.
* **State**:
  * `signals`: `{ mfa_on: bool, device_healthy: bool, known_location: bool, normal_hours: bool }`.
  * `ripple`: boolean triggering visual bounce animation on the score number.
* **Child Components**:
  * Internal helper `AnimatedScoreRoll`.
  * Internal helper `Toggle`.
* **CSS Class Names**:
  * `panel`, `panel-stage-3`, `panel-header`, `panel-title`, `panel-badge`, `panel-body`, `trust-panel-inner`, `trust-hero`, `trust-number-wrap`, `trust-number`, `trust-score-ripple`, `trust-band-label`, `trust-hint`, `toggles-grid`, `toggle-item`, `toggle-label`, `toggle-switch`, `toggle-slider`, `resend-btn`, `resend-icon`, `trust-formula-hint`.
* **Events & Interactions**:
  * Toggling any of the 4 switches updates local `signals` state and triggers ripple animation.
  * Clicking `Re-send with new trust signals` constructs a synthetic flow (`flow_id + '-retrust'`) copying 52 packet features and overwriting trust flags, then transmits over WebSocket.

---

### 9. `MitigationPanel.jsx`
* **File Path**: [`frontend/src/components/MitigationPanel.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/MitigationPanel.jsx)
* **On-Screen Display**: Large mitigation action header (ALLOW, RATE-LIMIT, QUARANTINE, BLOCK), policy reason text, enforcement detail cards, simulated VLAN 99 indicator, interactive Cowrie decoy shell terminal with typewriter animations, and Telegram alert status.
* **Props**:
  * `flow`: active selected flow object.
  * `vlanData`: object containing simulated VLAN status flags.
* **State**:
  * `honeypotSession`: session telemetry object fetched from `/api/honeypot-session/{flow_id}`.
  * `showTerminal`: boolean toggling terminal shell visibility.
* **Child Components**:
  * Internal helper `TypewriterText` (animates typewriter terminal character printing via `setInterval`).
* **CSS Class Names**:
  * `panel`, `panel-stage-4`, `panel-header`, `panel-title`, `panel-badge`, `panel-body`, `empty-state`, `miti-action-display`, `miti-action-icon`, `miti-action-text`, `miti-action-label`, `miti-reason`, `miti-details`, `miti-row`, `miti-tag-badge`, `miti-text`, `vlan-badge`, `honeypot-terminal-wrapper`, `honeypot-header`, `honey-dots`, `hdot`, `hdot-red`, `hdot-yellow`, `hdot-green`, `honey-title`, `honey-toggle-btn`, `honeypot-terminal-body`, `honey-meta-bar`, `honey-dim`, `honey-auth-line`, `honey-auth-badge`, `honey-console-stream`, `honey-cmd-block`, `honey-cmd-line`, `honey-prompt`, `honey-cmd-text`, `honey-output-text`, `honey-cursor-line`, `honey-cursor`, `honey-footer-stats`, `honey-trapping-live`, `trapping-dot`, `telegram-alert-banner`.
* **Events & Interactions**:
  * Clicking `Show Terminal` / `Hide Terminal` toggles `showTerminal` boolean.
  * Automatically fetches `/api/honeypot-session/{flow_id}` when selected flow action is `Quarantine`.

---

### 10. `RedTeamPanel.jsx`
* **File Path**: [`frontend/src/components/RedTeamPanel.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/RedTeamPanel.jsx)
* **On-Screen Display**: Compact summary panel for adversarial benchmarks: Total Tested, Still Detected, Evaded stats cards, and interactive comparison table of Baseline vs Perturbed actions.
* **Props**:
  * `data`: red team results object (`total_tested`, `still_detected`, `evaded`, `per_flow`).
  * `error`: error string (or null).
  * `onOpenDetail`: callback `(flow) => void`.
* **State**: Local `StatCount` helper manages animated integer count-up.
* **Child Components**:
  * Internal helper `StatCount`.
  * Internal helper `DetectedBadge`.
* **CSS Class Names**:
  * `panel`, `panel-stage-6`, `panel-header`, `panel-title`, `panel-badge`, `panel-body`, `empty-state`, `redteam-summary`, `redteam-stats-grid`, `redteam-stat-card`, `redteam-stat-num`, `redteam-stat-label`, `redteam-table-wrap`, `redteam-table`, `redteam-row`, `row-evaded`, `row-detected`, `interactive-row`, `action-pill`, `detected-badge-wrap`, `check-svg`, `check-path`.
* **Events & Interactions**:
  * Clicking any table row calls `onOpenDetail(row)`.

---

### 11. `FlowDetailPage.jsx`
* **File Path**: [`frontend/src/components/FlowDetailPage.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/FlowDetailPage.jsx)
* **On-Screen Display**: Comprehensive inspection view featuring top navigation with Back button, executive AI Threat Diagnosis banner, sub-tab bar (`SHAP & Ensemble Attribution`, `Mitigation & Honeypot`, `Raw Packet Telemetry Matrix`, `Adversarial Robustness`), and categorized 52-feature data grid.
* **Props**:
  * `flow`: active flow object under inspection.
  * `vlanData`: VLAN status dictionary.
  * `redTeamData`: red-team results dictionary.
  * `onBack`: callback `() => void` returning to dashboard.
* **State**:
  * `activeTab`: `'ensemble' | 'mitigation' | 'features' | 'adversarial'` (default: `'ensemble'`).
* **Child Components**:
  * [`RiskGauge`](file:///c:/Music/TrustFlowNGFW/frontend/src/components/RiskGauge.jsx)
* **CSS Class Names**:
  * `detail-page-wrapper`, `detail-page-nav`, `back-btn`, `detail-flow-title-row`, `detail-flow-badge`, `detail-meta-chip`, `ai-diagnosis-card`, `diagnosis-header`, `diagnosis-verdict-pill`, `verdict-threat`, `verdict-quarantine`, `verdict-warning`, `verdict-clean`, `diagnosis-body`, `diagnosis-summary`, `diagnosis-grid`, `diag-block`, `diag-title`, `diag-text`, `detail-tab-nav`, `detail-tab-btn`, `active`, `detail-tab-content`, `features-grid`, `feature-cat-card`, `feature-cat-title`, `cat-pill`, `feature-list`, `feature-row`, `feat-name`, `feat-val`.
* **Events & Interactions**:
  * Clicking `← Back to Live SOC Dashboard` calls `onBack()`.
  * Clicking sub-tab buttons updates `activeTab` state.

---

### 12. `ReportsPage.jsx`
* **File Path**: [`frontend/src/pages/ReportsPage.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/pages/ReportsPage.jsx)
* **On-Screen Display**: Reporting and Compliance management console. Includes Daily / Monthly toggle, date picker, "Download PDF" action button, KPI tiles, mitigation distribution progress bars, AI sub-model attribution table, SOC audit table preview, and live PDF generator.
* **Props**:
  * `flows`: array of flow objects.
  * `incidentLogs`: array of incident objects.
  * `vlanData`: VLAN dictionary.
  * `redTeamData`: red-team results dictionary.
* **State**:
  * `reportType`: `'daily' | 'monthly'`.
  * `selectedDate`: string date `YYYY-MM-DD`.
  * `selectedMonth`: string month `YYYY-MM`.
  * `isGenerating`: boolean loading flag during PDF generation.
* **Child Components**: None.
* **CSS Class Names**:
  * `reports-page-container`, `page-header-banner`, `banner-icon-wrap`, `banner-text`, `banner-title`, `banner-subtitle`, `report-controls-card`, `control-group`, `control-label`, `report-type-toggle`, `toggle-btn`, `active`, `date-input`, `btn-download-pdf`, `btn-icon`, `report-preview-sheet`, `sheet-header`, `sheet-title-block`, `sheet-title`, `sheet-subtitle`, `sheet-meta-block`, `sheet-period`, `sheet-doc-id`, `report-kpi-grid`, `report-kpi-card`, `kpi-label`, `kpi-value`, `kpi-unit`, `kpi-sub`, `report-section`, `section-heading`, `distribution-bars-wrap`, `dist-row`, `dist-name-group`, `dist-dot`, `dist-name`, `dist-bar-track`, `dist-bar-fill`, `dist-stat-group`, `dist-pct-badge`, `dist-count`, `preview-table`, `status-badge-ok`, `action-pill`, `preview-sheet-footer`, `btn-download-pdf-small`.
* **Events & Interactions**:
  * Toggling Report Frequency switches between Daily and Monthly modes.
  * Date/Month inputs update reporting time horizon.
  * Clicking `Download Certified PDF Report` triggers `handleDownloadPDF()`, which builds an A4 multi-page vector PDF via `jsPDF` and `jspdf-autotable`.
* **Libraries Used**: `jspdf` (v4.2.1), `jspdf-autotable` (v5.0.8).

---

### 13. `AdversarialPage.jsx`
* **File Path**: [`frontend/src/pages/AdversarialPage.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/pages/AdversarialPage.jsx)
* **On-Screen Display**: Full-page Red-Team Arena displaying top banner, KPI metrics (Total Tested, Maintained Detection, Stealth Evaded, Defense Benchmark %), extended perturbation evaluation table, and architectural defense-in-depth explanation.
* **Props**:
  * `redTeamData`: red team data dictionary.
  * `error`: error string.
  * `onOpenDetail`: callback `(flow) => void`.
* **State**: None (controlled view).
* **Child Components**: None.
* **CSS Class Names**:
  * `page-container`, `page-header-banner`, `banner-icon-wrap`, `orange`, `banner-text`, `banner-title`, `banner-subtitle`, `adversarial-kpi-grid`, `adv-card`, `success`, `danger`, `gold`, `adv-card-label`, `adv-card-value`, `adv-card-sub`, `adv-main-card`, `card-header-flex`, `card-title`, `card-desc`, `card-tag`, `gold-tag`, `adv-table-container`, `adv-table`, `adv-row`, `method-pill`, `action-pill`, `status-evaded`, `status-detected`, `btn-inspect-small`, `adv-strategy-card`, `strategy-title`, `strategy-text`.
* **Events & Interactions**:
  * Clicking `Inspect Flow →` triggers `onOpenDetail(row)`.

---

### 14. `IncidentsPage.jsx`
* **File Path**: [`frontend/src/pages/IncidentsPage.jsx`](file:///c:/Music/TrustFlowNGFW/frontend/src/pages/IncidentsPage.jsx)
* **On-Screen Display**: Full-page Autonomous SOC Incident & Governance Audit Trail displaying KPI metrics, chronological ledger of Llama-3.2 decisions, and active simulated VLAN quarantined hosts table.
* **Props**:
  * `incidentLogs`: array of incident rows.
  * `vlanData`: VLAN state dictionary.
  * `onOpenDetail`: callback `(flow) => void`.
* **State**: None.
* **Child Components**: None.
* **CSS Class Names**:
  * `page-container`, `page-header-banner`, `banner-icon-wrap`, `blue`, `banner-text`, `banner-title`, `banner-subtitle`, `adversarial-kpi-grid`, `adv-card`, `warning`, `info`, `success`, `adv-card-label`, `adv-card-value`, `adv-card-sub`, `adv-main-card`, `card-header-flex`, `card-title`, `card-desc`, `card-tag`, `blue-tag`, `gold-tag`, `adv-table-container`, `adv-table`, `adv-row`, `action-pill`, `severity-badge`, `log-msg-cell`, `status-badge-ok`.
* **Events & Interactions**: None.

---

## 3. Dead, Duplicated, or Unused Components

### 1. `FederatedPanel.jsx` ([frontend/src/components/FederatedPanel.jsx](file:///c:/Music/TrustFlowNGFW/frontend/src/components/FederatedPanel.jsx))
* **Status**: **DEAD / UNUSED**.
* **Finding**: `FederatedPanel` is defined and utilizes `recharts` to render a Flower training accuracy line chart. However, it was removed from `App.jsx` during the UI redesign (lines 243–256 in `App.jsx` state: *"Extended Adversarial Panel taking full bottom space without Federated"*). It is not imported or rendered anywhere in the application.

### 2. `App.css` ([frontend/src/App.css](file:///c:/Music/TrustFlowNGFW/frontend/src/App.css))
* **Status**: **DEAD / UNUSED**.
* **Finding**: Leftover CSS rules from the default Vite starter template (`.hero`, `.counter`, `#next-steps`, `#docs`). Neither `App.jsx` nor `main.jsx` imports `App.css`.

### 3. `CircuitBackground.jsx` ([frontend/src/components/CircuitBackground.jsx](file:///c:/Music/TrustFlowNGFW/frontend/src/components/CircuitBackground.jsx))
* **Status**: **EMPTY / VESTIGIAL**.
* **Finding**: The component body consists entirely of `return null`. It is imported and rendered at the root of `App.jsx`, but produces no DOM nodes.
