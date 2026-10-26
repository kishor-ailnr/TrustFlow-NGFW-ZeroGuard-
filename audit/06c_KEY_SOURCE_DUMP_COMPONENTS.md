# Key Source Dump: Components (Part 1)

## File: frontend/src/components/CircuitBackground.jsx

``jsx
// src/components/CircuitBackground.jsx
// Enterprise Reskin: Flattened background without decorative circuits or canvas lines.

export default function CircuitBackground() {
  return null
}

``

## File: frontend/src/components/Sidebar.jsx

``jsx
// src/components/Sidebar.jsx
// Enterprise Navigation Console — SafeLine / ShieldCore Style

import React from 'react'

export default function Sidebar({ currentTab, onSelectTab, flowCount, wsConnected, theme, toggleTheme }) {
  const navItems = [
    {
      id: 'dashboard',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="3" y="3" width="7" height="9" rx="1"/>
          <rect x="14" y="3" width="7" height="5" rx="1"/>
          <rect x="14" y="12" width="7" height="9" rx="1"/>
          <rect x="3" y="16" width="7" height="5" rx="1"/>
        </svg>
      ),
      title: 'Live SOC Dashboard',
      subtitle: 'Real-time Zero-Trust & ML Matrix',
      badge: `${flowCount} flows`,
      badgeType: 'info',
    },
    {
      id: 'adversarial',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <circle cx="12" cy="12" r="6"/>
          <circle cx="12" cy="12" r="2"/>
        </svg>
      ),
      title: 'Adversarial Tests',
      subtitle: 'Red-Team Evasion & Defense',
      badge: 'Red Team',
      badgeType: 'block',
    },
    {
      id: 'incidents',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
          <polyline points="10 9 9 9 8 9"/>
        </svg>
      ),
      title: 'Incident Audit Trail',
      subtitle: 'Autonomous SOC & VLAN State',
      badge: 'AI Guardrail',
      badgeType: 'accent',
    },
    {
      id: 'reports',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="7 10 12 15 17 10"/>
          <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
      ),
      title: 'Reports & Export',
      subtitle: 'Daily & Monthly PDF Reports',
      badge: 'PDF',
      badgeType: 'allow',
    },
  ]

  return (
    <aside className="app-sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-logo-emblem">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path
              d="M12 2L3 7V12C3 17.52 6.84 22.74 12 24C17.16 22.74 21 17.52 21 12V7L12 2Z"
              stroke="var(--accent)"
              strokeWidth="1.6"
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="var(--accent-subtle)"
            />
            <path
              d="M12 7V17M8 11L12 7L16 11"
              stroke="var(--accent)"
              strokeWidth="1.6"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        <div className="sidebar-brand-text">
          <div className="brand-main">TRUST<span className="accent-text">FLOW</span></div>
          <div className="brand-tag">NEXT-GEN AI FIREWALL</div>
        </div>
      </div>

      <div className="sidebar-nav-section">
        <div className="sidebar-section-title">NAVIGATION CONSOLE</div>
        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const isActive = currentTab === item.id
            return (
              <button
                key={item.id}
                className={`sidebar-nav-item ${isActive ? 'active' : ''}`}
                onClick={() => onSelectTab(item.id)}
              >
                <div className="nav-icon">{item.icon}</div>
                <div className="nav-info">
                  <div className="nav-title">{item.title}</div>
                  <div className="nav-subtitle">{item.subtitle}</div>
                </div>
                {item.badge && (
                  <span className={`nav-badge badge-${item.badgeType}`}>
                    {item.badge}
                  </span>
                )}
                {isActive && <div className="nav-indicator" />}
              </button>
            )
          })}
        </nav>
      </div>

      <div className="sidebar-defense-status">
        <div className="sidebar-section-title">SYSTEM INTEGRITY</div>
        <div className="status-cards-col">
          <div className="status-pill">
            <span className={`status-led ${wsConnected ? 'online' : 'offline'}`} />
            <div className="status-text">
              <span className="status-label">FastAPI Engine</span>
              <span className="status-value">{wsConnected ? 'Connected (Port 8000)' : 'Offline'}</span>
            </div>
          </div>
          <div className="status-pill">
            <span className="status-led online" />
            <div className="status-text">
              <span className="status-label">Ollama SOC Agent</span>
              <span className="status-value">Llama-3.2 (Temp 0.0)</span>
            </div>
          </div>
          <div className="status-pill">
            <span className="status-led online" />
            <div className="status-text">
              <span className="status-label">Active Defense</span>
              <span className="status-value">Windows Netsh + Honeypot 2222</span>
            </div>
          </div>
        </div>
      </div>

      <div className="sidebar-footer">
        <div className="sidebar-footer-row">
          <div>
            <div className="sidebar-version">TrustFlow NGFW v2.4 Enterprise</div>
            <div className="sidebar-status-sub">Zero-Trust Active</div>
          </div>
          {toggleTheme && (
            <button
              className="theme-toggle-sidebar-btn"
              onClick={toggleTheme}
              title={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
              aria-label="Toggle theme"
            >
              {theme === 'light' ? (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                </svg>
              ) : (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="5"/>
                  <line x1="12" y1="1" x2="12" y2="3"/>
                  <line x1="12" y1="21" x2="12" y2="23"/>
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                  <line x1="1" y1="12" x2="3" y2="12"/>
                  <line x1="21" y1="12" x2="23" y2="12"/>
                  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
                </svg>
              )}
            </button>
          )}
        </div>
      </div>
    </aside>
  )
}

