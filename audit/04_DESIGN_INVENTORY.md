# 04 - Comprehensive Design and Styling Inventory

This document details every design token, color, typographic rule, effect, animation, component pattern, and layout parameter across the TrustFlow NGFW codebase to enable 1:1 visual precision during styling and redesign tasks.

---

## 1. Color Palette and Role Mapping

### 1.1 CSS Custom Properties (`frontend/src/tokens.css`)

| Role | Token Variable | Light Theme (`[data-theme="light"]`) | Dark Theme (`[data-theme="dark"]`) | Usage / Applied Elements |
|---|---|---|---|---|
| **Canvas Background** | `--bg-app` | `#F4F6F9` | `#0A0C0B` | `html`, `body`, `#root`, `app-shell-layout` |
| **Sidebar Surface** | `--bg-sidebar` | `#FFFFFF` | `#0E1110` | `app-sidebar` |
| **Surface (Default)** | `--surface` | `#FFFFFF` | `#111514` | Panels, cards, tables, popovers |
| **Surface (Header)** | `--surface-header` | `#FFFFFF` | `#141918` | `panel-header`, card headers |
| **Surface (Raised)** | `--surface-raised` | `#F8FAFC` | `#181D1C` | RiskGauge bezel fill, inputs, toggle rows, stat tiles |
| **Hairline Border** | `--border` | `#E3E8EF` | `#232A28` | Standard 1px panel and table borders |
| **Strong Border** | `--border-strong` | `#CBD5E1` | `#323B38` | Scrollbar thumb, inactive gauge track, input borders |
| **Primary Text** | `--text-primary` | `#111827` | `#E6EAE8` | High-contrast headings, values, numbers |
| **Secondary Text** | `--text-secondary` | `#4B5563` | `#9AA5A1` | Labels, table cells, descriptions |
| **Muted Text** | `--text-muted` | `#9CA3AF` | `#66716D` | Subtitles, disabled states, hint text |
| **Accent Primary** | `--accent` | `#0F766E` (Deep Teal) | `#22C55E` (Emerald Green) | Active dials, gauge sweep, icons, primary brand text |
| **Accent Hover** | `--accent-hover` | `#115E59` | `#16A34A` | Interactive hover fill, active dot states |
| **Accent Subtle** | `--accent-subtle` | `#E6F4F2` | `rgba(34, 197, 94, 0.10)` | Logo shield background, active nav item tint |
| **Action: Allow (Text)** | `--allow-text` | `#15803D` | `#4ADE80` | Allow pills, success badges, checkmark icons |
| **Action: Allow (BG)** | `--allow-bg` | `#DCFCE7` | `#0F2A1A` | Allow pill background fill |
| **Action: Rate-limit (Text)**| `--ratelimit-text` | `#B45309` | `#FBBF24` | Rate-limit pill text, medium trust badge |
| **Action: Rate-limit (BG)**  | `--ratelimit-bg`   | `#FEF3C7` | `#2B2208` | Rate-limit pill background fill |
| **Action: Quarantine (Text)**| `--quarantine-text`| `#C2410C` | `#FB923C` | Quarantine pills, honeypot headers |
| **Action: Quarantine (BG)**  | `--quarantine-bg`  | `#FFEDD5` | `#301B0C` | Quarantine pill background fill |
| **Action: Block (Text)**     | `--block-text`     | `#B91C1C` | `#F87171` | Block pills, critical risk readouts, firewall drop tag |
| **Action: Block (BG)**       | `--block-bg`       | `#FEE2E2` | `#331416` | Block pill background fill |
| **Informational Tag (Text)** | `--info-text`      | `#475569` | `#9AA5A1` | Standard metadata chip text |
| **Informational Tag (BG)**   | `--info-bg`        | `#F1F5F9` | `#1A1F1E` | Standard metadata chip background fill |
| **Button Primary Fill**      | `--btn-primary-bg` | `#0F766E` | `#16A34A` | Solid CTA buttons (`resend-btn`, `btn-download-pdf`) |
| **Button Primary Text**      | `--btn-primary-text`| `#FFFFFF` | `#FFFFFF` | Contrast text inside solid buttons |
| **Button Primary Hover**     | `--btn-primary-hover`| `#115E59`| `#15803D` | Hover fill on primary CTA buttons |

---

