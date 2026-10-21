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
