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