### 1.2 Hardcoded Colors Outside Variables (43 in `index.css` + Inline)

| File | Selector / Element | Hardcoded Color Value | Original Intent / Purpose |
|---|---|---|---|
| `frontend/index.html:12` | `<body style="...">` | `#0B0D10` | Dark splash before CSS load |
| `frontend/src/index.css:193` | `.btn-download-pdf` | `#FFFFFF` | Button label text |
| `frontend/src/index.css:836` | `.honeypot-terminal-body` | `#FFFFFF` | Terminal body background override |
| `frontend/src/index.css:849` | `.honey-output-text` | `#FFFFFF` | Terminal output text |
| `frontend/src/index.css:1134` | `.meta-item` | `#CAD0DB` | Topbar metadata text |
| `frontend/src/index.css:1166` | `.brand-tag` | `#CAD0DB` | Subtitle brand tag |
| `frontend/src/index.css:1496` | `.action-pill.allow` | `rgba(0, 230, 118, 0.18)` | Legacy Neon Green pill fill |
| `frontend/src/index.css:1498` | `.action-pill.allow` | `rgba(0, 230, 118, 0.6)` | Legacy Neon Green border |
| `frontend/src/index.css:1502` | `.action-pill.block` | `rgba(255, 51, 75, 0.2)` | Legacy Crimson Red pill fill |
| `frontend/src/index.css:1504` | `.action-pill.block` | `rgba(255, 51, 75, 0.7)` | Legacy Crimson Red border |
| `frontend/src/index.css:1508` | `.action-pill.quarantine` | `rgba(255, 109, 0, 0.2)` | Legacy Orange pill fill |
| `frontend/src/index.css:1510` | `.action-pill.quarantine` | `rgba(255, 109, 0, 0.7)` | Legacy Orange border |
| `frontend/src/index.css:1514` | `.action-pill.rate-limit` | `rgba(255, 167, 38, 0.2)` | Legacy Amber pill fill |
| `frontend/src/index.css:1516` | `.action-pill.rate-limit` | `rgba(255, 167, 38, 0.7)` | Legacy Amber border |
| `frontend/src/index.css:1642` | `.modal-backdrop` | `rgba(0, 0, 0, 0.45)` | Modal background scrim |
| `frontend/src/index.css:2104` | `.card-desc` | `#94A3B8` | Slate 400 description text |
| `frontend/src/index.css:2111` | `.adv-card-sub` | `#64748B` | Slate 500 subtitle |
| `frontend/src/index.css:2261` | `.adv-table code` | `#E2E8F0` | Code font color in tables |
| `frontend/src/index.css:2558` | `.kpi-label` | `#94A3B8` | Slate 400 uppercase metric label |
| `frontend/src/index.css:2561` | `.kpi-sub` | `#64748B` | Slate 500 caption text |
| `frontend/src/index.css:2617` | `.preview-table th` | `#F1F5F9` | Slate 100 table header fill |
| `frontend/src/index.css:2834` | `.severity-badge.warning` | `rgba(249, 115, 22, 0.2)` / `#FB923C` | Amber warning badge fill/text |
| `frontend/src/index.css:2835` | `.severity-badge.info` | `rgba(56, 189, 248, 0.2)` / `#38BDF8` | Sky blue info badge fill/text |
| `frontend/src/pages/ReportsPage.jsx:109` | PDF Background Canvas | `#FFFFFF` / `[255, 255, 255]` | White A4 page canvas |
| `frontend/src/pages/ReportsPage.jsx:113` | PDF Header Rule | `#0F766E` / `[15, 118, 110]` | Teal primary rule |
| `frontend/src/pages/ReportsPage.jsx:117` | PDF Title Text | `#111827` / `[17, 24, 39]` | Dark slate header text |
| `frontend/src/pages/ReportsPage.jsx:127` | PDF Metadata Subtitle | `#64748B` / `[100, 116, 139]` | Gray subtitle text |
| `frontend/src/pages/ReportsPage.jsx:153` | PDF Table Header Fill | `#F8FAFC` / `[248, 250, 252]` | Light slate header fill |
| `frontend/src/pages/ReportsPage.jsx:157` | PDF Table Grid Lines | `#E3E8EF` / `[227, 232, 239]` | Thin cell border line |
| `frontend/src/pages/ReportsPage.jsx:185-188` | PDF Bar Chart Elements | `[21, 128, 61]`, `[180, 83, 9]`, `[194, 65, 12]`, `[185, 28, 28]` | Green, Amber, Orange, Red |