``

## File: frontend/src/components/FlowFeed.jsx

``jsx
// src/components/FlowFeed.jsx
// Panel 1 — scrolling live flow list

import { useEffect, useState } from 'react'
import { riskClass } from '../utils'

function FlowScore({ score }) {
  const [val, setVal] = useState(0)
  const target = score ?? 0

  useEffect(() => {
    let start = null
    const duration = 400
    let raf = null
    const step = (ts) => {
      if (!start) start = ts
      const progress = Math.min((ts - start) / duration, 1)
      const ease = 1 - Math.pow(1 - progress, 3)
      setVal(target * ease)
      if (progress < 1) {
        raf = requestAnimationFrame(step)
      } else {
        setVal(target)
      }
    }
    raf = requestAnimationFrame(step)
    return () => cancelAnimationFrame(raf)
  }, [target])

  return <span>{val.toFixed(1)}</span>
}

export default function FlowFeed({ flows, selectedFlowId, onSelect, onOpenDetail }) {
  return (
    <div className="panel span-row panel-stage-1">
      <div className="panel-header">
        <span className="panel-title">Live Flow Feed</span>
        <span className="panel-badge">{flows.length} flows</span>
      </div>
      <div className="panel-body">
        {flows.length === 0 ? (
          <div className="empty-state">
            <div>Waiting for flows on WebSocket…</div>
            <div style={{ fontSize: 11, opacity: 0.6 }}>Send a payload to ws://127.0.0.1:8000/ws</div>
          </div>
        ) : (
          <div className="flow-feed-list">
            {flows.map((f, i) => {
              const isSelected = selectedFlowId === f.flow_id
              return (
                <div
                  key={f.flow_id ? `${f.flow_id}-${i}` : i}
                  className={`flow-item${isSelected ? ' selected' : ''}`}
                  onClick={() => onSelect(f)}
                >
                  <div className="flow-main">
                    <div className="flow-id-row">
                      <span className="flow-id" title={f.flow_id}>{f.flow_id}</span>
                      {onOpenDetail && (
                        <button
                          className="flow-inspect-pill"
                          onClick={(e) => {
                            e.stopPropagation()
                            onOpenDetail(f)
                          }}
                          title="Open detailed flow inspection page"
                        >
                          Inspect ↗
                        </button>
                      )}
                    </div>
                    <div className="flow-meta">
                      <span className="flow-ip">{f.source_ip}</span> &nbsp;·&nbsp; <span className="flow-trust">trust {f.trust_score?.toFixed(0)}</span> ({f.trust_band})
                      &nbsp;·&nbsp; <span className="flow-time">{f._ts}</span>
                    </div>
                  </div>
                  <div className="flow-right">
                    <div className={`flow-risk ${riskClass(f.fused_risk_score)}`}>
                      <FlowScore score={f.fused_risk_score} />
                    </div>
                    <div className={`action-pill ${f.action}`}>{f.action}</div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}


``

## File: frontend/src/components/EnsemblePanel.jsx

``jsx
// src/components/EnsemblePanel.jsx
// Panel 2 — per-flow ensemble breakdown + fused score

import { useEffect, useState } from 'react'
import RiskGauge from './RiskGauge'

function ModelBar({ label, value, barClass }) {
  const [filled, setFilled] = useState(false)
  const pct = Math.round((value ?? 0) * 100)

  useEffect(() => {
    // Fill left-to-right after main gauge settles
    const t = setTimeout(() => setFilled(true), 650)
    return () => clearTimeout(t)
  }, [value])

  return (
    <div className="model-bar-wrap">
      <div className="model-bar-label">
        <span className="model-name">{label}</span>
        <span className="model-val">{(value ?? 0).toFixed(4)}</span>
      </div>
      <div className="bar-track">
        <div
          className={`bar-fill ${barClass}`}
          style={{
            width: filled ? `${pct}%` : '0%',
            transition: 'width 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
          }}
        />
      </div>
    </div>
  )
}

export default function EnsemblePanel({ flow, onOpenDetail }) {
  if (!flow) {
    return (
      <div className="panel panel-stage-2">
        <div className="panel-header">
          <span className="panel-title">Ensemble Breakdown</span>
        </div>
        <div className="empty-state" style={{ height: '100%' }}>
          <div>Click a flow to inspect</div>
        </div>
      </div>
    )
  }

  const { model_a_score, model_b_score, model_c_score, fused_risk_score, shap_attribution } = flow

  return (
    <div className="panel panel-stage-2">
      <div className="panel-header">
        <span className="panel-title">Ensemble Breakdown</span>
        <span className="panel-badge flow-id-badge">{flow.flow_id}</span>
      </div>
      <div className="panel-body">
        <div className="detail-panel decluttered-ensemble">

          {/* Signature gauge — the one bold focal centerpiece */}
          <div className="gauge-wrap">
            <RiskGauge score={fused_risk_score ?? 0} size={145} />
          </div>

          {/* Sub-model bars with clean breathing room */}
          <div className="ensemble-row">
            <ModelBar label="Model A — XGBoost"          value={model_a_score} barClass="bar-a" />
            <ModelBar label="Model B — Isolation Forest" value={model_b_score} barClass="bar-b" />
            <ModelBar label="Model C — JA3 / TLS"        value={model_c_score} barClass="bar-c" />
          </div>

          {/* Decluttered Driver Summary & Detail Page Link */}
          <div className="ensemble-summary-box">
            <div className="shap-driver-pill">
              <span className="shap-driver-label">Primary Driver:</span>
              <span className="shap-driver-name">{shap_attribution?.primary_model ?? 'Model A — XGBoost'}</span>
            </div>
            {onOpenDetail && (
              <button
                className="inspect-detail-btn"
                onClick={() => onOpenDetail(flow)}
                title="Open full SHAP feature attribution and explainability page"
              >
                <span>Inspect Deep SHAP Attribution</span>
                <span className="inspect-arrow">&rarr;</span>
              </button>
            )}
          </div>

        </div>
      </div>
    </div>
  )
}


``

## File: frontend/src/components/RiskGauge.jsx

``jsx
// src/components/RiskGauge.jsx
// Enterprise Precision Instrument Dial for fused_risk_score.
// Flat surfaces, hairline borders, single accent color, no gradients, no glows.

import { useEffect, useRef, useState } from 'react'

const R        = 66          // ring radius
const CX       = 100         // SVG center (viewBox 200x180)
const CY       = 92
const CIRC     = 2 * Math.PI * R   // ~414.69
const STROKE_W = 8
const GAP_DEG  = 64          // open gap at the bottom
const GAP_RAD  = (GAP_DEG / 360) * CIRC   // open gap length

// Clamp score 0-100 and compute stroke-dashoffset
function computeOffset(score) {
  const usable = CIRC - GAP_RAD
  const filled = (Math.min(Math.max(score, 0), 100) / 100) * usable
  return CIRC - filled
}

// Count-up animation synchronized with the sweep
function useAnimatedScore(target, durationMs = 600) {
  const [display, setDisplay] = useState(target)
  const raf  = useRef(null)
  const prev = useRef(target)

  useEffect(() => {
    const from = prev.current
    const to   = target
    if (Math.abs(from - to) < 0.05) { setDisplay(to); return }

    const start = performance.now()
    const tick  = (now) => {
      const t = Math.min((now - start) / durationMs, 1)
      const ease = 1 - Math.pow(1 - t, 3)
      setDisplay(from + (to - from) * ease)
      if (t < 1) {
        raf.current = requestAnimationFrame(tick)
      } else {
        prev.current = to
        setDisplay(to)
      }
    }
    raf.current = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf.current)
  }, [target, durationMs])

  return display
}

// Generate fine chronograph ticks along the usable arc
function generateTicks() {
  const ticks = []
  const totalTicks = 40 // every 2.5%
  const startAngle = 90 + GAP_DEG / 2
  const sweepAngle = 360 - GAP_DEG

  for (let i = 0; i <= totalTicks; i++) {
    const pct = i / totalTicks
    const angleDeg = startAngle + pct * sweepAngle
    const angleRad = (angleDeg * Math.PI) / 180
    const isMajor = i % 4 === 0 // every 10%
    const isMid   = i % 4 === 2
    const innerR  = isMajor ? 52 : (isMid ? 55 : 57)
    const outerR  = 59

    const x1 = CX + innerR * Math.cos(angleRad)
    const y1 = CY + innerR * Math.sin(angleRad)
    const x2 = CX + outerR * Math.cos(angleRad)
    const y2 = CY + outerR * Math.sin(angleRad)

    let label = null
    if (i === 0) label = '0'
    else if (i === 20) label = '50'
    else if (i === 40) label = '100'

    const labelR = 45
    const lx = CX + labelR * Math.cos(angleRad)
    const ly = CY + labelR * Math.sin(angleRad) + 2.5

    ticks.push({
      key: i, x1, y1, x2, y2, isMajor, label, lx, ly, pct: pct * 100
    })
  }
  return ticks
}

const TICKS = generateTicks()

export default function RiskGauge({ score = 0, size = 150 }) {
  const animated = useAnimatedScore(score, 600)
  const offset   = computeOffset(animated)
  const rotationDeg = 90 + GAP_DEG / 2

  return (
    <div className="risk-gauge-container">
      <svg
        viewBox="0 0 200 180"
        width={size}
        height={size * 0.9}
        style={{ overflow: 'visible' }}
        aria-label={`Fused risk score: ${score.toFixed(1)}`}
      >
        {/* Outer bezel circle */}
        <circle
          cx={CX} cy={CY} r={84}
          fill="var(--surface-raised)"
          stroke="var(--border)"
          strokeWidth="1"
        />

        {/* Chronograph tick marks */}
        <g className="chronograph-ticks" opacity="0.8">
          {TICKS.map((t) => (
            <g key={t.key}>
              <line
                x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2}
                stroke={t.pct <= animated ? 'var(--accent)' : 'var(--border-strong)'}
                strokeWidth={t.isMajor ? 1.2 : 0.7}
                strokeLinecap="round"
              />
              {t.label && (
                <text
                  x={t.lx} y={t.ly}
                  textAnchor="middle"
                  fontFamily="var(--font-mono)"
                  fontSize="6.5"
                  fontWeight="600"
                  fill="var(--text-muted)"
                >
                  {t.label}
                </text>
              )}
            </g>
          ))}
        </g>

        {/* Inactive track arc */}
        <circle
          cx={CX} cy={CY} r={R}
          fill="none"
          stroke="var(--border-strong)"
          strokeWidth={STROKE_W}
          strokeDasharray={`${CIRC - GAP_RAD} ${GAP_RAD}`}
          strokeDashoffset={0}
          strokeLinecap="round"
          transform={`rotate(${rotationDeg} ${CX} ${CY})`}
        />

        {/* Active arc with accent color */}
        <circle
          cx={CX} cy={CY} r={R}
          fill="none"
          stroke="var(--accent)"
          strokeWidth={STROKE_W}
          strokeDasharray={`${CIRC - GAP_RAD} ${GAP_RAD}`}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(${rotationDeg} ${CX} ${CY})`}
          style={{
            transition: 'stroke-dashoffset 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
          }}
        />

        {/* Center score readout */}
        <text
          x={CX}
          y={CY + 5}
          textAnchor="middle"
          fill="var(--text-primary)"
          fontFamily="var(--font-mono)"
          fontSize="24"
          fontWeight="700"
          letterSpacing="-0.5px"
        >
          {animated.toFixed(1)}
        </text>

        {/* Dial Subtitle */}
        <text
          x={CX}
          y={CY + 22}
          textAnchor="middle"
          fill="var(--text-muted)"
          fontFamily="var(--font-body)"
          fontSize="7"
          fontWeight="600"
          letterSpacing="0.8px"
        >
          FUSED RISK SCORE
        </text>
      </svg>
    </div>
  )
}

``

## File: frontend/src/components/TrustPanel.jsx

``jsx
// src/components/TrustPanel.jsx
// Panel 3 — trust score display + live toggle re-send

import { useState, useEffect, useRef } from 'react'
import { trustColor } from '../utils'

const FEATURE_COLS = [
  "Destination Port","Flow Duration","Total Fwd Packets","Total Length of Fwd Packets",
  "Fwd Packet Length Max","Fwd Packet Length Min","Fwd Packet Length Mean","Fwd Packet Length Std",
  "Bwd Packet Length Max","Bwd Packet Length Min","Bwd Packet Length Mean","Bwd Packet Length Std",
  "Flow Bytes/s","Flow Packets/s","Flow IAT Mean","Flow IAT Std","Flow IAT Max","Flow IAT Min",
  "Fwd IAT Total","Fwd IAT Mean","Fwd IAT Std","Fwd IAT Max","Fwd IAT Min",
  "Bwd IAT Total","Bwd IAT Mean","Bwd IAT Std","Bwd IAT Max","Bwd IAT Min",
  "Fwd Header Length","Bwd Header Length","Fwd Packets/s","Bwd Packets/s",
  "Min Packet Length","Max Packet Length","Packet Length Mean","Packet Length Std","Packet Length Variance",
  "FIN Flag Count","PSH Flag Count","ACK Flag Count","Average Packet Size","Subflow Fwd Bytes",
  "Init_Win_bytes_forward","Init_Win_bytes_backward","act_data_pkt_fwd","min_seg_size_forward",
  "Active Mean","Active Max","Active Min","Idle Mean","Idle Max","Idle Min"
]

function AnimatedScoreRoll({ value, isRippling }) {
  const [display, setDisplay] = useState(value)
  const prevRef = useRef(value)

  useEffect(() => {
    const from = prevRef.current
    const to   = value
    if (Math.abs(from - to) < 0.1) { setDisplay(to); return }

    let start = null
    const duration = 500
    let raf = null
    const step = (ts) => {
      if (!start) start = ts
      const progress = Math.min((ts - start) / duration, 1)
      const ease = 1 - Math.pow(1 - progress, 3)
      setDisplay(Math.round(from + (to - from) * ease))
      if (progress < 1) {
        raf = requestAnimationFrame(step)
      } else {
        prevRef.current = to
        setDisplay(to)
      }
    }
    raf = requestAnimationFrame(step)
    return () => cancelAnimationFrame(raf)
  }, [value])

  return (
    <span className={`trust-number ${isRippling ? 'trust-score-ripple' : ''}`}>
      {display}
    </span>
  )
}

function Toggle({ id, label, checked, onChange }) {
  return (
    <div className="toggle-item">
      <span className="toggle-label">{label}</span>
      <label className="toggle-switch" htmlFor={id}>
        <input id={id} type="checkbox" checked={checked} onChange={e => onChange(e.target.checked)} />
        <span className="toggle-slider" />
      </label>
    </div>
  )
}

export default function TrustPanel({ flow, sendFlow }) {
  const [signals, setSignals] = useState({
    mfa_on: true, device_healthy: true, known_location: true, normal_hours: true
  })
  const [ripple, setRipple] = useState(false)

  // Sync to selected flow's signals when it changes
  useEffect(() => {
    if (flow) {
      setSignals({
        mfa_on:          flow.mfa_on          ?? true,
        device_healthy:  flow.device_healthy  ?? true,
        known_location:  flow.known_location  ?? true,
        normal_hours:    flow.normal_hours    ?? true,
      })
    }
  }, [flow])

  const set = (key) => (val) => {
    setSignals(prev => ({ ...prev, [key]: val }))
    // Trigger visual ripple on the score number
    setRipple(true)
    setTimeout(() => setRipple(false), 600)
  }

  const trustScore = flow?.trust_score ?? 0
  const trustBand  = flow?.trust_band  ?? '—'

  function handleResend() {
    if (!flow) return
    // Extract feature cols from the last flow, overlay new trust signals
    const payload = { flow_id: flow.flow_id + '-retrust', source_ip: flow.source_ip }
    FEATURE_COLS.forEach(c => { payload[c] = flow[c] ?? 0 })
    Object.assign(payload, signals)
    payload.ja3_risk = flow.ja3_risk ?? 0
    sendFlow(payload)
  }

  return (
    <div className="panel panel-stage-3">
      <div className="panel-header">
        <span className="panel-title">Zero Trust Score</span>
        <span className="panel-badge" style={{ color: trustColor(trustBand) }}>{trustBand}</span>
      </div>
      <div className="panel-body">
        <div className="trust-panel-inner">

          <div className="trust-hero">
            <div className="trust-number-wrap" style={{ color: 'var(--text-primary)' }}>
              <AnimatedScoreRoll value={trustScore} isRippling={ripple} />
            </div>
            <div className="trust-band-label">/ 100 &nbsp;·&nbsp; {trustBand} trust</div>
          </div>

          <div className="trust-hint">
            Flip signals below and hit Re-send to test how trust modifies mitigation action:
          </div>

          <div className="toggles-grid">
            <Toggle id="mfa"     label="MFA enabled"       checked={signals.mfa_on}         onChange={set('mfa_on')} />
            <Toggle id="health"  label="Device healthy"     checked={signals.device_healthy}  onChange={set('device_healthy')} />
            <Toggle id="loc"     label="Known location"     checked={signals.known_location}  onChange={set('known_location')} />
            <Toggle id="hours"   label="Normal hours"       checked={signals.normal_hours}    onChange={set('normal_hours')} />
          </div>

          <button
            className="resend-btn"
            onClick={handleResend}
            disabled={!flow}
          >
            <span className="resend-icon">↺</span> Re-send with new trust signals
          </button>

          <div className="trust-formula-hint">
            trust = mfa(30) + healthy(30) + location(25) + hours(15) &nbsp;·&nbsp; High≥80 · Med≥50 · Low&lt;50
          </div>
        </div>
      </div>
    </div>
  )
}


``

## File: frontend/src/components/MitigationPanel.jsx

``jsx
// src/components/MitigationPanel.jsx
// Panel 4 — iptables enforcement, Cowrie honeypot & Telegram alert status
// Flat enterprise styling, status text colors, no emojis, no glassmorphism

import { useState, useEffect } from 'react'

function TypewriterText({ text, speed = 25 }) {
  const [displayed, setDisplayed] = useState('')

  useEffect(() => {
    let i = 0
    setDisplayed('')
    const timer = setInterval(() => {
      if (i < text.length) {
        setDisplayed(text.slice(0, i + 1))
        i++
      } else {
        clearInterval(timer)
      }
    }, speed)
    return () => clearInterval(timer)
  }, [text, speed])

  return <span>{displayed}</span>
}

export default function MitigationPanel({ flow, vlanData }) {
  const [honeypotSession, setHoneypotSession] = useState(null)
  const [showTerminal, setShowTerminal] = useState(true)

  const { flow_id, source_ip, action, reason } = flow || {}

  useEffect(() => {
    if (flow_id && action === 'Quarantine') {
      fetch(`http://127.0.0.1:8000/api/honeypot-session/${flow_id}`)
        .then(r => r.json())
        .then(d => {
          if (d && d.session_id) setHoneypotSession(d)
        })
        .catch(() => {})
    } else {
      setHoneypotSession(null)
    }
  }, [flow_id, action])

  const actionColors = {
    Allow: 'var(--allow-text)',
    'Rate-limit': 'var(--ratelimit-text)',
    Quarantine: 'var(--quarantine-text)',
    Block: 'var(--block-text)',
  }

  const actionIcons = {
    Allow: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="20 6 9 17 4 12" />
      </svg>
    ),
    'Rate-limit': (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="23 4 23 10 17 10" />
        <polyline points="1 20 1 14 7 14" />
        <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
      </svg>
    ),
    Quarantine: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
        <path d="M7 11V7a5 5 0 0 1 10 0v4" />
      </svg>
    ),
    Block: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
      </svg>
    ),
  }

  if (!flow) {
    return (
      <div className="panel panel-stage-4">
        <div className="panel-header"><span className="panel-title">Mitigation Action</span></div>
        <div className="empty-state" style={{ height: '100%' }}>
          <div>Select a flow to see action taken</div>
        </div>
      </div>
    )
  }

  const vlanEntry = vlanData ? Object.entries(vlanData).find(([k]) => k === flow_id) : null
  const vlanInfo  = vlanEntry ? vlanEntry[1] : null

  return (
    <div className="panel panel-stage-4" style={{ overflowY: 'auto' }}>
      <div className="panel-header">
        <span className="panel-title" style={{ color: actionColors[action] ?? 'var(--text-primary)' }}>
          Mitigation Action
        </span>
        <span className="panel-badge">{source_ip}</span>
      </div>
      <div className="panel-body">

        <div className="miti-action-display">
          <div className="miti-action-icon" style={{ color: actionColors[action] ?? 'var(--text-primary)' }}>
            {actionIcons[action] ?? null}
          </div>
          <div className="miti-action-text">
            <div className="miti-action-label" style={{ color: actionColors[action] ?? 'var(--text-primary)' }}>
              {action}
            </div>
            <div className="miti-reason">{reason}</div>
          </div>
        </div>

        <div className="miti-details">

          {action === 'Block' && (
            <div className="miti-row">
              <span className="miti-tag-badge block">FW-DROP</span>
              <div className="miti-text">
                <strong>Windows Firewall Netsh / iptables DROP rule applied</strong> — source IP{' '}
                <code style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text-primary)' }}>{source_ip}</code>{' '}
                blocked at the kernel level. Rule persists until manually flushed.
              </div>
            </div>
          )}

          {action === 'Quarantine' && (
            <>
              <div className="miti-row">
                <span className="miti-tag-badge quarantine">HONEYPOT</span>
                <div className="miti-text">
                  <strong>Redirected to Cowrie Honeypot</strong> — flow diverted to port 2222 SSH
                  decoy sandbox for attacker profiling and session capture.
                </div>
              </div>
              <div className="miti-row">
                <span className="miti-tag-badge info">VLAN-99</span>
                <div className="miti-text">
                  <strong>VLAN Quarantine Status:</strong>{' '}
                  {vlanInfo ? (
                    <>
                      <span className="vlan-badge">{vlanInfo.vlan_status}</span>
                      {' '}
                      <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                        {vlanInfo.simulated ? '(simulated sandbox isolation)' : ''}
                        {' '}· {vlanInfo.timestamp?.slice(0, 19).replace('T', ' ')}
                      </span>
                    </>
                  ) : (
                    <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>
                      QUARANTINED_VLAN_99 (Decoy Network)
                    </span>
                  )}
                </div>
              </div>

              {/* Decoy Terminal Window */}
              <div className="honeypot-terminal-wrapper">
                <div className="honeypot-header">
                  <div className="honey-dots">
                    <span className="hdot hdot-red"></span>
                    <span className="hdot hdot-yellow"></span>
                    <span className="hdot hdot-green"></span>
                  </div>
                  <div className="honey-title">
                    Decoy Honeypot Shell — {honeypotSession?.session_id || 'COWRIE-SESSION'}
                  </div>
                  <button 
                    className="honey-toggle-btn"
                    onClick={() => setShowTerminal(!showTerminal)}
                  >
                    {showTerminal ? 'Hide Terminal' : 'Show Terminal'}
                  </button>
                </div>

                {showTerminal && (
                  <div className="honeypot-terminal-body">
                    <div className="honey-meta-bar">
                      <div><span className="honey-dim">Host:</span> cowrie-decoy-01:2222</div>
                      <div><span className="honey-dim">Attacker:</span> {source_ip}</div>
                      <div><span className="honey-dim">Isolation:</span> VLAN 99</div>
                      <div><span className="honey-dim">Intent:</span> <span style={{ color: 'var(--quarantine-text)' }}>{honeypotSession?.intent || 'Profiling'}</span></div>
                    </div>

                    <div className="honey-auth-line">
                      <span className="honey-auth-badge">AUTH TRAP</span>
                      <span>SSH login attempt: user=<code>{honeypotSession?.auth?.username || 'root'}</code> pass=<code>••••••••</code> &rarr; <strong style={{ color: 'var(--allow-text)' }}>SESSION GRANTED (DECOY)</strong></span>
                    </div>

                    <div className="honey-console-stream">
                      {honeypotSession?.commands?.map((c, i) => (
                        <div key={i} className="honey-cmd-block">
                          <div className="honey-cmd-line">
                            <span className="honey-prompt">root@decoy:~#</span>
                            <span className="honey-cmd-text">
                              <TypewriterText text={c.cmd} speed={18} />
                            </span>
                          </div>
                          <div className="honey-output-text">
                            <TypewriterText text={c.output} speed={12} />
                          </div>
                        </div>
                      ))}
                      <div className="honey-cursor-line">
                        <span className="honey-prompt">root@decoy:~#</span>
                        <span className="honey-cursor">█</span>
                      </div>
                    </div>

                    <div className="honey-footer-stats">
                      <span><strong>{honeypotSession?.keystrokes_captured || 0}</strong> Keystrokes Logged</span>
                      <span><strong>{honeypotSession?.payloads_intercepted || 0}</strong> Malware Droppers Contained</span>
                      <span className="honey-trapping-live">
                        <span className="trapping-dot" /> Trapping Live
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </>
          )}

          {(action === 'Block' || action === 'Quarantine') && (
            <div className="miti-row telegram-alert-banner">
              <span className="miti-tag-badge block">ALERT</span>
              <div className="miti-text">
                <strong>Telegram alert sent</strong> — SOC notification dispatched via Telegram bot
                (flow_id, action, risk score, trust score, reason).
              </div>
            </div>
          )}

          {(action === 'Allow' || action === 'Rate-limit') && (
            <div className="miti-row">
              <span className="miti-tag-badge allow">PASS</span>
              <div className="miti-text" style={{ color: 'var(--text-muted)' }}>
                No blocking action taken. Flow passed the trust + risk matrix threshold.
                {action === 'Rate-limit' && ' Bandwidth throttling policy applied.'}
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  )
}

``

## File: frontend/src/components/RedTeamPanel.jsx

``jsx
// src/components/RedTeamPanel.jsx
// Panel 6 — adversarial / red-team test results
// Enterprise flat styling, status text colors, no emojis

import { useEffect, useState } from 'react'

function StatCount({ value, duration = 600 }) {
  const [val, setVal] = useState(0)
  const target = Number(value) || 0

  useEffect(() => {
    let start = null
    let raf = null
    const step = (ts) => {
      if (!start) start = ts
      const progress = Math.min((ts - start) / duration, 1)
      const ease = 1 - Math.pow(1 - progress, 3)
      setVal(Math.round(target * ease))
      if (progress < 1) {
        raf = requestAnimationFrame(step)
      } else {
        setVal(target)
      }
    }
    raf = requestAnimationFrame(step)
    return () => cancelAnimationFrame(raf)
  }, [target, duration])

  return <span>{val}</span>
}

function DetectedBadge() {
  return (
    <span className="detected-badge-wrap" style={{ color: 'var(--allow-text)' }}>
      <svg className="check-svg" width="12" height="12" viewBox="0 0 24 24" fill="none">
        <path
          d="M4 12.5L9.5 18L20 6"
          stroke="var(--allow-text)"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="check-path"
        />
      </svg>
      <span>Detected</span>
    </span>
  )
}

export default function RedTeamPanel({ data, error, onOpenDetail }) {
  if (error || !data || Object.keys(data).length === 0) {
    return (
      <div className="panel panel-stage-6">
        <div className="panel-header">
          <span className="panel-title">Adversarial Tests</span>
        </div>
        <div className="empty-state" style={{ height: '100%' }}>
          <div>No red-team results yet</div>
          <div style={{ fontSize: 11, opacity: 0.6 }}>Run backend/redteam/ scripts to populate</div>
        </div>
      </div>
    )
  }

  const { summary, total_tested, still_detected, evaded, per_flow } = data

  return (
    <div className="panel panel-stage-6">
      <div className="panel-header">
        <span className="panel-title">Adversarial Tests</span>
        <span className="panel-badge">{total_tested} flows tested</span>
      </div>
      <div className="panel-body">

        <div className="redteam-summary">{summary ?? `${still_detected}/${total_tested} attacks still detected after perturbation`}</div>

        <div className="redteam-stats-grid">
          {[
            { label: 'Total tested', val: total_tested, color: 'var(--text-primary)' },
            { label: 'Still detected', val: still_detected, color: 'var(--allow-text)' },
            { label: 'Evaded',         val: evaded,         color: 'var(--block-text)' },
          ].map(({ label, val, color }) => (
            <div key={label} className="redteam-stat-card">
              <div className="redteam-stat-num" style={{ color }}>
                {val !== undefined ? <StatCount value={val} /> : '—'}
              </div>
              <div className="redteam-stat-label">{label}</div>
            </div>
          ))}
        </div>

        {per_flow && per_flow.length > 0 && (
          <div className="redteam-table-wrap">
            <table className="redteam-table">
              <thead>
                <tr>
                  <th>Flow ID</th>
                  <th>Baseline</th>
                  <th>Perturbed</th>
                  <th>Result</th>
                </tr>
              </thead>
              <tbody>
                {per_flow.map((row) => {
                  const isInteractive = Boolean(onOpenDetail)
                  const evadedRow = row.result === 'evaded' || row.perturbed_action !== row.baseline_action
                  return (
                    <tr
                      key={row.flow_id}
                      className={`redteam-row ${evadedRow ? 'row-evaded' : 'row-detected'} ${isInteractive ? 'interactive-row' : ''}`}
                      onClick={() => onOpenDetail && onOpenDetail(row)}
                      title={isInteractive ? 'Click to inspect flow' : undefined}
                    >
                      <td><code>{row.flow_id}</code></td>
                      <td>
                        <span className={`action-pill ${row.baseline_action}`}>
                          {row.baseline_action}
                        </span>
                      </td>
                      <td>
                        <span className={`action-pill ${row.perturbed_action}`}>
                          {row.perturbed_action}
                        </span>
                      </td>
                      <td>
                        {evadedRow ? (
                          <span style={{ color: 'var(--block-text)', fontWeight: 600 }}>Evaded</span>
                        ) : (
                          <DetectedBadge />
                        )}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}

      </div>
    </div>
  )
}

``

## File: frontend/src/components/FederatedPanel.jsx

``jsx
// src/components/FederatedPanel.jsx
// Panel 5 — federated learning accuracy chart (recharts)
// Enterprise styling: flat solid line, token colors, no glow, hairline borders

import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ReferenceLine
} from 'recharts'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: 'var(--surface-raised)',
      border: '1px solid var(--border)',
      boxShadow: 'var(--shadow-sm)',
      borderRadius: 4, padding: '6px 10px', fontSize: 11,
      fontFamily: "var(--font-body)"
    }}>
      <div style={{ color: 'var(--text-muted)', marginBottom: 2 }}>Round {label}</div>
      <div style={{ color: 'var(--accent)', fontFamily: "var(--font-mono)", fontWeight: 700 }}>
        Accuracy: {(payload[0].value * 100).toFixed(1)}%
      </div>
    </div>
  )
}

export default function FederatedPanel({ data, error }) {
  return (
    <div className="panel panel-stage-5">
      <div className="panel-header">
        <span className="panel-title">Federated Learning</span>
        <span className="panel-badge">2 simulated nodes</span>
      </div>

      {error && (
        <div style={{ padding: 14, fontSize: 12, color: 'var(--text-muted)' }}>
          No data yet — run federated training to populate.
        </div>
      )}

      {!error && (!data || data.length === 0) && (
        <div className="empty-state" style={{ height: '100%' }}>
          <div>No federated rounds logged yet</div>
        </div>
      )}

      {data && data.length > 0 && (
        <div className="fed-chart-wrap">
          <div style={{ fontSize: 10, color: 'var(--text-muted)', marginBottom: 6, paddingLeft: 8, textTransform: 'uppercase', letterSpacing: '0.8px' }}>
            Model Accuracy by Round
          </div>
          <ResponsiveContainer width="100%" height="82%">
            <LineChart data={data} margin={{ top: 4, right: 16, left: -16, bottom: 4 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis
                dataKey="round"
                tick={{ fill: 'var(--text-secondary)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                label={{ value: 'Round', position: 'insideBottom', offset: -2, fill: 'var(--text-muted)', fontSize: 10 }}
              />
              <YAxis
                domain={[0.5, 1.0]}
                tick={{ fill: 'var(--text-secondary)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                tickFormatter={v => `${(v * 100).toFixed(0)}%`}
              />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={0.9} stroke="var(--text-muted)" strokeDasharray="3 3"
                label={{ value: '90% Target', fill: 'var(--text-muted)', fontSize: 9 }} />
              <Line
                type="monotone"
                dataKey="accuracy"
                stroke="var(--accent)"
                strokeWidth={2}
                dot={{ fill: 'var(--accent)', r: 3, strokeWidth: 1, stroke: 'var(--surface)' }}
                activeDot={{ r: 5, fill: 'var(--accent-hover)', stroke: 'var(--surface)', strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

``


