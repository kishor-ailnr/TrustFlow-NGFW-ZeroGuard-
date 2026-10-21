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