---

## 2. Typography Inventory

### 2.1 Font Families

| Stack Name | CSS Value | Imported From |
|---|---|---|
| **Body & UI Font** | `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif` | System Native OS Font Stack |
| **Monospace / Code** | `'JetBrains Mono', 'SF Mono', Consolas, monospace` | Google Fonts (`JetBrains Mono:wght@300..700`) + Local Monospace |
| **Imported But Unused** | `'Fraunces'`, `'Plus Jakarta Sans'` | Google Fonts link in `frontend/index.html:10` |

### 2.2 Font Sizes, Weights, and Letter Spacing

| Font Size | Font Weight | Letter Spacing | Selectors / Elements Where Used |
|---|---|---|---|
| `6.5px` | `600` | Normal | `RiskGauge.jsx`: Chronograph tick labels (`0`, `50`, `100`) |
| `7px` | `600` | `0.8px` | `RiskGauge.jsx`: "FUSED RISK SCORE" subdial label |
| `7.5px` | `400` / `700` | Normal | `ReportsPage.jsx` jsPDF table cells and chart labels |
| `8px` | `600` / `700` | `1px` | `topbar .sub`, `brand-tag`, `badge-pill` |
| `9px` | `600` | `0.5px` | `.sidebar-section-title`, `.panel-badge` |
| `10px` | `500` / `600` | `0.5px` | `.flow-time`, `.kpi-sub`, `.dist-stat-group` |
| `10.5px` | `700` | `0.8px` | `.kpi-label`, `.adv-card-label`, `.card-tag` |
| `11px` | `500` / `600` | Normal | `.flow-ip`, `.model-name`, `.method-pill`, `.severity-badge` |
| `12px` | `400` / `600` | Normal | `.flow-trust`, `.honey-dim`, `.diag-title`, `.toggle-label` |
| `13px` | `400` (Base) | Normal | `body`, `table td`, `.miti-text`, `.diag-text` |
| `14px` | `500` / `600` | `-0.2px` | `.nav-title`, `.card-title`, `.section-heading` |
| `16px` | `600` / `700` | `-0.3px` | `.panel-title`, `.banner-title` (small), `.flow-id` |
| `18px` | `700` | `-0.4px` | `.banner-title`, `.brand-title` |
| `24px` | `700` | `-0.5px` | `RiskGauge.jsx` center score readout, `.kpi-value` |
| `28px` | `700` / `800` | `-0.8px` | `.trust-hero .trust-number`, `.adv-card-value` |

---

## 3. Shadows, Borders, Radii, and Visual Effects

### 3.1 Shadows and Depth
* Standard Shadow: `--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05)` (Light) / `rgba(0, 0, 0, 0.20)` (Dark).
* Bezel Shadow: `--bezel-shadow: 0 1px 2px rgba(0, 0, 0, 0.05)`.
* Card Hover Shadow: `box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08)`.
* **Zero Glassmorphism**: `backdrop-filter`, `filter: blur(...)`, and decorative multi-color canvas glow circles were eradicated during the enterprise UI redesign.

### 3.2 Corner Radii
* Panels and Major Containers: `--radius-panel: 6px`.
* Small Controls, Buttons, Inputs: `--radius-sm: 4px`.
* Badges, Chips, Pills: `--radius-xs: 3px`.
* Action Status Badges & Theme Toggles: Fully rounded pill shape (`border-radius: 9999px` / `20px`).

---

## 4. Keyframe Animations and Transitions

| Animation / Transition | Duration | Easing Function | Target Elements |
|---|---|---|---|
| `risk-gauge-arc-sweep` | `600ms` | `cubic-bezier(0.16, 1, 0.3, 1)` | Active SVG arc `stroke-dashoffset` in `RiskGauge.jsx` |
| `model-bar-fill` | `600ms` | `cubic-bezier(0.16, 1, 0.3, 1)` | Sub-model bar width fill (`EnsemblePanel.jsx:28`) |
| `trust-score-ripple` | `600ms` | `ease-out` | Transform scale bounce `scale(1.15)` on trust number change |
| `odometer-roll` | `450ms` | `cubic-bezier(0.16, 1, 0.3, 1)` | Numerical roll-up via `requestAnimationFrame` |
| `typewriter-stream` | `12-25ms/char` | Linear | Terminal command and output printout in `MitigationPanel.jsx` |
| `pulse-led` | `2000ms` | `ease-in-out` infinite | Blinking status LED indicator (`.status-led.online`) |
| `trapping-dot-ping` | `1500ms` | `ease-in-out` infinite | Red recording dot ping (`.trapping-dot`) in decoy terminal |
| Standard UI Hover Transition | `150ms` | `ease` | Buttons, navigation links, table rows (`background-color`, `border-color`) |

---

## 5. UI Component Style Definitions

### 5.1 Card & Panel Containers
```css
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-panel);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.panel-header {
  height: 38px;
  padding: 0 14px;
  background: var(--surface-header);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
```

### 5.2 Action Status Pills
```css
.action-pill {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}
.action-pill.allow      { color: var(--allow-text);      background: var(--allow-bg); }
.action-pill.rate-limit { color: var(--ratelimit-text);  background: var(--ratelimit-bg); }
.action-pill.quarantine { color: var(--quarantine-text); background: var(--quarantine-bg); }
.action-pill.block      { color: var(--block-text);      background: var(--block-bg); }
```

### 5.3 Buttons
* **Primary Solid Action Button** (`.resend-btn`, `.btn-download-pdf`):
  `background: var(--btn-primary-bg); color: var(--btn-primary-text); border: 1px solid transparent; border-radius: var(--radius-sm); font-weight: 600; height: 32px;`
* **Ghost / Inspect Button** (`.flow-inspect-pill`, `.inspect-detail-btn`, `.btn-inspect-small`):
  `background: transparent; color: var(--accent); border: 1px solid var(--border); border-radius: var(--radius-sm); font-size: 11px;`

### 5.4 Toggle Switches
```css
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 32px;
  height: 18px;
}
.toggle-switch input { opacity: 0; width: 0; height: 0; }
.toggle-slider {
  position: absolute; inset: 0;
  background-color: var(--border-strong);
  border-radius: 18px;
  transition: 0.2s;
}
.toggle-slider::before {
  content: "";
  position: absolute; height: 12px; width: 12px; left: 3px; bottom: 3px;
  background-color: white; border-radius: 50%; transition: 0.2s;
}
input:checked + .toggle-slider { background-color: var(--accent); }
input:checked + .toggle-slider::before { transform: translateX(14px); }
```

### 5.5 Tables
* Table headers: `font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); background: var(--surface-raised); border-bottom: 1px solid var(--border);`
* Table rows: `border-bottom: 1px solid var(--border); height: 36px; transition: background 0.15s;`
* Interactive hover: `tr:hover { background: var(--surface-raised); cursor: pointer; }`

---

## 6. Layout Architecture and Grid Structure

### 6.1 Main Shell Layout
* Layout Type: CSS Flexbox Shell (`.app-shell-layout { display: flex; width: 100vw; height: 100vh; overflow: hidden; }`)
* Sidebar: Fixed width `240px`, non-shrinking (`flex: 0 0 240px; border-right: 1px solid var(--border);`).
* Main Viewport: Flexible container (`flex: 1 1 0; overflow-y: auto;`).

### 6.2 SOC Operations Grid (`.main-grid`)
```css
.main-grid {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 12px;
  padding: 12px;
  height: calc(100vh - 54px);
}
.right-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto 1fr;
  gap: 12px;
}
```

### 6.3 Responsive Breakpoints
* **`@media (max-width: 1280px)`**:
  * `.main-grid`: Collapses from 2 columns into 1 vertical column (`grid-template-columns: 1fr`).
  * `.span-row` (FlowFeed): Constrained to height `340px` instead of full view height.
* **`@media (max-width: 1024px)`**:
  * `.right-grid`: Collapses from 2×2 subgrid into a single vertical stack (`grid-template-columns: 1fr`).
  * `.adversarial-kpi-grid`, `.report-kpi-grid`: Collapses from 4 columns to 2 columns.
* **`@media (max-width: 768px)`**:
  * `.app-shell-layout`: Sidebar collapses or stacks above viewport.
  * KPI grids collapse to single-column layout.
